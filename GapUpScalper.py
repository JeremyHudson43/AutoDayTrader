import time
from ib_insync.contract import Index, Option, Stock
from ib_insync.ib import IB
from datetime import datetime
import pandas as pd
from ib_insync import Order
import random


# Logging into Interactive Broker TWS
ib = IB()
# port for IB gateway : 4002
# port for IB TWS : 7497
ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

# To get the current market value, first create a contract for the underlyer,
# we are selecting Tesla for now with SMART exchanges:
SPY = Stock('SPY', 'SMART', 'USD')

UPRO = Stock('UPRO', 'SMART', 'USD')
SPXU = Stock('SPXU', 'SMART', 'USD')

# check like 5 stocks at once

# if one of them has crossed premarket highs, pick that one

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

# Fetching historical data when market is closed for testing purposes
market_data = pd.DataFrame(
    ib.reqHistoricalData(
        SPY,
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
low_value = min(premarket_data['low'].to_list())

print(low_value, high_value)

print("Market data: ", market_data)

# last candle close, 4EMA and 55EMA values:
last_close = market_data['close'].iloc[-1]


print("Trading started!")

[SPY_close] = ib.reqTickers(SPY)

order = Order(orderId = 2, action = 'Buy', orderType = 'LIMIT', lmtPrice= last_close ,
           totalQuantity = 200)

ib.placeOrder(SPY, order)

time.sleep(10)

order = Order(orderId = 3, action = 'Sell', orderType = 'TRAIL',
              trailingPercent = 1.0, totalQuantity = 200)

ib.placeOrder(SPY, order)



