import os
from ckanapi import RemoteCKAN


API_KEY = 'cf0ece1e-854c-4a81-b2c9-af1bb794af3e'


class LocalCkanInterface:

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
