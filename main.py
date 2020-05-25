import sys
from remote_ckan_interface import *
from local_ckan_interface import *


def main():
    command = sys.argv[1]
    if command == 'get':
        setup('http://dados.cvm.gov.br/', './datasets')
        get_from_remote_ckan()
    elif command == 'update_db':
        setup('http://localhost:5000/', '')
        persist_resources()


def get_from_remote_ckan():
    fis_pkgs = get_FIs_pkg_names()

    print('>> Datasets of Investment Funds:')
    pprint(fis_pkgs)

    # fis_pkgs = filter(
    #        lambda name: name not in "fi-doc-extrato fi-doc-eventual  fi-doc-compl  fi-doc-cda  fi-doc-balancete  fidc-doc-inf_mensal  fi-cad",
    #        fis_pkgs
    #        )
    download_pkgs(fis_pkgs)


if __name__ == '__main__':
    main()


