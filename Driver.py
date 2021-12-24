import PyAutoGUI
import Tesseract
import Premarket

pyAuto = PyAutoGUI.PyAutoGUI_Driver()
tesseract = Tesseract.Tesseract_Driver()
premarket = Premarket.Premarket_Driver()

# tess

pyAuto.screenshot_bluestacks()
df = tesseract.return_df()

print(df)

premarket.loop_through_yfinance()

