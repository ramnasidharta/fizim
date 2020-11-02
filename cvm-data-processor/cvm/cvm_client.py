import os
import sys
import re
import requests
import logging
from pathlib import Path
from ckanapi import RemoteCKAN
from requests import Response

LOG = logging.getLogger('CvmPlatformClient')
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


class CvmPlatformClient:
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
            self.datasets_dir = os.environ['DATASETS']

        self.ckan = RemoteCKAN(CvmPlatformClient.CVM_URL)
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
        LOG.info('Download resources from all FI datasources...')
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

