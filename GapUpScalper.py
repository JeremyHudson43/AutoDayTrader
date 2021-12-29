import time
from ib_insync.contract import Index, Option, Stock
from ib_insync.ib import IB
from datetime import datetime
import pandas as pd
from ib_insync import Order
import random


class GapUpScalper_Driver():

    def start_scalping(self, df):

        count = 0

        final_stock = ""

        final_ticker_list = []
        final_high_list = []

        ticker_dict = {}

        # Logging into Interactive Broker TWS
        ib = IB()
        # port for IB gateway : 4002
        # port for IB TWS : 7497
        ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

        # To get the current market value, first create a contract for the underlyer,
        # we are selecting Tesla for now with SMART exchanges:

        for ticker in df['Ticker'].to_list():
            ticker = Stock(ticker, 'SMART', 'USD')
            final_ticker_list.append(ticker)

        for ticker in final_ticker_list:
            # Fetching historical data when market is closed for testing purposes
            market_data = pd.DataFrame(
                ib.reqHistoricalData(
                    ticker,
                    endDateTime='',
                    durationStr='1 D',
                    barSizeSetting='3 mins',
                    whatToShow="TRADES",
                    useRTH=False,
                    formatDate=1,
                    keepUpToDate=True
                ))

            start = datetime.strptime('04:00:00', '%H:%M:%S').time()
            end = datetime.strptime('09:29:00', '%H:%M:%S').time()

            premarket_data = market_data[market_data['date'].dt.time.between(start, end)]

            high_value = max(premarket_data['high'].to_list())

            final_high_list.append(high_value)

            ticker_dict[ticker.symbol] = high_value

        # check like 5 stocks at once

        # if one of them has crossed premarket highs, pick that one

        for ticker, high in zip(ticker_dict.keys(), ticker_dict.values()):

            ticker = Stock(ticker, 'SMART', 'USD')

            [ticker] = ib.reqTickers(ticker)

            current_stock_value = ticker.marketPrice()

            if current_stock_value > high:
                print(ticker + " selected")
                final_stock = ticker



        # wait 10 minutes

        # take high of the highest candle after the 10 minutes is up

        # wait for another touch of the premarket high

        # once the price breaks the high of the highest candle in that 10 minute period, buy

        # set trailing stop loss

        # ???

        # profit

        purchased = False

        qty = 1
        ib.sleep(1)


