import pyautogui
import time

class PyAutoGUI_Driver():

    def open_browser(self):

        pyautogui.moveTo(510, 1057) # Move the mouse to XY coordinates.
        pyautogui.click()

        pyautogui.moveTo(678, 62, duration=2)
        pyautogui.click()

        pyautogui.write('reddit.com', interval=0.15)
        pyautogui.press('enter')


    def screenshot_bluestacks(self):
        pyautogui.moveTo(190, 1067)  # Move the mouse to XY coordinates.
        pyautogui.click(duration=2)

        pyautogui.write('realtimestockscreener', interval=0.15)

        time.sleep(5)

        pyautogui.moveTo(246, 556, duration=2)  # Move the mouse to XY coordinates.

        pyautogui.click()

        time.sleep(18)

        # change = pyautogui.locateOnScreen('volume.png')

        pyautogui.moveTo(1368, 310, duration=2)

        pyautogui.click()

        time.sleep(15)

        im = pyautogui.screenshot(region=(370, 289, 1420, 575))

        im.save('test.png')
