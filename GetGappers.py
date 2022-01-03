from ib_insync.contract import Stock
from ib_insync.ib import IB, ScannerSubscription
import pandas as pd
import random
from bs4 import BeautifulSoup

class GetGapper_Driver():

    def get_percent(self, first, second):
        if first == 0 or second == 0:
            return 0
        else:
            percent = first / second * 100
        return percent

    def get_gappers(self):

        tickers = []
        prices = []
        volumes = []
        floats = []
        volume_float_ratios = []


        ib = IB()

        ib.connect('127.0.0.1', 7497, clientId=random.randint(0, 300))

        topPercentGainerListed = ScannerSubscription(instrument='STK', locationCode='STK.US.MAJOR', scanCode='TOP_PERC_GAIN', belowPrice=20, abovePrice=0.01, aboveVolume=500000)

        # topPercentGainerListed = ScannerSubscription(instrument='STK', locationCode='STK.US.MAJOR', scanCode='HOT_BY_VOLUME', belowPrice=20, abovePrice=0.01, aboveVolume=50000000)

        scanner = ib.reqScannerData(topPercentGainerListed, [])

        df = pd.DataFrame()

        # loop through the scanner results and get the contract details
        for stock in scanner[:10]:

            try:
                security = Stock(stock.contractDetails.contract.symbol,

                                 stock.contractDetails.contract.exchange,
                                 stock.contractDetails.contract.currency)

                # request the fundamentals
                fundamentals = ib.reqFundamentalData(security, 'ReportSnapshot')

                soup = BeautifulSoup(str(fundamentals), 'xml')

                shares = soup.find('SharesOut').text
                shares = float(shares)

                price = float(soup.find('Ratio').text)

                # Fetching historical data when market is closed for testing purposes
                premarket_data = pd.DataFrame(
                    ib.reqHistoricalData(
                        security,
                        endDateTime='09:29:00',
                        durationStr='1 D',
                        barSizeSetting='1 min',
                        whatToShow="TRADES",
                        useRTH=False,
                        formatDate=1
                    ))

                volume = sum(premarket_data['volume'].tolist()) * 100
                ratio = self.get_percent(volume, shares)

                if ratio > 20 and volume > 150000 and shares < 25000000 and price < 20:
                    print('Ticker', security.symbol)
                    print('Price', price)
                    print("Shares Outstanding", shares)
                    print("Volume", volume)
                    print('Premarket Volume is', ratio, '% of Shares Outstanding\n')

                    tickers.append(security.symbol)
                    prices.append(price)
                    volumes.append(volume)
                    floats.append(shares)
                    volume_float_ratios.append(ratio)

                    df['Ticker'] = tickers
                    df['Price'] = prices
                    df['Volume'] = volumes
                    df['Float'] = floats
                    df['V/F Ratio'] = volume_float_ratios

                print(df)

                return df

            except Exception as err:
                print(err)