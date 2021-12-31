# get list of all gap ups / stocks that have made huge gains in a day
from ib_insync.ib import IB
import pandas as pd
import random
from ib_insync.contract import Index, Option, Stock
from datetime import datetime
import time
from datetime import date, timedelta

# Logging into Interactive Broker TWS
ib = IB()

ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

content = open("gainers.txt", "r").readlines()
dates = open("dates.txt", "r").readlines()

converted_stocks = []
converted_dates = []

winners = 0
losers = 0
index_count = 0



date_count = 0

for element in content:
    converted_stocks.append(element.strip())

for element in dates:
    converted_dates.append(element.strip())

start_date = date(2021, 1, 1)
end_date = date(2021, 12, 31)    # perhaps date.now()

delta = end_date - start_date   # returns timedelta

for i in range(delta.days + 1):
    try:

        date = start_date + timedelta(days=i)

        if date.weekday() > 4:
            # for date, ticker in zip(converted_dates, converted_stocks):
            # try:

            ticker = Stock('SPY', 'SMART', 'USD')

            # date = datetime.strptime(date, '%m/%d/%Y')

            # Fetching historical data when market is closed for testing purposes
            market_data = pd.DataFrame(
                ib.reqHistoricalData(
                    ticker,
                    endDateTime=date,
                    durationStr='1 D',
                    barSizeSetting='1 min',
                    whatToShow="TRADES",
                    useRTH=False,
                    formatDate=1,
                    keepUpToDate=False
                ))

            # fetch premarket high and add ticker / high to dictionary
            start_pre = datetime.strptime('04:00:00', '%H:%M:%S').time()
            end_pre = datetime.strptime('09:29:00', '%H:%M:%S').time()

            premarket_data = market_data[market_data['date'].dt.time.between(start_pre, end_pre)]

            high_value = premarket_data['high'].max()

            # fetch premarket high and add ticker / high to dictionary
            start_reg = datetime.strptime('09:30:00', '%H:%M:%S').time()
            end_reg = datetime.strptime('16:30:00', '%H:%M:%S').time()

            market_data_reg = market_data[market_data['date'].dt.time.between(start_reg, end_reg)]

            market_data_reg_indices = market_data[market_data['close'] > high_value].index

            index_list = []

            for item in market_data_reg_indices:
                index_count += 1
                if index_count < 10:
                    index_list.append(item)

            print(index_list)
            # market_data_reg = market_data_reg[market_data_reg.index.isin(index_list)]

            # for item

            high_value_reg = market_data_reg['high'].max()

           #  print(market_data_reg )

            if high_value_reg > high_value:
                winners = winners + 1

                print('')

                print('Premarket High')
                print(ticker.symbol, high_value, date)

                print('')

                print('Market Close')
                print(ticker.symbol, high_value_reg, date)

                print()

                print('Winner', winners)

            else:
                print('')

                print('Premarket High')
                print(ticker.symbol, high_value, date)

                print('')

                print('Market Close')
                print(ticker.symbol, high_value_reg, date)

                print()

                losers = losers + 1
                print('Losers', losers)

        # time.sleep(1)
    except Exception as err:
        print(err)


# get statistics of how much higher on average top gainer stocks go after breaking premarket high

# find max average drawdown after breaking premarket high

# find out when drawdowns are most likely to occur
