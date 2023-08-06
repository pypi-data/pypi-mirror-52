# todo find a way to aggregate these classes
import pandas as pd


class AvailableStocks:
    # todo
    def __init__(self, server_reponse):
        self.response=server_reponse

    def to_dataframe(self):
        return pd.read_json(self.response)


class StockQuote:
    # todo
    pass


class News:
    # todo
    pass


class Book:
    # todo
    pass


class Chart:
    # todo
    pass


class SectorPerformance:
    # todo
    pass


class CompanyInfo:
    # todo
    pass


class Collection:
    # todo
    pass


class StockDividend:
    # todo
    pass


class Earnings:
    # todo
    pass


class FinancialOverwiev:
    # todo
    pass


class KeyStats:
    # todo
    pass


class BalanceSheet:
    # todo
    pass


class CashFlow:
    # todo
    pass


class IncomeStatement:
    # todo
    pass


class StockSplits:
    # todo
    pass


class EstimatesEPS:
    # todo
    pass


class OHLC:
    # todo
    pass


class Previous:
    # todo
    pass

