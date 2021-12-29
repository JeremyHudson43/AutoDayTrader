import PyAutoGUI
import Tesseract
import GapUpScalper
import pandas as pd
import multiprocessing

pyAuto = PyAutoGUI.PyAutoGUI_Driver()
tesseract = Tesseract.Tesseract_Driver()
scalper = GapUpScalper.GapUpScalper_Driver()


def kill_bluestacks():
    import psutil

    PROCNAME = "BlueStacks.exe"

    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()


def check_stock(stock_name):
    # loop through all ticker / high values
    ticker, premarket_high = scalper.get_premarket_highs(stock_name)
    scalper.check_for_breakout(ticker, premarket_high)

    scalper.check_for_second_support_touch(ticker, premarket_high)
    scalper.check_for_final_breakout(ticker, premarket_high)

    scalper.buy_stock(ticker)

# try:
# pyAuto.screenshot_bluestacks()
# df = tesseract.return_df()
# df.to_csv('gappers.csv')
# except Exception as err:
# kill_bluestacks()
# pyAuto.screenshot_bluestacks()

# df = tesseract.return_df()
# df.to_csv('gappers.csv')

df = pd.read_csv('gappers.csv')

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
tickers = df['Ticker'].to_list()

if __name__ == "__main__":
    pool = multiprocessing.Pool(len(tickers))
    pool.map(check_stock, tickers)

    print(df)
