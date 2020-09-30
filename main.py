import sys
from remote_ckan_interface import RemoteCkanInterface
from local_ckan_interface import LocalCkanInterface

import pprint as pp


def main():
    if len(sys.argv) < 2 or sys.argv[1] == 'help':
        print('Options:\n'
              '  help\n'
              '  remote                     perform an operation agains the remote CKAN server (http://dados.cvm.gov.br)\n'
              '    get [-p,--persist]       download all investment funds related resources in the default datasets\n'
              '                             directory. If including -p, such data will be persisted to the local CKAN\n'
              '                             instance\n\n'
              '        [-d, --dataset <dataset>]\n'
              '                             specify the directory where to store all data, default is "./datasets".\n'
              '    list                     list all investment funds datasets available in the remote CKAN.\n\n'
              '  local\n'
              '    update [-d <dataset>]    persist current resource files in the default datasets directory or\n'
              '                             in the directory specified with -d.')
        return

    ckan = sys.argv[1]
    if ckan == 'remote':
        remote_ckan_cmd(sys.argv[2:])
    elif ckan == 'local':
        local_ckan_cmd(sys.argv[2:])
    else:
        print('Run `py main.py help` for running options.')


def remote_ckan_cmd(args):
    command = args[0]
    ckan = RemoteCkanInterface()

    if command == 'get':
        if_pkgs = ckan.list_if_pkgs()
        print('Datasets of Investment Funds:')
        _pprint(if_pkgs)

        datasets_dir = read_datasets_dir_option(args, True)
        ckan.datasets_dir = datasets_dir
        ckan.download_pkgs(if_pkgs)

        if ('--persist' in args) or ('-p' in args):
            LocalCkanInterface(datasets_dir=datasets_dir).persist_resources()

    elif command == 'list':
        _pprint(ckan.list_if_pkgs())


def local_ckan_cmd(args):
    if len(args) > 0 and args[0] == 'update':
        datasets_dir = read_datasets_dir_option(args, False)
        LocalCkanInterface(datasets_dir=datasets_dir).persist_resources()


def read_datasets_dir_option(args, remote_ckan):
    datasets_long_option = '--datasets' in args
    datasets_short_option = '-d' in args

    if datasets_short_option:
        datasets_dir = ''.join(args).split('-d')[1].split(' ')[0]
    elif datasets_long_option:
        datasets_dir = ''.join(args).split('--datasets')[1].split(' ')[0]
    elif remote_ckan:
        datasets_dir = RemoteCkanInterface.DATASETS_DIR
    else:
        datasets_dir = LocalCkanInterface.DATASETS_DIR

    return datasets_dir.strip()


def _pprint(x):
    pp.PrettyPrinter(indent=2).pprint(x)


if __name__ == '__main__':
    main()
