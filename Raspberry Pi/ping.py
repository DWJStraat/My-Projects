import requests
from time import sleep
from win10toast import ToastNotifier

def ping(ip):
    try:
        r = requests.get(ip)
        return r.status_code
    except:
        return -1

ip = 'raspberrypi.local'
pinging = True
while pinging:
    if ping(ip) == 200:
        pinging = False
        print('Raspberry Pi is online')
        toaster = ToastNotifier()
        toaster.show_toast('Raspberry Pi', 'Raspberry Pi is online', icon_path='raspberry.ico')
    else:
        print('Raspberry Pi is offline')
        sleep(30)