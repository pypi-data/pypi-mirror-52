from IEXWrapper.config import IEX_AVAILABLE_RANGES, IEX_AVAILABLE_GROUPS


class InvalidAccountPeriod(Exception):
    def __init__(self):
        super().__init__('\'period\' not supported. It can be only annual or quarter')


class InvalidTimeFrame(Exception):
    def __init__(self):
        super().__init__('Available TimeFrames are: {}'.format(IEX_AVAILABLE_RANGES))


class InvalidGroups(Exception):
    def __init__(self):
        super().__init__('Available Groups are: {}'.format(IEX_AVAILABLE_GROUPS))