import os
import csv
import time
import winreg as reg

def get_usb_history():
    path = r'SYSTEM\ControlSet001\Enum\USBSTOR'
    key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, path)

    devices = []
    try:
        for i in range(10000):
            device_key_name = reg.EnumKey(key, i)
            device_key = reg.OpenKey(key, device_key_name)
            try:
                for j in range(10000):
                    serial_number = reg.EnumKey(device_key, j)
                    serial_key = reg.OpenKey(device_key, serial_number)
                    
                    try:
                        model = reg.QueryValueEx(serial_key, 'DeviceDesc')[0]
                        hardware_id = reg.QueryValueEx(serial_key, 'HardwareID')[0]
                        friendly_name = reg.QueryValueEx(serial_key, 'FriendlyName')[0]
                        timestamp = reg.QueryInfoKey(serial_key)[2]
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp / 1e7 - 11644473600))
                        devices.append((timestamp, friendly_name, serial_number, model, hardware_id))
                    except FileNotFoundError:
                        pass
            except OSError:
                pass
    except OSError:
        pass

    return devices

def write_to_csv(devices):
    with open('usb_history.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Last Connected', 'Friendly Name', 'Serial Number', 'Model', 'Hardware ID'])
        writer.writerows(devices)
        print(devices)

devices = get_usb_history()
write_to_csv(devices)
