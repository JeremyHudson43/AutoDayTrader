import PyAutoGUI
import Tesseract
import SimpleGapUpScalper
import pandas as pd
import multiprocessing
import time
from datetime import datetime

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

    now = datetime.now().time()  # time object

    StartTime = pd.to_datetime("9:30").tz_localize('America/New_York')
    TimeNow = pd.to_datetime(now).tz_convert('America/New_York')
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
        # loop through all ticker / high values
        ticker, premarket_high = scalper.get_premarket_highs(stock_name)
        ticker = scalper.check_for_breakout(ticker, premarket_high)

        # scalper.check_for_second_support_touch(ticker, premarket_high)
        # scalper.check_for_final_breakout(ticker, premarket_high)

        scalper.buy_stock(ticker)


def generate_gapper_CSV():
    try:
        pyAuto.screenshot_bluestacks()
        df = tesseract.return_df()
        df.to_csv('gappers.csv')
    except Exception as err:
        kill_bluestacks()
        pyAuto.screenshot_bluestacks()
        df = tesseract.return_df()
        df.to_csv('gappers.csv')


if __name__ == "__main__":

    generate_gapper_CSV()

    df = pd.read_csv('gappers.csv')

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    tickers = df['Ticker'].to_list()

    pool = multiprocessing.Pool(len(tickers))
    pool.map(check_stock, tickers)

    print(df)
