# USBnLnk
This program can correlate the dates of USB mass device connections with recent files and  export a report in CSV format

It runs on Windows 8,10,11

**How to RUN**

pip install -r requirements.txt

python main.py

it creates the report and the two CSV files (list of usb devices and list of recent files) in the same directory of the program.

You can create an **EXEcutable** file for Windows using this command::

 **pyinstaller --hidden-import babel.numbers --onefile main.py**

![image](https://github.com/nannib/USBnLnk/assets/12171140/ba5be7c9-4a62-4b2e-985f-5f37bf5fc3e0)
