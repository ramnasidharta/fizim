import json
from functools import reduce

SCRAPPED_FILE = 'scrapping/b3_companies_scrapped.json'
CLEANED_FILE = 'scrapping/b3_companies.json'


def clean_scrapped_companies(source_file=SCRAPPED_FILE,
                             target_file=CLEANED_FILE) -> dict:
    """Read source_file (a parsehub scrapping), clean and write to target_file

    Returns: a dictionary in the following form. The id is the name of the
    company but lowercased and without spaces, "." and "/".
        {'id': {
            'name': '',
            'code': '',
            'category': '',
            'sector': ''
        }}
    """

    print('[Clean scrapped companies]')

    print(f'Reading {SCRAPPED_FILE}...')
    with open(SCRAPPED_FILE, 'r') as parsehub_file:
        parsehub_companies = json.loads(parsehub_file.read())['companies']

    print('Extracting companies from file and reformating...')
    companies = {}
    company_names = []
    for company in parsehub_companies:
        name = company['name'].replace('.', '')\
                              .replace(' ', '')\
                              .replace('/', '')\
                              .lower()
        company_names.append(name)
        companies[name] = {
                'name': company['name'],
                'number': company['number'],
                'codes': company['code'] + '.SA',
                'category': company['category'],
                'sector': company['sector']
            }

    print('Number of companies formated:', len(company_names))

    print(f'Writing reformated companies to {CLEANED_FILE}')
    with open(CLEANED_FILE, 'w') as b3_companies_file:
        json.dump(companies, b3_companies_file, indent=2)

    print('Finished!')
    return companies


def get_companies(source: str = CLEANED_FILE) -> dict:
    with open(source, 'r') as companies_file:
        companies_file = companies_file.read()
        companies = json.loads(companies_file)

    return companies
