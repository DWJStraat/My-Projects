import bluetooth
import time
import json
import win32api

def on_exit(sig, func=None):
    with open("w", "devices.json") as f:
        json.dump(devices, f)
    print('Saved to file')
    time.sleep(10)

file = open("devices.json", "r")
win32api.SetConsoleCtrlHandler(on_exit, True)
devices = json.load(file)
while True:
    nearby_devices = bluetooth.discover_devices(lookup_names = True)
    print(f"Found {len(nearby_devices)} devices")
    timestamp = time.strftime("%H:%M:%S")
    for addr, name in nearby_devices:
        if addr not in devices:
            devices[addr] = []
        if name not in devices[addr]:
            devices[addr].append(name)
        devices[addr].append(timestamp)
    time.sleep(5)




