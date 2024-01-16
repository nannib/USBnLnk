# USBnLnk
This program can correlate the dates of USB mass device connections with recent files and  export a report in CSV format

It runs on Windows 8,10,11 - tested with Python 3.8.6

This program export the Windows key: [HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Enum\USBSTOR]
via NIRCMD.EXE (https://www.nirsoft.net/utils/nircmd.html) nircmd.exe elevatecmd runassystem reg export "HKLM\\SYSTEM\\ControlSet001\\Enum\\USBSTOR" {usbstor_txt_path} to elevate privileges to the SYSTEM user, which is the only one user that can access to the subkey:[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Enum\USBSTOR\<device>\<SerialNumber>\Properties\\{83da6326-97a6-4088-9453-a1923f573b29}\0066] where is the last connection timestamp of the USB MASS DEVICE. (https://www.nirsoft.net/utils/usb_devices_view.html)

NIRCMD LICENSE: This utility is released as freeware. You are allowed to freely distribute this utility via floppy disk, CD-ROM, Internet, or in any other way, as long as you don't charge anything for this. If you distribute this utility, you must include all files in the distribution package, without any modification!

NIRCMD.EXE: SHA256: B994AE5CBFB5AD308656E9A8BF7A4A866FDEB9E23699F89F048D7F92E6BB8577

NIRCMD.ZIP: SHA256: 5071B54669BB1E88422C6C340204B0B3A0FFD07E2AC1D747CCBD1447ABC92948

**How to RUN**

pip install -r requirements.txt

python main.py

it creates the report and the two CSV files (list of usb devices and list of recent files) in the same directory of the program.

You can create an **EXEcutable** file for Windows using this command::

 **pyinstaller --hidden-import babel.numbers --onefile main.py**

![image](https://github.com/nannib/USBnLnk/assets/12171140/287f55b8-b3c1-4729-8c26-09167c2065a8)


