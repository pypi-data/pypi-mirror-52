from urllib import parse
from IEXWrapper.exceptions import InvalidAccountPeriod, InvalidTimeFrame, InvalidGroups
from IEXWrapper.wrapper_base import HTTPTransport


class IEX(HTTPTransport):
    def __init__(self, symbols: str = '', test: bool = False):
        super().__init__(symbols=symbols, test=test)

    def available_stocks(self):
        return self._make_request('/ref-data/symbols')

    def get_stock_quote(self):
        return self._make_batch_request('quote')

    def get_news(self):
        return self._make_batch_request('news')

    def get_book(self):
        return self._make_batch_request('book')

    def get_chart(self, range):
        if range in self._available_ranges:
            return self._make_batch_request('chart&range={}'.format(range))
        else:
            raise InvalidTimeFrame()

    # Returns an array of quotes for the top 10 symbols in a specified list.
    def get_list_value(self, group):
        if group in self._available_groups:
            endpoint = f'/stock/market/{group}'
            return self._make_request(endpoint)
        else:
            raise InvalidGroups()

    def get_sector_performance(self):
        return self._make_request('/stock/market/sector-performance')

    def get_company_info(self):
        return self._make_batch_request('company')

    def get_companies_by_sector(self, sector_name):
        endpoint = '/stock/market/collection/sector?collectionName={}'.format(parse.quote_plus(sector_name))
        return self._make_request(endpoint)

    def get_companies_by_tag(self, tag_name):
        endpoint = '/stock/market/collection/tag?collectionName={}'.format(parse.quote_plus(tag_name))
        return self._make_request(endpoint)

    def get_stock_dividend(self, range):
        if range in self._available_ranges:
            base_endpoint = '/stock/{}/dividends/'+range
            return self._make_multiple_requests(base_endpoint)
        else:
            raise InvalidTimeFrame()

    def get_earnings(self):
        return self._make_batch_request('earnings')

    def get_custom_call(self, endpoint):
        return self._make_request(endpoint)

    def get_financial_overview(self, period):
        if period.lower() in self._available_accounts:
            base_endpoint = '/stock/{}/financials'
            return self._make_multiple_requests(base_endpoint=base_endpoint,parameters={'period': period})
        else:
            raise InvalidAccountPeriod()

    def get_key_stats(self):
        endpoint = '/stock/{}/stats'
        return self._make_multiple_requests(endpoint)

    def get_balance_sheet(self, period):
        if period.lower() in self._available_accounts:
            base_endpoint = '/stock/{}/balance-sheet'
            return self._make_multiple_requests(base_endpoint=base_endpoint, parameters={'period': period})
        else:
            raise InvalidAccountPeriod()

    def get_cash_flow(self, period):
        if period.lower() in self._available_accounts:
            base_endpoint = '/stock/{}/cash-flow'
            return self._make_multiple_requests(base_endpoint=base_endpoint, parameters={'period': period})
        else:
            raise InvalidAccountPeriod()

    def get_income_statement(self, period):
        if period.lower() in self._available_accounts:
            base_endpoint = '/stock/{}/income'
            return self._make_multiple_requests(base_endpoint=base_endpoint, parameters={'period': period})
        else:
            raise InvalidAccountPeriod()

    def get_splits(self, range: str):
        if range in self._available_ranges:
            base_endpoint = '/stock/{}/splits/'+range
            return self._make_multiple_requests(base_endpoint=base_endpoint)
        else:
            raise InvalidTimeFrame()

    def get_estimates_eps(self):
        endpoint = '/stock/{}/estimates'
        return self._make_multiple_requests(endpoint)

    def get_ohlc(self):
        return self._make_batch_request('ohlc')

    def get_previous(self):
        return self._make_batch_request('previous')
