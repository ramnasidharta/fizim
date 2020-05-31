import re
import requests
from pathlib import Path
from ckanapi import RemoteCKAN


def _build_directories(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def _save_resource_stream(r, path):
    r.raise_for_status()
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)


class RemoteCkanInterface:

    DATASETS_DIR = './datasets'

    def __init__(self, ckan_url='http://dados.cvm.gov.br', local_datasets_dir=DATASETS_DIR):
        self.datasets_dir = local_datasets_dir
        self.ckan = RemoteCKAN(ckan_url)
        self.local_files = {}  # { "package": {"resource1": "pathToIt"} }

    def list_pkgs(self):
        return self.ckan.action.package_list()

    def list_if_pkgs(self):
        packages = self.list_pkgs()
        fis_pkgs_matcher = re.compile('fie.+')
        return list(filter(
            lambda x: fis_pkgs_matcher.match(x),
            packages
        ))

    def download_pkgs(self, pkgs):
        print('>> Download resources from all FI datasources...')
        for p in pkgs:
            print(f' Datasource "{p}":')
            p_data = self.ckan.action.package_show(id=p)
            p_resources = p_data['resources']
            self.download_resources(p_resources, p)

    def download_resources(self, resource_list, package):
        self.local_files[package] = {}  # add resource names with their paths

        for res in resource_list:
            url = res['url']
            print('   Resource at ' + url)

            package_subdir = url.split('/')[-2]
            res_name = url.split('/')[-1]
            res_destination = \
                f'{self.datasets_dir}/{package}/{package_subdir}/{res_name}'

            self.download_resource(url, res_destination)
            print(f'   Saved: {res_destination}')

            self.local_files[package][res_name] = res_destination

    @staticmethod
    def download_resource(url, path):
        path_without_filename_arr = path.split('/')[:-1]
        file_directory = str.join('/', path_without_filename_arr) + '/'
        _build_directories(file_directory)

        with requests.get(url, stream=True) as r:
            _save_resource_stream(r, path)
