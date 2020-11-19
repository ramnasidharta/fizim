import os
import sys
import logging
import tarfile
import subprocess

from pathlib import Path

import psycopg2

LOG = logging.getLogger('Exporter')
LOG.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
LOG.addHandler(stdout_handler)


def copy_dir_to_container(source_path, destine_path):
    os.chdir(os.path.dirname(source_path))

    source = os.path.basename(source_path)

    LOG.debug('Copying files from to container %s...', destine_path)
    process = subprocess.Popen(f'docker cp {source_path} {destine_path}'.split())
    output_ignored, error_ignored = process.communicate()
    LOG.debug('Finished copying files to container!')


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

    def export_all_normalized(self, dbcontainer='docker_fizz-postgresql_1'):
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
            copy_dir_to_container(data_dir, container_dir)
            data_dir = '/data/normalized'

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
        register_file = list(filter(lambda f: f.endswith('.csv'),
                                    os.listdir(data_dir)))[0]

        if dbcontainer:
            # If the database is running in a docker container, we have to
            # firstly copy the files from the local filesystem to the container.
            # Then the source of the files becomes the path within the
            # container.
            container_dir = dbcontainer + ':/data/'
            copy_dir_to_container(data_dir, container_dir)
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
