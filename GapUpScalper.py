import time
from ib_insync.contract import Index, Option, Stock
from ib_insync.ib import IB
from datetime import datetime
import pandas as pd
from ib_insync import Order
import random

ticker_dict = {}


# Logging into Interactive Broker TWS
ib = IB()

class GapUpScalper_Driver():

    def get_premarket_highs(self, ticker):
            ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

            ticker = Stock(ticker, 'SMART', 'USD')

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

            # fetch premarket high and add ticker / high to dictionary
            start = datetime.strptime('04:00:00', '%H:%M:%S').time()
            end = datetime.strptime('09:29:00', '%H:%M:%S').time()

            premarket_data = market_data[market_data['date'].dt.time.between(start, end)]

            high_value = max(premarket_data['high'].to_list())

            ticker_dict[ticker.symbol] = high_value

            return ticker.symbol, high_value

    def check_for_breakout(self, ticker, high):

        stock_brokeout = False

        while not stock_brokeout:

            time.sleep(60)

            ticker = Stock(ticker, 'SMART', 'USD')

            [ticker] = ib.reqTickers(ticker)

            current_stock_value = ticker.marketPrice()

            # if current stock value is greater than premarket high, add to list of stocks that broke out
            if current_stock_value > high:
                stock_brokeout = True

            time.sleep(600)

        last_10_minutes = pd.DataFrame(
            ib.reqHistoricalData(
                ticker,
                endDateTime='',
                durationStr='600 S',
                barSizeSetting='1 min',
                whatToShow="TRADES",
                useRTH=True,
                formatDate=1,
                keepUpToDate=True
            ))

        # get the highest value of the last 10 minutes
        high_value_last_10_minutes = max(last_10_minutes['high'].to_list())

        return high_value_last_10_minutes


    def check_for_second_support_touch(self, ticker):
        print('hello')

    def check_for_final_breakout(self, ticker):
        print('hello')

    def buy_stock(self, ticker):
        print('hello')





