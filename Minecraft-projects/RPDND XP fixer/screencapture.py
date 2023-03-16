import numpy as np
import re
import pytesseract
import requests
import cv2
import time
from PIL import ImageGrab
import json
from win10toast import ToastNotifier

toaster = ToastNotifier()
def imToString():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
    test = pytesseract.image_to_string(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR), lang='eng')
    UUIDs = re.findall('UUID:.*', test)
    toaster.show_toast("UUIDs found", f"{len(UUIDs)} UUIDs found", duration=10)
    for i in UUIDs:
        uuid = i.split(': ')[1]
        uuid = uuid.replace('-', '')
        print(uuid)
        try:
            r = requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}')
            print(r.json())
            print(r.json()['name'])
        except KeyError:
            toaster.show_toast("Can't find user", f"Can't find user with UUID {uuid}", duration=10)


time.sleep(10)
imToString()