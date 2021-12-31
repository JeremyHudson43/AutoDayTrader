import PyAutoGUI
import Tesseract
import SimpleGapUpScalper
import pandas as pd
import multiprocessing
import time
from datetime import datetime
import gc
import sys

pyAuto = PyAutoGUI.PyAutoGUI_Driver()
tesseract = Tesseract.Tesseract_Driver()
scalper = SimpleGapUpScalper.GapUpScalper_Driver()


def kill_bluestacks():
    import psutil

    PROCNAME = "BlueStacks.exe"

    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()



def check_stock(stock_name):

    ## STARTING THE ALGORITHM ##
    # Time frame: 6.30 hrs

    now = str(datetime.now().time())  # time object

    StartTime = pd.to_datetime("9:30").tz_localize('America/New_York')
    TimeNow = pd.to_datetime(now).tz_localize('America/New_York')
    EndTime = pd.to_datetime("16:30").tz_localize('America/New_York')

    # Waiting for Market to Open
    if StartTime > TimeNow:
        wait = (StartTime - TimeNow).total_seconds()
        print("Waiting for Market to Open..")
        print(f"Sleeping for {wait} seconds")
        time.sleep(wait)

    # Run the algorithm till the daily time frame exhausts:
    while TimeNow <= EndTime:

        # TODO:
        # until you can get around PDT rule, select the first stock that breaks the PM high and disregard the rest
        # add logic to sell if you've bought already and haven't sold 5 minutes before close
        # add logic to cancel all orders if the price drops 1% below the premarket high then sell immediately

        # loop through all ticker / high values
        ticker, premarket_high = scalper.get_premarket_highs(stock_name)
        ticker = scalper.check_for_breakout(ticker, premarket_high)

        # scalper.check_for_second_support_touch(ticker, premarket_high)
        # scalper.check_for_final_breakout(ticker, premarket_high)

        scalper.buy_stock(ticker)


def generate_gapper_CSV():

    # pyAuto.screenshot_bluestacks()
    df = tesseract.return_df()
    df.to_csv('gappers.csv')


if __name__ == "__main__":

    generate_gapper_CSV()

    df = pd.read_csv('gappers.csv')

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    tickers = df['Ticker'].to_list()

    count = 0

    while 1:
        # gc.collect()
       #  try:
        if count < len(tickers):
            count = count + 1
            check_stock(tickers[count - 1])
            print(count)

        elif count >= len(tickers):
            count = 0
        # except Exception as err:
           #  print(err)

