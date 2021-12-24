try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract
import cv2
import pandas as pd

def value_to_float(x):
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

    return 0.0

tickers = []
prices = []
changes = []
volumes = []
floats = []

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image = cv2.imread(r'test.png')

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

data = pytesseract.image_to_string(threshold_img, lang='eng',config='--psm 6')

lines = data.split("\n")

df = pd.DataFrame()

for line in lines:

    ticker = line.split()[0]
    price = line.split()[1]
    change = line.split()[2]

    volume = line.split()[3]

    volume = value_to_float(volume)

    stock_float = line.split()[4]
    stock_float = value_to_float(stock_float)

    tickers.append(ticker)
    prices.append(price)
    changes.append(change)
    volumes.append(volume)
    floats.append(stock_float)

df['Ticker'] = tickers
df['Price'] = prices
df['Change'] = changes
df['Volume'] = volumes
df['Float'] = floats

print(df)



