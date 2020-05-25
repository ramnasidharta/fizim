import requests
import pprint as pp
import re
import local_ckan_interface
from pathlib import Path
from ckanapi import RemoteCKAN


DATASETS_DIR = './datasets'
BASE_URL = 'http://dados.cvm.gov.br/'
cvm_ckan = RemoteCKAN(BASE_URL)


def setup(base_url, datasets_dir):
    BASE_URL = base_url
    DATASETS_DIR = datasets_dir
    cvm_ckan = RemoteCKAN(BASE_URL)


def pprint(x):
    pp.PrettyPrinter(indent=2).pprint(x)


def get_pkg_list():
    return cvm_ckan.action.package_list()


def get_FIs_pkg_names():
    packages = get_pkg_list()
    fis_pkgs_matcher = re.compile('fi.+')
    return list(filter(
        lambda x: fis_pkgs_matcher.match(x),
        packages
    ))


def download_pkgs(pkgs):
    print('>> Download resources from all FI datasources...')
    for p in pkgs:
        print(f'>> Datasource "{p}":')
        p_datapackage = cvm_ckan.action.package_show(id=p)
        p_resources = p_datapackage['resources']
        download_resources(p_resources, p)


def download_resources(resource_list, package):
    for r in resource_list:
        url = r['url']
        print('>>   Resource at ' + url)

        package_subdir = url.split('/')[-2]
        rsc_name = url.split('/')[-1]
        resource_destination = f'{DATASETS_DIR}/{package}/{package_subdir}/{rsc_name}'

        _download_resource(url, resource_destination)
        local_ckan_interface.persist_resource(resource_destination)


def _download_resource(url, path):
    path_without_filename_arr = path.split('/')[:-1]
    file_directory = str.join('/', path_without_filename_arr) + '/'
    _build_directories(file_directory)

    with requests.get(url, stream=True) as r:
        _save_resource_stream(r, path)


def _build_directories(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def _save_resource_stream(r, path):
    r.raise_for_status()
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

