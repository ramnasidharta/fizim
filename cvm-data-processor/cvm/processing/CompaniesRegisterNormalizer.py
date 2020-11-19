import os
import sys
import logging

from pathlib import Path

import pandas

LOG = logging.getLogger('Normalizer')
LOG.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
LOG.addHandler(stdout_handler)


def _short(fpath):
    return os.path.basename(fpath)


class CompaniesRegisterNormalizer:

    IGNORABLE_COLUMNS = ('DDD_FAX', 'FAX', 'DDD_FAX_RESP', 'FAX_RESP')
    NORMALIZED_COLUMNS = ('cnpj', 'social_denomination',
                          'commercial_denomination', 'register_date',
                          'constitution_date', 'cancellation_date',
                          'cancellation_reason', 'situation',
                          'situation_start_date',
                          'cvm_code', 'sector', 'market', 'category',
                          'category_start_date', 'issuer_situation',
                          'issuer_situation_start_date', 'addr_type',
                          'public_space', 'addr_complement', 'neighborhood',
                          'county', 'st', 'country', 'zip', 'std', 'phone',
                          'email', 'resp_type', 'resp_name',
                          'resp_acting_start_date', 'resp_public_space',
                          'resp_addr_complement', 'resp_neighbourhood',
                          'resp_county', 'resp_st', 'resp_country', 'resp_zip',
                          'resp_std', 'resp_phone', 'resp_email',
                          'cnpj_auditor', 'auditor')

    def __init__(self, datasets_dir=None, destine_dir=None):
        self.datasets_dir = datasets_dir
        self.destine_dir = destine_dir
        self.ignorable_columns = CompaniesRegisterNormalizer.IGNORABLE_COLUMNS
        self.normalized_columns = CompaniesRegisterNormalizer.NORMALIZED_COLUMNS

    @property
    def datasets_dir(self):
        return self._datasets_dir

    @property
    def destine_dir(self):
        return self._destine_dir

    @datasets_dir.setter
    def datasets_dir(self, value):
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
        if value:
            self._destine_dir = value
        else:
            try:
                self._destine_dir = os.environ['DESTINE']
            except KeyError:
                self._destine_dir = self.datasets_dir + '/registers'

    def normalize_all(self):
        LOG.debug('Create %s directory.', self.destine_dir)
        Path(self.destine_dir).mkdir(parents=True, exist_ok=True)

        LOG.debug('cd %s', _short(self.datasets_dir))
        os.chdir(self.datasets_dir)

        self.normalize_dataset(self.datasets_dir + '/cia_aberta-cad')

        os.chdir('../')

    def normalize_dataset(self, datasets_dir_path: str):
        LOG.info("Start processing dataset %s.", _short(datasets_dir_path))

        data_dir_path = datasets_dir_path + '/DADOS'
        LOG.debug('Process data of zipfiles under %s.',
                  _short(data_dir_path))
        for register_file in os.listdir(data_dir_path):
            if register_file.endswith('.csv'):
                register_fpath = f'{data_dir_path}/{register_file}'
                self._normalize_companies_register(register_fpath)

        LOG.info('Finished processing dataset %s.\n',
                 _short(data_dir_path))

    def _normalize_companies_register(self, register_fpath: str):
        LOG.debug('Normalizing balance sheet %s.', _short(register_fpath))
        register = pandas.read_csv(register_fpath, delimiter=';',
                                   encoding='latin-1')

        self._remove_columns(register)
        self._rename_columns(register)
        self._remove_duplicates(register)
        self._nullify_inconsistent(register)

        balance_sheet_name = os.path.basename(register_fpath)
        self._write_normalized(register, balance_sheet_name)

    def _remove_columns(self, balance_sheet: pandas.DataFrame):
        columns_to_drop = list(self.IGNORABLE_COLUMNS)
        balance_sheet.drop(columns=columns_to_drop, inplace=True)

    def _rename_columns(self, balance_sheet: pandas.DataFrame):
        balance_sheet.columns = list(self.NORMALIZED_COLUMNS)

    def _remove_duplicates(self, register: pandas.DataFrame):
        register.drop_duplicates(subset='cvm_code', keep='last', inplace=True)

    def _nullify_inconsistent(self, register: pandas.DataFrame):
        register.loc[register['std'].astype(str).map(len) > 4, 'std'] = None
        register.loc[register.register_date.str.count('-') != 2,
                     'register_date'] = None
        register.loc[register.constitution_date.str.count('-') != 2,
                     'constitution_date'] = None
        register.loc[register.cancellation_date.str.count('-') != 2,
                     'cancellation_date'] = None
        register.loc[register.situation_start_date.str.count('-') != 2,
                     'situation_start_date'] = None
        register.loc[register.category_start_date.str.count('-') != 2,
                     'category_start_date'] = None
        register.loc[register.issuer_situation_start_date.str.count('-') != 2,
                     'issuer_situation_start_date'] = None
        register.loc[register.resp_acting_start_date.str.count('-') != 2,
                     'resp_acting_start_date'] = None

    def _write_normalized(self, balance_sheet: pandas.DataFrame,
                          balance_sheet_name: str):
        destine_csv = f'{self.destine_dir}/{balance_sheet_name}'
        balance_sheet.to_csv(destine_csv, sep=';', encoding='utf-8',
                             index=False)
