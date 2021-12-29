import PyAutoGUI
import Tesseract
import GapUpScalper
import pandas as pd

pyAuto = PyAutoGUI.PyAutoGUI_Driver()
tesseract = Tesseract.Tesseract_Driver()
scalper = GapUpScalper.GapUpScalper_Driver()

# tess

def kill_bluestacks():
    import psutil

    PROCNAME = "BlueStacks.exe"

    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()

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

scalper.start_scalping(df)

print(df)
