import SimpleGapUpScalper
import GetGappers
import pandas as pd
import multiprocessing
import time
from datetime import datetime
import gc
import sys

scalper = SimpleGapUpScalper.GapUpScalper_Driver()
get_gappers_class = GetGappers.GetGapper_Driver()


def check_stock(stock_name, final_stock_selected, premarket_high):
    ## STARTING THE ALGORITHM ##
    # Time frame: 6.30 hrs

    stock_brokeout = False

    now = str(datetime.now().time())  # time object

    StartTime = pd.to_datetime("9:30").tz_localize('America/New_York')
    TimeNow = pd.to_datetime(now).tz_localize('America/New_York')
    EndTime = pd.to_datetime("16:30").tz_localize('America/New_York')

    time_until_market_close = (EndTime - TimeNow).total_seconds()

    # Waiting for Market to Open
    if StartTime > TimeNow:
        wait = (StartTime - TimeNow).total_seconds()
        print("Waiting for Market to Open..")
        print(f"Sleeping for {wait} seconds")
        time.sleep(wait)

    # Run the algorithm till the daily time frame exhausts:
    while TimeNow <= EndTime:

        # loop through all ticker / high values
        if not final_stock_selected:
            stock_brokeout, ticker = scalper.check_for_breakout(stock_name, premarket_high)

        if stock_brokeout and not final_stock_selected:
            scalper.buy_stock(ticker, premarket_high)
            final_stock_selected = True

            return final_stock_selected

            time.sleep(time_until_market_close - 300)

        try:
            # sell if you've bought already and haven't sold 5 minutes before close
            if time_until_market_close < 300 and final_stock_selected:
                scalper.sell_stock(ticker)
                sys.exit(0)
        except Exception as err:
            print(err)


def generate_gapper_CSV():

    today = datetime.today().strftime('%Y-%m-%d')

    filepath = 'C:\\Users\\Frank Einstein\\PycharmProjects\\AutoDaytrader\\gapper_records\\gappers_' + today + '.csv'

    df = get_gappers_class.get_gappers()
    df.to_csv(filepath)

    return df


if __name__ == "__main__":

    now = str(datetime.now().time())  # time object

    StartTime = pd.to_datetime("9:30").tz_localize('America/New_York')
    TimeNow = pd.to_datetime(now).tz_localize('America/New_York')
    EndTime = pd.to_datetime("16:30").tz_localize('America/New_York')

    time_until_market_close = (EndTime - TimeNow).total_seconds()

    # Waiting for Market to Open
    if StartTime > TimeNow:
        wait = (StartTime - TimeNow).total_seconds()
        print("Waiting for Market to Open..")
        print(f"Sleeping for {wait} seconds")
        time.sleep(wait)

    df = generate_gapper_CSV()

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    tickers = df['Ticker'].to_list()
    premarket_highs = df['Premarket_High'].to_list()

    print(tickers)

    count = 0
    final_stock_selected = False

    while not final_stock_selected:
        # gc.collect()
        try:
            if count < len(tickers):
                count = count + 1
                final_stock_selected = check_stock(tickers[count - 1], premarket_highs[count - 1], final_stock_selected)
                print(count)

            elif count >= len(tickers):
                count = 0
        except Exception as err:
                print(err)
