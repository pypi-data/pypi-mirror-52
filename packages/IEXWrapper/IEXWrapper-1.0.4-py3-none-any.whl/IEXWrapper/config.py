from environs import Env

env = Env()

# Cast the environment variables:
IEX_PUBLIC_TOKEN = env('IEX_PUBLIC_TOKEN', 'public_token_value')
IEX_PRIVATE_TOKEN = env('IEX_PRIVATE_TOKEN', 'private_token_value')
IEX_TEST_PUBLIC_TOKEN = env('IEX_TEST_PUBLIC_TOKEN', '')
IEX_TEST_PRIVATE_TOKEN = env('IEX_TEST_PRIVATE_TOKEN', '')

# Constants
IEX_BASE_URL = "https://cloud.iexapis.com/v1"
IEX_BASE_URL_TEST = "https://sandbox.iexapis.com/v1"
IEX_AVAILABLE_RANGES = ['5y','2y', '1y','ytd','6m', '3m', '1m', '1d', 'date', 'dynamic']
IEX_AVAILABLE_GROUPS = ['mostactive', 'gainers', 'losers', 'iexvolume', 'iexpercent', 'infocus']
IEX_BATCH_ENDPOINT = '/stock/market/batch?symbols={}&types={}'
