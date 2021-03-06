try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract
import cv2
import pandas as pd

class Tesseract_Driver():

    def get_percent(self, first, second):

        if first == 0 or second == 0:
            return 0
        else:
            percent = first / second * 100
        return percent

    def value_to_float(self, x):
        try:
            if type(x) == float or type(x) == int:
                return x
            if 'K' in x:
                if len(x) > 1:
                    return float(x.replace('K', '')) * 1000
                return 1000.0
            if 'M' in x:
                if len(x) > 1:
                    return float(x.replace('M', '')) * 1000000
                return 1000000.0
            if 'B' in x:
                if len(x) > 1:
                    return float(x.replace('B', '')) * 1000000000
                return 1000000000.0
            if 'T' in x:
                if len(x) > 1:
                    return float(x.replace('T', '')) * 1000000000000
                return 1000000000000000.0
        except Exception as err:
            print(err)
            return 0

        return 0.0

    def return_df(self):

        tickers = []
        prices = []
        changes = []
        volumes = []
        floats = []
        volume_float_ratios = []

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        image = cv2.imread(r'test.png')

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        data = pytesseract.image_to_string(threshold_img, lang='eng', config='--psm 6')

        lines = data.split("\n")
        lines.pop(0)

        df = pd.DataFrame()

        for line in lines:

            ticker = line.split()[0]
            price = line.split()[1]
            change = line.split()[2]

            volume = line.split()[3]

            volume = self.value_to_float(volume)

            stock_float = line.split()[4]
            stock_float = self.value_to_float(stock_float)

            volume_float_ratio = self.get_percent(volume, stock_float)

            tickers.append(ticker)
            prices.append(price)
            changes.append(change)
            volumes.append(volume)
            floats.append(stock_float)
            volume_float_ratios.append(volume_float_ratio)

        df['Ticker'] = tickers
        df['Price'] = prices
        df['Change'] = changes
        df['Volume'] = volumes
        df['Float'] = floats
        df['V/F Ratio'] = volume_float_ratios

        df = df[df['Float'].astype(float) < 25000000]
        df = df[df['V/F Ratio'].astype(float) >= 10]
        df = df[df['Change'].astype(float) > 0]

        return df




