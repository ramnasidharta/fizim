import sys
import pprint as pp

from src.cvm.clients import CvmClient, LocalCkanClient
from src.cvm.normalization import BalancesNormalizer,\
    CompaniesRegisterNormalizer

from src import utils, yahoofinance


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
             Specify the directory where to store all data, default is "../datasets".
    normalize-balances
             processes all datasets of financial balances so they are transformed
             into a more convenient format for reading, persisting, etc.
    normalize-registers
             processes the datasets of companies register so they are
             transformed into a more convenient format for reading, persisting,
             etc.
    list [-c]
             List all datasets available in CVM platform. Adding -c will show only
             datasets of public companies.
  clean-scrapped [source_file] [target_file]
            Clean the data from source_file (Parsehub scrapping file) and writes the result to
            target_file (files respectivelly default to "scrapping/b3_companies_scrapped.json"
            and scrapping/b3_companies.json).
  export-all
            Exports all cvm data to the database.
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
    elif command == 'export-all':
        utils.Exporter().export_all()
        return

    print('Unknown command. Run `py main.py help` to see options.')


def cvm_cmd(args):
    command = args[0]

    if command == 'get':
        cvm_client = CvmClient()
        pkgs = cvm_client.list_pkgs(pattern='cia_aberta.+')

        print('Datasets of public companies:')
        _pprint(pkgs)

        cvm_client.download_pkgs(pkgs)
    elif command == 'list':
        cvm_client = CvmClient()
        if len(args) > 1 and args[1] == '-c':
            _pprint(cvm_client.list_pkgs(pattern='cia_aberta.+'))
        else:
            _pprint(cvm_client.list_pkgs())
    elif command == 'normalize-all':
        BalancesNormalizer().normalize_all()
        CompaniesRegisterNormalizer().normalize_all()
    elif command == 'normalize-balances':
        BalancesNormalizer().normalize_all()
    elif command == 'normalize-registers':
        CompaniesRegisterNormalizer().normalize_all()


def read_datasets_dir_option(args):
    datasets_long_option = '--datasets' in args
    datasets_short_option = '-d' in args

    if datasets_short_option:
        datasets_dir = ''.join(args).split('-d')[1].split(' ')[0]
    elif datasets_long_option:
        datasets_dir = ''.join(args).split('--datasets')[1].split(' ')[0]
    else:
        datasets_dir = '../datasets'

    return datasets_dir.strip()


def _pprint(x):
    pp.PrettyPrinter(indent=2).pprint(x)


if __name__ == '__main__':
    main()
