import time
from ib_insync.contract import Stock
from ib_insync.ib import IB
from datetime import datetime
from ib_insync import Order
import pandas as pd
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

purchased = False

qty = 1
ib.sleep(1)

# Fetching historical data when market is closed for testing purposes
market_data = pd.DataFrame(
    ib.reqHistoricalData(
        SPY,
        endDateTime='',
        durationStr='1 D',
        barSizeSetting='1 min',
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

print("last close: ", last_close)

## STARTING THE ALGORITHM ##
# Time frame: 6.30 hrs
StartTime = pd.to_datetime("9:30").tz_localize('America/New_York')
TimeNow = pd.to_datetime(ib.reqCurrentTime()).tz_convert('America/New_York')
EndTime = pd.to_datetime("16:30").tz_localize('America/New_York')

# Waiting for Market to Open
if StartTime > TimeNow:
    wait = (StartTime - TimeNow).total_seconds()
    print("Waiting for Market to Open..")
    print(f"Sleeping for {wait} seconds")
    time.sleep(wait)
    time.sleep(3 * 60)

# Run the algorithm till the daily time frame exhausts:
while TimeNow <= EndTime:
    try:
        print("Looking for an opportunity!")

        [SPY_close] = ib.reqTickers(SPY)

        Current_SPY_Value = SPY_close.marketPrice()

        print(low_value, high_value, Current_SPY_Value)

        if Current_SPY_Value > high_value and purchased == False:

            [UPRO_close] = ib.reqTickers(UPRO)
            print("ticker: ", UPRO)
            Current_UPRO_Value = UPRO_close.marketPrice()

            order = Order(orderId=2, action='Buy', orderType='LIMIT', lmtPrice=Current_UPRO_Value,
                          totalQuantity=200)

            ib.placeOrder(UPRO, order)

            time.sleep(10)

            order = Order(orderId=3, action='Sell', orderType='TRAIL',
                          trailingPercent=0.5, totalQuantity=200)

            ib.placeOrder(UPRO, order)

            purchased = True

            print('Bought UPRO!')

            ib.disconnect()

        elif Current_SPY_Value < low_value and purchased == False:

            [SPXU_close] = ib.reqTickers(SPXU)
            print("ticker: ", SPXU)
            Current_SPXU_Value = SPXU_close.marketPrice()

            order = Order(orderId=4, action='Buy', orderType='LIMIT', lmtPrice=Current_SPXU_Value,
                          totalQuantity=200)

            ib.placeOrder(SPXU, order)

            time.sleep(10)

            order = Order(orderId=5, action='Sell', orderType='TRAIL',
                          trailingPercent=0.5, totalQuantity=200)

            ib.placeOrder(SPXU, order)

            purchased = True

            print('Bought SPXU!')

            ib.disconnect()

        time.sleep(60)


    except Exception as err:
        print(err)


# **The ability to kill the trade while the market is trading
# master square off or square off in IB
# ib.cancelOrder()

# on bash file close:
# ib.reqGlobalCancel()