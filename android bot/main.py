import PIL
import pytesseract
from ppadb.client import Client as AdbClient
import progress



def connect():
    adb = AdbClient(
        host='127.0.0.1',
        port=5037
    )
    devices = adb.devices()
    if len(devices) == 0:
        print('No devices')
    else:
        return devices[0]

def screenshot(device):
    image = device.screencap()
    with open('screenshot.png', 'wb') as f:
        f.write(image)

print('running')
device = connect()
print('connected')
screenshot(device)
print('done')