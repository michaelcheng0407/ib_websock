from dataclasses import dataclass
from ib_insync.objects import BarDataList
from ib_insync.ticker import Ticker

@dataclass
class Asset:
    ticker: Ticker = None
    bars_5s: BarDataList = None
    bars_1m: BarDataList = None
    bars_1h: BarDataList = None
    bars_4h: BarDataList  = None
    bars_1d: BarDataList = None