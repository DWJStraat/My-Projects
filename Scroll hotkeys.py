# I made this script when my mouse was dead.

import pyautogui
import win10toast
from pynput import keyboard

def scroll_up():
    print('up')
    pyautogui.scroll(100)

def scroll_down():
    print('down')
    pyautogui.scroll(-100)

def main():
    win10toast.ToastNotifier().show_toast("Hotkeys", "Hotkeys are now active", duration=5)
    with keyboard.GlobalHotKeys(
        {
            '<ctrl>+<shift>+<up>': scroll_up,
            '<ctrl>+<shift>+<down>': scroll_down
        }
    ) as h:
        h.join()

main()



