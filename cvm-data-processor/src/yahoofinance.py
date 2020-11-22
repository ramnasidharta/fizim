import yfinance
from src import utils


def current_price(companies: dict):
    current_price_list = []

    i = 0
    for company_id in companies:
        company = companies[company_id]

        print('Obtaining data from', company['name'], f'(code={company["codes"]})')

        try:
            # TODO: remember to remove '.SA' if the source file already
            # records codes with it
            ticker_info = yfinance.Ticker(company['codes'] + '.SA').info
        except Exception as e:
            print(e)
            continue

        previous_close = ticker_info['previousClose']
        print('Price =', previous_close)
        current_price_list.append(previous_close)

        i = i + 1
        if i == 10:
            break

    return current_price_list


def current_price():
    companies = utils.get_companies()

    # TODO: remember to remove '.SA' if the source file already
    # records codes with it
    company_codes = list(map(lambda c: companies[c]['codes'] + '.SA', companies))
    company_codes_str = ' '.join(company_codes[:100])

    tickers = yfinance.Tickers(company_codes_str).tickers

    current_prices = {}
    i = 0  # to iterate over company_codes
    for ticker in tickers:
        print('Obtaining data from', company_codes[i])

        try:
            ticker_current_price = ticker.info['previousClose']
            print('Price:', ticker_current_price)
        except KeyError as e:
            if e.args[0] == 'regularMarketOpen':
                print('No regularMarketOpen found, skipping it.')
                continue

        current_prices[company_codes[i]] = ticker_current_price
        i += 1

    print('Number of obtained last close price:', len(current_prices))
    print(current_prices)
    return current_prices
