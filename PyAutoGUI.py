import pyautogui
import time

def open_browser():

    pyautogui.moveTo(510, 1057) # Move the mouse to XY coordinates.
    pyautogui.click()

    pyautogui.moveTo(678, 62, duration=2)
    pyautogui.click()

    pyautogui.write('reddit.com', interval=0.15)
    pyautogui.press('enter')


def screenshot_bluestacks():
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

    time.sleep(10)

    im = pyautogui.screenshot(region=(370, 339, 1420, 575))

    im.save('test.png')



screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.
print(screenWidth, screenHeight)

# time.sleep(5)

currentMouseX, currentMouseY = pyautogui.position() # Get the XY coordinates of the mouse.
print(currentMouseX, currentMouseY)

screenshot_bluestacks()
