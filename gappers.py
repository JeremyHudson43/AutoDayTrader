from ib_insync.contract import Stock
from ib_insync.ib import IB, ScannerSubscription, TagValue
import pandas as pd
import random
from bs4 import BeautifulSoup


def get_percent(first, second):
    if first == 0 or second == 0:
        return 0
    else:
        percent = first / second * 100
    return percent


def get_gappers():

    tickers = []
    prices = []
    volumes = []
    floats = []
    volume_float_ratios = []

    ib = IB()

    ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

    sub = ScannerSubscription(
        instrument='STK',
        locationCode='STK.US.MAJOR',
        scanCode='TOP_PERC_GAIN')

    tagValues = [
        TagValue("changePercAbove", "10"),
        TagValue('priceAbove', 5),
        TagValue('priceBelow', 50)]

    # the tagValues are given as 3rd argument; the 2nd argument must always be an empty list
    # (IB has not documented the 2nd argument and it's not clear what it does)
    scanData = ib.reqScannerData(sub, [], tagValues)

    symbols = [sd.contractDetails.contract.symbol for sd in scanData]
    print(symbols)

get_gappers()