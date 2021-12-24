import yfinance as yf
import time

class Premarket_Driver():

        def loop_through_yfinance(self):
                counter = 0

                while True:

                        counter = counter + 1

                        data = yf.download(
                                tickers = "XXII",
                                period = "1d",
                                interval = "1m",
                                auto_adjust = True,
                                prepost = True,
                                threads = True,
                                proxy = None
                            )

                        data.to_csv('data_' + str(counter) + '.csv')

                        time.sleep(300)
