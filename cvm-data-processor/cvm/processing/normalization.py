import os
import sys
import pathlib
import zipfile
import logging

import pandas

LOG = logging.getLogger('CvmPlatformClient')
LOG.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
LOG.addHandler(stdout_handler)


class Normalizer:

    IGNORABLE_COLUMNS = ('DT_REFER', 'VERSAO', 'MOEDA', 'ESCALA_MOEDA',
                         'ORDEM_EXERC', 'CD_CONTA', 'ST_CONTA_FIXA')
    NORMALIZED_COLUMNS = ('cnpj', 'name', 'cvm_code', 'category',
                          'final_accounting_date', 'subcategory', 'value')

    def __init__(self, datasets_dir=None,
                 ignorable_columns=IGNORABLE_COLUMNS,
                 normalized_columns=NORMALIZED_COLUMNS):
        if datasets_dir:
            self.datasets_dir = datasets_dir
        else:
            try:
                self.datasets_dir = os.environ['DATASETS']
            except KeyError:
                current_dir = pathlib.Path().absolute()
                self.datasets_dir = str(current_dir.parent) + '/datasets'

        self.ignorable_columns = ignorable_columns
        self.normalized_columns = normalized_columns

    def normalize_all(self):
        """Performs normalization on all data of the datasets cia_aberta-doc-dfp
        and cia_aberta-doc-itr.

        The normalized data will be under the respective directories of the
        datasets, in unzipped subdirectories corresponding to the existing zip
        files.
        """
        LOG.debug('cd %s', self.datasets_dir)
        os.chdir(self.datasets_dir)

        self.normalize_dataset('cia_aberta-doc-dfp')
        self.normalize_dataset('cia_aberta-doc-itr')

        os.chdir('../')

    def normalize_dataset(self, dataset_name: str):
        LOG.info("Start processing dataset %s", dataset_name)
        LOG.debug('cd %s', dataset_name + '/DADOS/')

        os.chdir(dataset_name + '/DADOS/')
        for annual_balance_file in os.listdir():
            if annual_balance_file.endswith('.zip'):
                self.normalize_annual_balances(annual_balance_file)

        LOG.debug('cd ../../')
        os.chdir('../../')
        LOG.info('Finished processing dataset %s', dataset_name)

    def normalize_annual_balances(self, annual_balances_file: str):
        """Unzips the given file and normalizes each of the files within it.

        Args:
            annual_balances_file - name of the file of all balances of a year.
        """
        LOG.info('Start normalization of %s', annual_balances_file)

        self.unzip(annual_balances_file)
        os.chdir(annual_balances_file[:-4])

        for balance_sheet in os.listdir():
            # One of the files is only descriptive, and it is lowercase, the
            # other ones contain an acronym of the kind of the balance (e.g.
            # BPA, "Balanço Patrimonial Ativo", active balance sheet), that's
            # why this conditional is needed. In other words, the condition
            # below is needed because there is (only) one file to be ignored and
            # its name is lowercase.
            if not balance_sheet.islower() and balance_sheet.endswith('.csv'):
                try:
                    self._normalize_balance_sheet(balance_sheet)
                except Exception as e:
                    LOG.error('Error "%s" when normalizing balance sheet %s: %s',
                              e, balance_sheet, str(e))

        os.chdir("../")

    def unzip(self, file_path: str):
        LOG.debug('Unzipping file %s...', file_path)
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            file_path_without_ext = file_path[:-4]
            zip_file.extractall(file_path_without_ext)

    def _normalize_balance_sheet(self, balance_sheet_name: str):
        """Normalize balance sheet by changing values, deleting and renaming
        columns.

        Reads the balance sheet, normalizes it and writes the result to the same
        file. The normalization is composed by four steps:

        1. Remove unnecessary rows. Odd rows contain the value of the previous
           accounting period (in other words, rows with the value "PENÚLTIMO"
           for the column "ORDEM_EXERC"), all those rows, that is, half of the
           columns of the file.
        2. Convert the scale of the accounting values to thousand. Such scale is
           determined by the column "ESCALA_MOEDA" ("MIL", "UNIDADE", ?), so
           this step divides all values which "ESCALA_MOEDA" is "UNIDADE" (unit
           scale) by 1000 (one thousand).
        3. Remove unnecessary columns: self.IGNORABLE_COLUMNS.
        4. Rename remaining columns to the names of self.NORMALIZED_COLUMNS. In
           the default case, the remaining columns are ['CNPJ_CIA', 'DENOM_CIA',
           'CD_CVM', 'GRUPO_DFP', 'DT_FIM_EXERC', 'DS_CONTA', 'VL_CONTA'] and
            will be replaced to ['cnpj', 'name', 'cvm_code', 'category', 'date',
            'subcategory', 'value']

        Args:
            balance_sheet_name - the name of the CSV file of the balance sheet.
        """
        LOG.debug('Normalizing balance sheet %s', balance_sheet_name)
        balance_sheet = pandas.read_csv(balance_sheet_name,
                                        delimiter=';',
                                        encoding='latin-1')

        balance_sheet = balance_sheet[balance_sheet.index % 2 == 1]

        balance_sheet.loc[
            (balance_sheet.ESCALA_MOEDA == 'UNIDADE'), 'VL_CONTA'] /= 1000

        columns_to_drop = list(self.IGNORABLE_COLUMNS)
        if 'DT_INI_EXERC' in balance_sheet.columns:
            columns_to_drop.append('DT_INI_EXERC')
        balance_sheet = balance_sheet.drop(columns=columns_to_drop)

        updated_column_names = list(self.NORMALIZED_COLUMNS)
        if 'COLUNA_DF' in balance_sheet.columns:
            updated_column_names.insert(5, 'financial_statement')
        balance_sheet.columns = updated_column_names

        balance_sheet.to_csv(balance_sheet_name, sep=';', encoding='latin-1')
