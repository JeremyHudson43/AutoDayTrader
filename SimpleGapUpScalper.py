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

            ticker_obj = Stock(ticker, 'SMART', 'USD')

            [ticker] = ib.reqTickers(ticker_obj)

            current_stock_value = ticker.marketPrice()

            print('\nTicker: ', ticker_obj.symbol)
            print('Current Stock Value: ', current_stock_value)
            print('Premarket High: ', high)

            # if current stock value is greater than premarket high, add to list of stocks that broke out
            if current_stock_value > high:
                return ticker_obj.symbol

            time.sleep(15)

            ib.disconnect()


    def buy_stock(self, ticker):

       ticker_contract = Stock(ticker, 'SMART', 'USD')

       [ticker_close] = ib.reqTickers(ticker_contract)

       print("ticker: ", ticker_close)

       Current_Ticker_Value = ticker_close.marketPrice()

       acc_vals = float([v.value for v in ib.accountValues() if v.tag == 'CashBalance' and v.currency == 'USD'][0])

       qty = acc_vals // (Current_Ticker_Value * 1.01)

       order = Order(orderId=4, action='Buy', orderType='MKT',  totalQuantity=100)

       ib.placeOrder(ticker_contract, order)

       time.sleep(10)

       order = Order(orderId=5, action='Sell', orderType='TRAIL',
                      trailingPercent=2.0, totalQuantity=100)

       ib.placeOrder(ticker_contract, order)

       print('Bought ' + str(ticker) +  "!")

       time.sleep(10)

       ib.disconnect()
