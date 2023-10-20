import pyautogui as pg
import time
import webbrowser

def make_call(number='+18005284800'):
    def open_website(url):
        webbrowser.open(url, new=2)  # new=2 opens in a new tab, if possible

    website = 'https://dialer.callhippo.com/dial'
    open_website(website)

    time.sleep(15)

    pg.click(977, 316) ## cick on dialer pad
    pg.press('backspace')
    pg.press('backspace')
    pg.press('backspace')
    pg.write(number)
    print("Number typed")
    time.sleep(2)
    pg.press('enter')
    print('calling', {number})
    time.sleep(2)
