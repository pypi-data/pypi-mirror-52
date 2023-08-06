import cyvcf2
import logging
import numpy as np
import os
import pandas as pd

from MODApy.cfg import variantsDBPath, patientPath, cfg
from MODApy.vcfmgr import ParsedVCF

logger = logging.getLogger(__name__)


# TODO: FIND A MORE EFFICIENT WAY TO SUM EMPTY

class VariantsDB(pd.DataFrame):
    @property
    def _constructor(self):
        return VariantsDB

    @classmethod
    def from_exceldb(cls, excelpath):
        if os.path.exists(excelpath):
            try:
                db = pd.read_excel(excelpath)

            except:
                logger.error('There was an error parsing excel File')
                logger.debug('', exc_info=True)
                exit(1)
        else:
            logger.error('Path to excel file incorrect.')
            exit(1)
        db.set_index(['CHROM', 'POS', 'REF', 'ALT', 'GENE_NAME', 'HGVS.C', 'HGVS.P'], inplace=True)
        db = db.pipe(VariantsDB)
        return db

    @classmethod
    def from_csvdb(cls, csvpath):
        if os.path.exists(csvpath):
            try:
                db = pd.read_csv(csvpath)
            except:
                logger.error('There was an error parsing CSV File')
                logger.debug('', exc_info=True)
                exit(1)
        else:
            logger.error('Path to CSV file incorrect.')
            exit(1)
        db.set_index(['CHROM', 'POS', 'REF', 'ALT', 'GENE_NAME', 'HGVS.C', 'HGVS.P'], inplace=True)
        db = db.pipe(VariantsDB)
        return db

    @classmethod
    def buildDB(cls):
        def patientLister(db=None):
            vcfspath = []
            for dirpath, dirnames, filenames in os.walk(patientPath):
                for filename in [f for f in filenames if f.lower().endswith('final.vcf')]:
                    vcfspath.append(os.path.join(dirpath, filename))
            try:
                vcfsnames = [cyvcf2.Reader(x).samples[0] for x in vcfspath]
            except:
                logger.info('No Sample name in one of the vcfs files. Using File Names Instead')
                vcfsnames = [x.rsplit('/', maxsplit=1)[-1].strip('.final.vcf') for x in vcfspath]

            if db is not None:
                addpatnames = [x for x in vcfsnames if x not in db.columns]
                if len(addpatnames) >= 1:
                    logger.info('Adding Patients: {}'.format([x for x in addpatnames]))
                else:
                    logger.error('No Patients to Add')
                    exit(1)
                patientslist = [x for x in vcfspath for y in addpatnames if y in x]
            else:
                patientslist = vcfspath

            return patientslist

        def dbbuilder(patientslist, db=None):
            logger.info('Parsing Patients')
            pvcfs = ParsedVCF.mp_parser(*patientslist)
            pvcfs = [x[['CHROM', 'POS', 'REF', 'ALT', 'ZIGOSITY', 'GENE_NAME', 'HGVS.C', 'HGVS.P']] for x in pvcfs]
            for df in pvcfs:
                if 'ZIGOSITY' not in df.columns:
                    df['ZIGOSITY'] = 'UNKWN'
            pvcfs = [x.rename(columns={'ZIGOSITY': x.name}) for x in pvcfs if 'ZIGOSITY' in x.columns]
            logger.info('Merging parsed patients toDB')
            if db is not None:
                db = db.reset_index()
                pvcfs.insert(0, db)
            pvcfs = [x.set_index(['CHROM', 'POS', 'REF', 'ALT', 'GENE_NAME', 'HGVS.C', 'HGVS.P']) for x in pvcfs]
            tempdb1 = pd.concat(pvcfs, axis=1, join='outer')
            tempdb2 = tempdb1.reset_index().groupby(['CHROM', 'POS', 'REF', 'ALT']).agg(
                {'GENE_NAME': ' | '.join, 'HGVS.P': ' | '.join, 'HGVS.C': ' | '.join}).reset_index()
            pvcfs2 = [x.reset_index().drop(columns=['GENE_NAME', 'HGVS.C', 'HGVS.P']) for x in pvcfs]
            pvcfs2.insert(0, tempdb2)
            pvcfs2 = [x.set_index(['CHROM', 'POS', 'REF', 'ALT']) for x in pvcfs2]
            db = pd.concat(pvcfs2, axis=1, join='outer')
            colslist = ['GENE_NAME', 'HGVS.C', 'HGVS.P']
            for col in colslist:
                db[col] = db[col].apply(lambda x: ' | '.join(set(x.split(' | '))))
            db = db.reset_index().set_index(['CHROM', 'POS', 'REF', 'ALT', 'GENE_NAME', 'HGVS.C', 'HGVS.P'])
            db.replace({'.': np.nan}, inplace=True)
            db = db.pipe(VariantsDB)
            db = db.calcfreqs()
            return db

        if os.path.exists(variantsDBPath):
            if variantsDBPath.rsplit('.')[-1].lower() == 'xlsx':
                logger.info('Parsing XLSX DB File')
                db = VariantsDB.from_exceldb(variantsDBPath)
                patientslist = patientLister(db)
            elif variantsDBPath.rsplit('.')[-1].lower() == 'csv':
                logger.info('Parsing CSV DB File')
                db = VariantsDB.from_csvdb(variantsDBPath)
                patientslist = patientLister(db)
            else:
                logger.error('VariantsDBPath must be a xlsx or csv file')
                exit(1)

        else:
            logger.info('No DB Found, Building new Variants DB')
            patientslist = patientLister()
            db = None
        sublists = [patientslist[i:i + int(cfg['GENERAL']['cores'])] for i in
                    range(0, len(patientslist), int(cfg['GENERAL']['cores']))]
        for l in sublists:
            db = dbbuilder(l, db)
        return db

    def addPatientToDB(self, patient):
        if patient.rsplit('/')[-1].strip('.final.vcf') in self.columns:
            logger.error('Patient already is in DB')
            exit(1)
        if isinstance(patient, str):
            pvcf = ParsedVCF.from_vcf(patient)
        elif isinstance(patient, ParsedVCF):
            pvcf = patient
        else:
            logger.error('Patient must be either a path to vcf or a ParsedVCF object')
            logger.debug('', exc_info=True)
            exit(1)
        pvcf = pvcf[['CHROM', 'POS', 'REF', 'ALT', 'ZIGOSITY', 'GENE_NAME', 'HGVS.C', 'HGVS.P']]
        if 'ZIGOSITY' not in pvcf.columns:
            pvcf['ZIGOSITY'] = 'UNKWN'
        pvcf.rename(columns={'ZIGOSITY': pvcf.name}, inplace=True)
        pvcf.set_index(['CHROM', 'POS', 'REF', 'ALT', 'GENE_NAME', 'HGVS.C', 'HGVS.P'], inplace=True)
        db = pd.concat([self, pvcf], axis=1, join='outer')
        db = db.pipe(VariantsDB)
        db = db.calcfreqs()
        return db

    def to_VarDBXLS(self):
        logger.info('Writing DB to Excel')
        self.reset_index(inplace=True)
        self['POS'] = self['POS'].astype(int)
        self.sort_values(['CHROM', 'POS'], inplace=True)
        os.makedirs(variantsDBPath.rsplit('/', maxsplit=1)[0], exist_ok=True)
        output = pd.ExcelWriter(variantsDBPath)
        workbook = output.book
        datasheet = workbook.add_worksheet('VariantSDB')
        output.sheets['VariantsDB'] = datasheet
        formatpos = workbook.add_format({'num_format': '###,###,###'})
        self['POS'] = self['POS'].astype(int)
        datasheet.set_column('B:B', 15, formatpos)
        self.to_excel(output, sheet_name='VariantsDB', index=False, merge_cells=False)
        output.save()
        logger.info('Xlsx DB construction complete')

    def to_VarDBCSV(self):
        logger.info('Writing DB to CSV')
        self.reset_index(inplace=True)
        self['POS'] = self['POS'].astype(int)
        self.sort_values(['CHROM', 'POS'], inplace=True)
        os.makedirs(variantsDBPath.rsplit('/', maxsplit=1)[0], exist_ok=True)
        self.to_csv(variantsDBPath, index=False,float_format='%.5f')
        logger.info('DB construction complete')

    def calcfreqs(self):
        logger.info('Calculating Variant Frequencies')
        patients = self.columns.tolist()
        if 'FREQ' in patients:
            patients.remove('FREQ')
        if 'ALLELE_FREQ' in patients:
            patients.remove('ALLELE_FREQ')
        self.replace({'.': np.nan}, inplace=True)
        self['FREQ'] = (self[patients].notnull().sum(axis=1) / len(patients))
        self['ALLELE_FREQ'] = self[patients].apply(lambda x: ((x.str.contains('HOM')*1 + x.str.contains('HET')*2).sum())/len(patients*2),axis=1)
        cols = self.columns.tolist()
        cols.remove('FREQ')
        cols.remove('ALLELE_FREQ')
        self = self[['ALLELE_FREQ', 'FREQ'] + cols]
        self.replace({np.nan: '.'}, inplace=True)
        self.pipe(VariantsDB)
        return self
