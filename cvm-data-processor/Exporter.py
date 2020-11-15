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

    if not os.path.exists(source + '.tar'):
        LOG.debug('Compressing %s...', source)
        tar_compress(source)
        LOG.debug('Directory compressed!')

    data = open(source + '.tar', 'rb').read()

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

    def __init__(self, normalized_dir=None):
        if normalized_dir:
            self._normalized_dir = normalized_dir
        else:
            try:
                self._normalized_dir = os.environ['DESTINE']
            except KeyError:
                current_dir = Path().absolute()
                self._datasets_dir =\
                    str(current_dir.parent) + '/datasets/normalized'

    def export_all(self, dbcontainer='docker_fizz-postgresql_1'):
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
                self._export_to_database(data_dir + '/' + balance_sheet,
                                         connection)
            except Exception as e:
                LOG.error('Error "%s" when trying to export file %s', str(e),
                          balance_sheet)

        LOG.debug('Finished exporting all data!')

    @staticmethod
    def _export_to_database(balance_sheet_path, connection):
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
