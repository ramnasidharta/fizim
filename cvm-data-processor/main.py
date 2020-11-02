import sys
from cvm.cvm_client import CvmPlatformClient
from cvm.local_ckan_interface import LocalCkanInterface

import pprint as pp
import utils
import yahoofinance


def main():
    if len(sys.argv) < 2 or sys.argv[1] == 'help':
        print('''Options:
  help       Shows this instructions.
  cvm        Perform an operation with the remote CKAN server (http://dados.cvm.gov.br).
    get  [-p,--persist]
             Download all public companies related resources in the default datasets
             directory. If including -p, such data will be persisted to the local CKAN
             instance.
         [-d, --dataset <dataset>]
             Specify the directory where to store all data, default is "./datasets".
    list [-c]
             List all datasets available in CVM platform. Adding -c will show only
             datasets of public companies.
  clean-scrapped [source_file] [target_file]
            Clean the data from source_file (Parsehub scrapping file) and writes the result to
            target_file (files respectivelly default to "scrapping/b3_companies_scrapped.json"
            and scrapping/b3_companies.json).
  yfinance  Get data from Yahoo Finance website.''')

        return

    args = sys.argv
    command = args[1]
    if command == 'cvm':
        return cvm_cmd(args[2:])
    elif command == 'clean-scrapped':
        if len(args) == 3:
            return utils.clean_scrapped_companies(source_file=args[2])
        if len(args) == 4:
            return utils.clean_scrapped_companies(source_file=args[2],
                                                  target_file=args[3])
        else:
            return utils.clean_scrapped_companies()
    elif command == 'companies':
        if ('-l' in args) or ('--list' in args):
            _pprint(utils.get_companies())
            return
        elif '--previous-close' in args:
            if '-u' in args:
                _pprint(yahoofinance.current_price())
                return
            else:
                # TODO show prices from last update
                print('Not implemented yet')
                return

    print('Unknown command. Run `py main.py help` to see options.')


def cvm_cmd(args):
    command = args[0]
    cvm_client = CvmPlatformClient()

    if command == 'get':
        pkgs = cvm_client.list_pkgs(pattern='cia_aberta.+')

        print('Datasets of public companies:')
        _pprint(pkgs)

        datasets_dir = read_datasets_dir_option(args, True)
        cvm_client.datasets_dir = datasets_dir
        cvm_client.download_pkgs(pkgs)

        # if ('--persist' in args) or ('-p' in args):
        #     LocalCkanInterface(datasets_dir=datasets_dir).persist_resources()

    elif command == 'list':
        if len(args) > 1 and args[1] == '-c':
            _pprint(cvm_client.list_pkgs(pattern='cia_aberta.+'))
        else:
            _pprint(cvm_client.list_pkgs())


def read_datasets_dir_option(args, remote_ckan):
    datasets_long_option = '--datasets' in args
    datasets_short_option = '-d' in args

    if datasets_short_option:
        datasets_dir = ''.join(args).split('-d')[1].split(' ')[0]
    elif datasets_long_option:
        datasets_dir = ''.join(args).split('--datasets')[1].split(' ')[0]
    elif remote_ckan:
        datasets_dir = CvmPlatformClient.DATASETS_DIR
    else:
        datasets_dir = LocalCkanInterface.DATASETS_DIR

    return datasets_dir.strip()


def _pprint(x):
    pp.PrettyPrinter(indent=2).pprint(x)


if __name__ == '__main__':
    main()
