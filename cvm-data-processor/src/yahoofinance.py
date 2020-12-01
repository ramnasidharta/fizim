import sys
import logging

import yfinance


LOG = logging.getLogger('yahoofinance')
LOG.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
LOG.addHandler(stdout_handler)


def current_price(companies: dict):
    current_price_list = []

    i = 0
    for company_id in companies:
        company = companies[company_id]

        LOG.info('Obtaining data from %s %s', company['name'], f'(code={company["codes"]})')

        try:
            # TODO: remember to remove '.SA' if the source file already
            # records codes with it
            ticker_info = yfinance.Ticker(company['codes'] + '.SA').info
        except Exception as e:
            LOG.error(e)
            continue

        previous_close = ticker_info['previousClose']
        LOG.info('Price = %s', previous_close)
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
    company_codes_str = ' '.join(company_codes)

    tickers = yfinance.Tickers(company_codes_str).tickers

    current_prices = {}
    i = 0  # to iterate over company_codes
    for ticker in tickers:
        LOG.info('Obtaining data from %s', company_codes[i])

        try:
            ticker_current_price = ticker.info['previousClose']
            LOG.info('Price: %s', ticker_current_price)
        except KeyError as e:
            if e.args[0] == 'regularMarketOpen':
                LOG.error('No regularMarketOpen found, skipping it.')
                continue
        except ValueError as e:
            LOG.error(e)
            continue


        current_prices[company_codes[i]] = ticker_current_price
        i += 1

    LOG.info('Number of obtained last close price: %d', len(current_prices))
    LOG.info(current_prices)
    return current_prices
