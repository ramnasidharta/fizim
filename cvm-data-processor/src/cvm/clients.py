import os
import sys
import re
import requests
import logging

from pathlib import Path
from requests import Response

from ckanapi import RemoteCKAN


LOG = logging.getLogger('clients')
LOG.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
LOG.addHandler(stdout_handler)


def _build_directories(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def _save_resource_stream(response: Response, path: str):
    response.raise_for_status()
    with open(path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


class CvmClient:
    """
    Class used to interact with the remote CVM platform (http://dados.cvm.gov.br)

    The CVM platform is a CKAN (https://github.com/ckan/ckan/) instance, so to
    pull data from it, this class uses the ckanapi lib.
    """

    CVM_URL = 'http://dados.cvm.gov.br'

    def __init__(self, datasets_dir=None):
        """Default constructor that initializes an instance of CKAN.

        Besides the ckan instance, initializes a dict to register the paths of
        downloaded data in the following form
          {
            "packageX": {
               "resourceX1": "path to the file",
               ...
            }
          }

        Args:
            datasets_dir - the path of the local directory where datasets
                           (packages) should be saved. Defaults to the value of
                           the DATASETS environment variable.
        """
        if datasets_dir:
            self.datasets_dir = datasets_dir
        else:
            try:
                self.datasets_dir = os.environ['DATASETS']
            except KeyError:
                current_dir = Path().absolute()
                self.datasets_dir = str(current_dir.parent) + '/datasets'

        self.ckan = RemoteCKAN(CvmClient.CVM_URL)
        self.local_files = {}

    def list_pkgs(self, pattern: str = None) -> list:
        """Returns a list of all packages of the CVM platform that follow the
        pattern.

        Args:
            pattern - a regex pattern to filter the packages of the CVM
                      platform.

        Returns:
            a list with the name of the packages.
        """
        packages = self.ckan.action.package_list()

        if pattern:
            pkgs_matcher = re.compile(pattern)
            packages = list(filter(
                lambda x: pkgs_matcher.match(x),
                packages
            ))

        return packages

    def download_pkgs(self, pkgs: list):
        """Downloads all the given packages to self.datasets_dir.

        Args:
            pkgs - a list with the names of the packages to download.
        """
        LOG.info('Download resources from all CVM datasources...')
        for pkg in pkgs:
            self.download_resources(pkg)

    def download_resources(self, package):
        """Download all resources of the given package.

        Calls the CVM platform to obtain all the information of the given
        package (a dict), so getting the list of resources from it and
        downloading one by one.

        At the end, self.local_files will contain all paths of the resources
        downloaded.

        Args:
            package - the name of the packages which the resources should be
                      downloaded from.
        """
        package_data = self.ckan.action.package_show(id=package)
        package_resources = package_data['resources']

        self.local_files[package] = {}  # add resource names with their paths

        for res in package_resources:
            url = res['url']
            LOG.debug('Resource at ' + url)

            package_subdir = url.split('/')[-2]
            res_name = url.split('/')[-1]
            res_destination = \
                f'{self.datasets_dir}/{package}/{package_subdir}/{res_name}'

            self.download_resource(url, res_destination)
            LOG.info(f'Saved: {res_destination}')

            self.local_files[package][res_name] = res_destination

    @staticmethod
    def download_resource(url, path):
        """Downloads the resource specified by the given URL to the given path.

        Args:
            url  - the URL of the resource to be downloaded.
            path - the destination of the resource to be downloaded.
        """
        path_without_filename_arr = path.split('/')[:-1]
        file_directory = str.join('/', path_without_filename_arr) + '/'
        _build_directories(file_directory)

        with requests.get(url, stream=True) as r:
            _save_resource_stream(r, path)


API_KEY = 'cf0ece1e-854c-4a81-b2c9-af1bb794af3e'


class LocalCkanClient:

    DATASETS_DIR = '../datasets'

    def __init__(self, ckan_url='http://ckan:5000', datasets_dir=DATASETS_DIR):
        self.DATASETS_DIR = datasets_dir
        self.local_ckan = RemoteCKAN(ckan_url, apikey=API_KEY)

    def persist_resources(self):
        print('Persist all files')
        for root, subdirs, files in os.walk(self.DATASETS_DIR):
            files = list(filter(lambda file: file.split('.')[-1] == 'csv', files))

            if len(files) == 0:
                continue

            for f in files:
                self.persist_resource(os.path.join(root, f))

    def persist_resource(self, path):
        split_path = path.split('/')
        package_index = 1
        if split_path[0] == '.':
            package_index = 2
        package = split_path[package_index]
        name = split_path[-1]

        # Create dataset if it doesn't exist yet
        if package not in self.local_ckan.action.package_list():
            print('   Creating dataset named ' + package)
            self.local_ckan.action.package_create(name=package,
                                                  author='program',
                                                  groups=[{'name': 'investment-funds'}],
                                                  owner_org='cvm')

        print(f'\n   Trying to persist {name}...')
        try:
            with open(path, 'rb') as res:
                self.local_ckan.action.resource_create(package_id=package,
                                                       name=name,
                                                       owner_org='cvm',
                                                       upload=res)
        except Exception as e:  # e.g. authentication error
            print('   [ERROR] ', e)
            return

        print(f'   Done!')
