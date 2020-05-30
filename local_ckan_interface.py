import os
from pathlib import Path
from ckanapi import RemoteCKAN

API_KEY = '406c8497-fb04-48bc-bb64-0f774c0526c4'

DATASETS_DIR = './datasets'
BASE_URL = 'http://ckan:5000/'
local_ckan = RemoteCKAN(BASE_URL, apikey=API_KEY)


def setup(base_url, datasets_dir):
    BASE_URL = base_url
    DATASETS_DIR = datasets_dir
    local_ckan = RemoteCKAN(BASE_URL, apikey=API_KEY)


def persist_resource(path):
    splitted_path = path.split('/')
    package_index = 1
    if splitted_path[0] == '.':
        package_index = 2
    package = splitted_path[package_index]
    name = splitted_path[-1]

    # Create dataset if it doesn't exist yet
    if package not in local_ckan.action.package_list():
        print('>>   Creating dataset named ' + package)
        local_ckan.action.package_create(name=package, author='program', groups=[{'name':'investment-funds'}], owner_org='cvm')

    # Upload the file if it's csv
    try:
        with open(path, 'rb') as f:
            local_ckan.action.resource_create(package_id=package, name=name, owner_org='cvm', upload=f)
    except Exception as e:
        print('>>   [ERROR] ', e)

    print(f'>>   Persisted!')


def persist_resources():
    print('>> Persist all files')
    for root, subdirs, files in os.walk(DATASETS_DIR):
        files = list(filter(lambda f: f.split('.')[-1] == 'csv', files))

        if len(files) == 0: break

        for f in files:
            persist_resource(os.path.join(root, f))


