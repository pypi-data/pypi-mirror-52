import requests
from IEXWrapper.config import IEX_AVAILABLE_GROUPS, IEX_BASE_URL, IEX_BASE_URL_TEST, IEX_AVAILABLE_RANGES, \
                              IEX_PRIVATE_TOKEN, IEX_PUBLIC_TOKEN, IEX_TEST_PRIVATE_TOKEN, IEX_TEST_PUBLIC_TOKEN, \
                              IEX_BATCH_ENDPOINT


class HTTPTransport:
    def __init__(self, symbols: str = '', test=False):
        self.ticker = self._format_list(symbols.lower() if isinstance(symbols, str) else [t.lower() for t in symbols])
        self.request_counter = 0
        self._batch_endpoint = IEX_BATCH_ENDPOINT
        self._available_groups = IEX_AVAILABLE_GROUPS
        self._available_ranges = IEX_AVAILABLE_RANGES
        self._available_accounts = ['annual', 'quarter']
        self.query_result = None
        if test:
            self.pk_token = IEX_TEST_PUBLIC_TOKEN
            self.sk_token = IEX_TEST_PRIVATE_TOKEN
            self.base_url = IEX_BASE_URL_TEST
        else:
            self.pk_token = IEX_PUBLIC_TOKEN
            self.sk_token = IEX_PRIVATE_TOKEN
            self.base_url = IEX_BASE_URL

        if len(self.ticker.split(',')) > 100:
            raise ValueError('IEX Cloud support maximum 100 symbols in a single call.')

    @staticmethod
    def _format_list(obj):
        # This method format lists in url format (ex. ['AAPL', 'MSFT'] --> 'AAPL,MSFT')
        if isinstance(obj, str):
            return obj
        elif isinstance(obj, list):
            return str(','.join(obj))
        else:
            raise ValueError('ticker missing')

    def _make_request(self, endpoint, parameters: dict = None):
        parameters = {'token': self.pk_token} if parameters is None else dict(parameters, **{'token': self.pk_token})
        return self._call_server(self.base_url + endpoint, params=parameters)

    def _call_server(self, url, params: dict =None):
        resp = requests.get(url, params=params)

        if resp.status_code == 200:
            self.request_counter += 1
            return resp.json()
        else:
            raise ConnectionError('IEX Trading API response code was: {} - {} URL: {}'\
                                  .format(resp.status_code, resp.reason, resp.url))

    def _make_batch_request(self, type: str):
        endpoint = self._batch_endpoint.format(self.ticker, type)
        return self._make_request(endpoint)

    def _make_multiple_requests(self, base_endpoint: str, parameters: dict = None):
        res = []
        for stock in self.ticker.split(','):
            tmp = self._make_request(base_endpoint.format(stock), parameters=parameters)
            if stock.upper() not in tmp:
                tmp = {stock.upper(): tmp}
            res.append(tmp)
        return res