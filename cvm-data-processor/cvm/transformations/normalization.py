import os
import zipfile

import pandas


class Normalizer:

    def __init__(self, datasets_dir=None):
        if datasets_dir:
            self.datasets_dir = datasets_dir
        else:
            self.datasets_dir = os.environ['DATASETS']

    def unzip(self, file_path: str):
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            file_path_without_ext = file_path[:-4]
            zip_file.extractall(file_path_without_ext)

    def normalize_annual_balances(self, annual_balances_dir: str):
        for file_name in os.listdir(annual_balances_dir):
            if file_name.endswith(".zip"):
                self._normalize_annual_balance(file_name)

    def _normalize_annual_balance(self, annual_balance_dir: str):
        for balance_sheet in os.listdir(annual_balance_dir):
            # One of the files is only descriptive, and it is lowercase, the
            # other ones contains an acronym of the kind of the balance (e.g.
            # BPA, "Balanço Patrimonial Ativo", active balance sheet), that's
            # why this conditional is needed.
            if not balance_sheet.islower():
                self._normalize_balance_sheet(balance_sheet)

    def _normalize_balance_sheet(self, balance_sheet_name: str):
        """Normalize balance sheet by changing values, deleting and renaming
        columns

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
        3. Remove unnecessary columns: "DT_REFER, "VERSAO", "MOEDA",
           "ESCALA_MOEDA", "ORDEM_EXERC", "CD_CONTA", "ST_CONTA_FIXA".
        4. Rename remaining columns from ['CNPJ_CIA', 'DENOM_CIA', 'CD_CVM',
          'GRUPO_DFP', 'DT_FIM_EXERC', 'DS_CONTA', 'VL_CONTA'] to ['cnpj',
          'name', 'cvm_code', 'category', 'date', 'subcategory', 'value']

        Args:
            balance_sheet_name - the name of the CSV file of the balance sheet.
        """
        balance_sheet = pandas.read_csv(balance_sheet_name,
                                        delimiter=';',
                                        encoding='latin-1')

        balance_sheet = balance_sheet[balance_sheet.index % 2 == 1]

        balance_sheet.loc[
            (balance_sheet.ESCALA_MOEDA == 'UNIDADE'), 'VL_CONTA'] /= 1000

        balance_sheet = balance_sheet.drop(columns=['DT_REFER',
                                                    'VERSAO',
                                                    'MOEDA',
                                                    'ESCALA_MOEDA',
                                                    'ORDEM_EXERC',
                                                    'CD_CONTA',
                                                    'ST_CONTA_FIXA'])

        balance_sheet.columns = ['cnpj', 'name', 'cvm_code', 'category', 'date',
                                 'subcategory', 'value']

        balance_sheet.to_csv(balance_sheet_name, sep=';', encoding='latin-1')
