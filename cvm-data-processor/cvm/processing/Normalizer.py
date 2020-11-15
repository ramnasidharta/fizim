import os
import sys
import zipfile
import logging

from pathlib import Path

import pandas

LOG = logging.getLogger('Normalizer')
LOG.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
LOG.addHandler(stdout_handler)


def _short(fpath):
    return os.path.basename(fpath)


class Normalizer:
    """"
    This class reads datasets of financial balances of public companies
    registered at CVM and performs operations to organize that data into a
    convenient format, so they can be persisted into a database more easily.

    The datasets read by this class are stored in the filesystem and are
    supposed to be structured exactly as CvmClient obtained them from CVM. Such
    structure is presented below.

    After the normalization processing throughout a dataset, the normalized CSV
    files are written to "normalized/".

    datasets/
        dataset_dir/
            DADOS/
                annual_balances_zip.zip
                annual_balances_dir/
                    annual_balance_sheet.csv
        normalized/
            annual_balance_sheet.csv
    """

    IGNORABLE_COLUMNS = ('DT_REFER', 'VERSAO', 'MOEDA', 'ESCALA_MOEDA',
                         'ORDEM_EXERC', 'CD_CONTA', 'ST_CONTA_FIXA')
    NORMALIZED_COLUMNS = ('cnpj', 'name', 'cvm_code', 'category',
                          'final_accounting_date', 'financial_statement',
                          'subcategory', 'value')

    def __init__(self, datasets_dir=None, destine_dir=None):
        """Creates a new instance of Normalizer.

        Args:
            datasets_dir - the directory where the datasets are in. Defaults to
            '../datasets' (relative to the directory where the program was run).

            destine_dir - the destine directory where to place normalized files.
            Defaults to '../datasets/normalized' (relative to the directory
            where the program was run).
        """
        self.datasets_dir = datasets_dir
        self.destine_dir = destine_dir
        self.ignorable_columns = Normalizer.IGNORABLE_COLUMNS
        self.normalized_columns = Normalizer.NORMALIZED_COLUMNS

    @property
    def datasets_dir(self):
        return self._datasets_dir

    @property
    def destine_dir(self):
        return self._destine_dir

    @datasets_dir.setter
    def datasets_dir(self, value):
        """Sets the path of the CVM datasets directory.

        If the value is None, then try to set the datasets directory based on
        the 'DATASETS' environment variable. If the environment variable doesn't
        exist, defaults to: '../datasets'.
        """
        if value:
            self._datasets_dir = value
        else:
            try:
                self._datasets_dir = os.environ['DATASETS']
            except KeyError:
                current_dir = Path().absolute()
                self._datasets_dir = str(current_dir.parent) + '/datasets'

    @destine_dir.setter
    def destine_dir(self, value):
        """Sets the path of the destine directory of normalized data.

        If the value is None, then try to set the destine directory based on
        the 'DESTINE' environment variable. If the environment variable doesn't
        exist, defaults to: self.datasets_dir + '/normalized'.
        """
        if value:
            self._destine_dir = value
        else:
            try:
                self._destine_dir = os.environ['DESTINE']
            except KeyError:
                self._destine_dir = self.datasets_dir + '/normalized'

    def normalize_all(self):
        """Performs normalization on all financial balances data from CVM
        datasets.

        The datasets in question are two: cia_aberta-doc-dfp and
        cia_aberta-doc-itr. The normalized data will be under the directory
        self.destine_dir.
        """
        LOG.debug('Create %s directory.', self.destine_dir)
        Path(self.destine_dir).mkdir(parents=True, exist_ok=True)

        LOG.debug('cd %s', _short(self.datasets_dir))
        os.chdir(self.datasets_dir)

        self.normalize_dataset(self.datasets_dir + '/cia_aberta-doc-dfp')
        self.normalize_dataset(self.datasets_dir + '/cia_aberta-doc-itr')

        os.chdir('../')

    def normalize_dataset(self, datasets_dir_path: str):
        """Normalizes all data of the given CVM dataset.

        Normalizes all CSV files of the given dataset and place them in the
        directory of normalized data: self.destine_dir. The non-normalized CSV
        files are compressed into multiple zip files. So this method iterates
        over all zip files, decompressing them and them normalizing all files
        within.

        Args:
            datasets_dir_path - the path to the directory of a financial
            balances dataset. This directory is supposed to have zip files
            under the subdirectory DADOS. Each zip file has data of a specific
            accounting year. Such data is organized in CSV files containing
            financial statements, those are the data to be normalized.
        """
        LOG.info("Start processing dataset %s.", _short(datasets_dir_path))

        data_dir_path = datasets_dir_path + '/DADOS'
        LOG.debug('Process data of zipfiles under %s.',
                  _short(data_dir_path))
        for annual_balances_zip in os.listdir(data_dir_path):
            if annual_balances_zip.endswith('.zip'):
                annual_balance_zip_path = f'{data_dir_path}/{annual_balances_zip}'
                self.normalize_annual_balances(annual_balance_zip_path)

        LOG.info('Finished processing dataset %s.\n',
                 _short(data_dir_path))

    def normalize_annual_balances(self, annual_balance_zip_path: str):
        """Unzips the given file and normalizes each of the files within it.

        Args:
            annual_balance_zip_path - path of the file of all balances of a year.
        """
        LOG.info('Start normalization of %s.',
                 _short(annual_balance_zip_path))

        self.unzip(annual_balance_zip_path)

        annual_balances_dir = annual_balance_zip_path[:-4]
        LOG.debug('Normalize annual balance sheets under %s.',
                  _short(annual_balances_dir))

        for balance_sheet in os.listdir(annual_balances_dir):
            # One of the files is only descriptive, it does not contain data to
            # be normalized. This file is lowercase, the other ones always
            # contain an acronym of its kind of balance (e.g. BPA, "Balanço
            # Patrimonial Ativo", active balance sheet), that's why this
            # conditional is needed. In other words, the condition below is
            # needed because there is (only) one file to be ignored and its name
            # is lowercase.
            if not balance_sheet.islower() and balance_sheet.endswith('.csv'):
                balance_sheet_path = f'{annual_balances_dir}/{balance_sheet}'
                try:
                    self._normalize_balance_sheet(balance_sheet_path)
                except Exception as e:
                    LOG.error(
                        'Error "%s" when normalizing balance sheet %s: %s.',
                        e, balance_sheet_path, str(e))

    def unzip(self, file_path: str):
        """Decompresses the given zip file."""
        LOG.debug('Unzipping file %s...', _short(file_path))
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            destine_dir = file_path[:-4]
            zip_file.extractall(destine_dir)

    def _normalize_balance_sheet(self, balance_sheet_path: str):
        """Normalizes balance sheet by changing values, deleting and renaming
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
            balance_sheet_path - the path of the CSV file of the balance sheet.
        """
        LOG.debug('Normalizing balance sheet %s.',
                  _short(balance_sheet_path))
        balance_sheet = pandas.read_csv(balance_sheet_path,
                                        delimiter=';',
                                        encoding='latin-1')

        # Remove odd rows
        balance_sheet = balance_sheet[balance_sheet.index % 2 == 1]

        # Normalize values to "thousand" scale. Units are divided by 1000.
        balance_sheet.loc[
            (balance_sheet.ESCALA_MOEDA == 'UNIDADE'), 'VL_CONTA'] /= 1000

        balance_sheet = self._remove_columns(balance_sheet)
        balance_sheet = self._rename_columns(balance_sheet)

        balance_sheet_name = os.path.basename(balance_sheet_path)
        self._write_normalized(balance_sheet, balance_sheet_name)

    def _remove_columns(self, balance_sheet: pandas.DataFrame):
        """Removes columns from the given balance_sheet.

        Remove the columns specified by IGNORABLE_COLUMNS from the given
        balance sheet, including the column 'DT_INIT_EXERC', which is present
        only in some files."""
        columns_to_drop = list(self.IGNORABLE_COLUMNS)

        # DT_INI_EXERC is present only in some files, but it shall be removes
        # too.
        if 'DT_INI_EXERC' in balance_sheet.columns:
            columns_to_drop.append('DT_INI_EXERC')

        return balance_sheet.drop(columns=columns_to_drop)

    def _rename_columns(self, balance_sheet: pandas.DataFrame):
        """Renames columns of the given balance sheet.

        Renames columns of the given balance sheet based on the names of
        self.NORMALIZED_COLUMNS. The column 'COLUNA_DF', which is not always
        present is renamed to 'financial_statement' (self.NORMALIZED_COLUMNS[5]).
        That column is not always present, in those cases the column
        'financial_statement' is created with empty values.
        """
        if 'COLUNA_DF' not in balance_sheet.columns:
            normalized_column_name = self.NORMALIZED_COLUMNS[5]
            balance_sheet.insert(loc=5, column=normalized_column_name,
                                 value=['' for _ in range(len(balance_sheet))])

        balance_sheet.columns = list(self.NORMALIZED_COLUMNS)

        return balance_sheet

    def _write_normalized(self, balance_sheet: pandas.DataFrame,
                          balance_sheet_name: str):
        destine_csv = f'{self.destine_dir}/{balance_sheet_name}'
        balance_sheet.to_csv(destine_csv, sep=';', encoding='utf-8',
                             index=False)
