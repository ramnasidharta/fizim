import json
import os
import sys
import logging
import tarfile
import subprocess

from pathlib import Path

import yfinance
import psycopg2


SCRAPPED_FILE = 'src/scrapping/b3_companies_scrapped.json'
CLEANED_FILE = 'src/scrapping/b3_companies.json'

LOG = logging.getLogger('utils')
LOG.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
LOG.addHandler(stdout_handler)


def current_price(companies: dict):
    current_price_list = []

    i = 0
    for company_id in companies:
        company = companies[company_id]

        LOG.info('Obtaining data from %s %s', company['name'], f'(code={company["codes"]})')

        try:
            # TODO: remember to remove '.SA' if the source file already
            # records codes with it
            ticker_info = yfinance.Ticker(company['codes'] + '.SA').info
        except Exception as e:
            LOG.error(e)
            continue

        previous_close = ticker_info['previousClose']
        LOG.info('Price = %s', previous_close)
        current_price_list.append(previous_close)

        i = i + 1
        if i == 10:
            break

    return current_price_list


def current_price():
    companies = get_companies()

    # TODO: remember to remove '.SA' if the source file already
    # records codes with it
    company_codes = list(map(lambda c: companies[c]['codes'] + '.SA', companies))
    company_codes_str = ' '.join(company_codes)

    tickers = yfinance.Tickers(company_codes_str).tickers

    current_prices = {}
    i = 0  # to iterate over company_codes
    for ticker in tickers:
        LOG.info('Obtaining data from %s', company_codes[i])

        try:
            ticker_current_price = ticker.info['previousClose']
            LOG.info('Price: %s', ticker_current_price)
        except KeyError as e:
            if e.args[0] == 'regularMarketOpen':
                LOG.error('No regularMarketOpen found, skipping it.')
                continue
        except ValueError as e:
            LOG.error(e)
            continue


        current_prices[company_codes[i]] = ticker_current_price
        i += 1

    LOG.info('Number of obtained last close price: %d', len(current_prices))
    LOG.info(current_prices)
    return current_prices


def clean_scrapped_companies(source_file=SCRAPPED_FILE,
                             target_file=CLEANED_FILE) -> dict:
    """Read source_file (a parsehub scrapping), clean and write to target_file

    Returns: a dictionary in the following form. The id is the name of the
    company but lowercased and without spaces, "." and "/".
        {'id': {
            'name': '',
            'code': '',
            'category': '',
            'sector': ''
        }}
    """

    LOG.debug(f'Reading {SCRAPPED_FILE}...')
    with open(SCRAPPED_FILE, 'r') as parsehub_file:
        parsehub_companies = json.loads(parsehub_file.read())['companies']

    LOG.debug('Extracting companies from file and reformating...')
    companies = {}
    company_names = []
    for company in parsehub_companies:
        name = company['name'].replace('.', '')\
                              .replace(' ', '')\
                              .replace('/', '')\
                              .lower()
        company_names.append(name)
        companies[name] = {
                'name': company['name'],
                'number': company['number'],
                'codes': company['code'] + '.SA',
                'category': company['category'],
                'sector': company['sector']
            }

    LOG.debug('Number of companies formated:', len(company_names))

    LOG.debug(f'Writing reformated companies to {CLEANED_FILE}')
    with open(CLEANED_FILE, 'w') as b3_companies_file:
        json.dump(companies, b3_companies_file, indent=2)

    return companies


def get_companies(source: str = CLEANED_FILE) -> dict:
    with open(source, 'r') as companies_file:
        companies_file = companies_file.read()
        companies = json.loads(companies_file)

    return companies


def tar_compress(fname):
    tar = tarfile.open(fname + '.tar', mode='w')
    try:
        tar.add(fname)
    finally:
        tar.close()


class Exporter:
    """Exports normalized data (normalized CSV files) to the database."""

    def __init__(self, datasets_dir=None):
        if datasets_dir:
            self._datasets_dir = datasets_dir
        else:
            try:
                self._datasets_dir = os.environ['DATASETS']
            except KeyError:
                current_dir = Path().absolute()
                self._datasets_dir = str(current_dir.parent) + '/datasets'

    def export_all(self, dbcontainer='docker_fizz-postgresql_1'):
        self.export_all_balances(dbcontainer)
        self.export_all_company_registers(dbcontainer)

    def export_all_balances(self, dbcontainer='docker_fizz-postgresql_1'):
        """Exports all data from self.normalized_dir to the application database

        Args:
            dbcontainer - the database may be running within a docker container.
            This argument says the name of such container.
        """
        data_dir = self._datasets_dir + '/normalized'
        balance_sheets = os.listdir(data_dir)

        if dbcontainer:
            # If the database is running in a docker container, we have to
            # firstly copy the files from the local filesystem to the container.
            # Then the source of the files becomes the path within the
            # container.
            container_dir = dbcontainer + ':/data/'
            self._copy_dir_to_container(data_dir, container_dir)
            data_dir = '/data'

        LOG.debug('Connecting to database to export data to...')
        connection = psycopg2.connect(host='localhost',
                                      port=5432,
                                      dbname='fizz',
                                      user='fizz')
        LOG.debug('Connected!')

        for balance_sheet in balance_sheets:
            try:
                LOG.debug('Exporting data from file %s to database...',
                          balance_sheet)
                self._export_normalized(data_dir + '/' + balance_sheet,
                                        connection)
            except Exception as e:
                LOG.error('Error "%s" when trying to export file %s', str(e),
                          balance_sheet)

        LOG.debug('Finished exporting all data!')

    def export_all_company_registers(self,
                                     dbcontainer='docker_fizz-postgresql_1'):
        """Exports all data from self.normalized_dir to the application database

        Args:
            dbcontainer - the database may be running within a docker container.
            This argument says the name of such container.
        """
        data_dir = self._datasets_dir + '/registers'

        # The data_dir directory is supposed to have only one .csv
        register_file = list(filter(lambda f: f.endswith('.csv'),
                                    os.listdir(data_dir)))[0]

        if dbcontainer:
            # If the database is running in a docker container, we have to
            # firstly copy the files from the local filesystem to the container.
            # Then the source of the files becomes the path within the
            # container.
            container_dir = dbcontainer + ':/data/registers'
            self._copy_dir_to_container(data_dir, container_dir)
            data_dir = '/data/registers'

        LOG.debug('Connecting to database to export data to...')
        connection = psycopg2.connect(host='localhost',
                                      port=5432,
                                      dbname='fizz',
                                      user='fizz')
        LOG.debug('Connected!')

        try:
            LOG.debug('Exporting data from file %s to database...',
                      register_file)
            self._export_company_registers(data_dir + '/' + register_file,
                                           connection)
        except Exception as e:
            LOG.error('Error "%s" when trying to export file %s', str(e),
                      register_file)

        LOG.debug('Finished exporting all data!')

    @staticmethod
    def _copy_dir_to_container(source_path, destine_path):
        curr_dir = os.getcwd()
        os.chdir(os.path.dirname(source_path))

        docker_cmd = f'docker cp {source_path} {destine_path}'
        LOG.debug('Copying files from %s to container %s...', source_path,
                  destine_path)
        LOG.debug(docker_cmd)

        process = subprocess.Popen(docker_cmd.split())
        output_ignored, error_ignored = process.communicate()

        LOG.debug('Finished copying files to container!')

        os.chdir(curr_dir)

    @staticmethod
    def _export_normalized(balance_sheet_path, connection):
        query_str = f'''
        COPY Balance(
            cnpj, name, cvm_code, category, final_accounting_date,
            financial_statement, subcategory, value)
        FROM '{balance_sheet_path}'
        DELIMITER ';'
        CSV HEADER;
        '''
        cursor = connection.cursor()

        cursor.execute(query_str)
        connection.commit()
        cursor.close()

    @staticmethod
    def _export_company_registers(registers_fpath, connection):
        query_str = f'''
        COPY Company(
            cnpj, social_denomination, commercial_denomination, register_date,
            constitution_date, cancellation_date, cancellation_reason,
            situation, situation_start_date, cvm_code, sector, market, category,
            category_start_date, issuer_situation, issuer_situation_start_date,
            addr_type, public_space, addr_complement, neighborhood, county, st,
            country, zip, std, phone, email, resp_type, resp_name,
            resp_acting_start_date, resp_public_space, resp_addr_complement,
            resp_neighbourhood, resp_county, resp_st, resp_country, resp_zip,
            resp_std, resp_phone, resp_email, cnpj_auditor, auditor
        )
        FROM '{registers_fpath}'
        DELIMITER ';'
        CSV HEADER;
        '''
        cursor = connection.cursor()

        cursor.execute(query_str)
        connection.commit()
        cursor.close()
