# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 13:02:44 2024

@author: nannib
"""
import os
import subprocess
import re
import csv
import time

# Inizializza le variabili
friendly_name = ''
serial_number = ''
model = ''
lctimestamp = ''

def convert_filetime(match_timestamp):
    # Inverti l'ordine dei byte
    reversed_hex_filetime = "".join(reversed([match_timestamp[i:i+2] for i in range(0, len(match_timestamp), 2)]))

    # Converti in un numero intero
    filetime = int(reversed_hex_filetime, 16)

    local_date= time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(filetime / 1e7 - 11644473600))

    return local_date

csv_filename="usb_history.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

# Ottieni il percorso del file Python
python_file_path = os.path.dirname(os.path.abspath(__file__))
timestamp_file = time.strftime("%Y%m%d%H%M%S")
usbstor_txt_path = os.path.join(python_file_path, f'usbstor_{timestamp_file}.txt')

# Esegui il comando esterno per esportare il registro
result = subprocess.run(f'nircmd.exe elevatecmd runassystem reg export "HKLM\\SYSTEM\\ControlSet001\\Enum\\USBSTOR" {usbstor_txt_path}', shell=True)

if result.returncode != 0:
    print('Errore durante l\'esecuzione del comando:')
    print(result.stderr.decode('utf-8'))

# Inizializza le variabili
usb_entries = []
time.sleep(2)
# Leggi il file usbstor.txt
with open(usbstor_txt_path, 'r', encoding='utf-16') as file:
    content = file.read()

# Utilizziamo espressioni regolari per estrarre le informazioni USB
matches = re.finditer(r'"FriendlyName"="([^"]+)"|\\0066\]\n@=hex\(ffff0010\):([0-9a-fA-F,]+)|\\USBSTOR\\([^\\]+)\\([^\\]+)\]', content)

# Itera su tutte le corrispondenze trovate
for match in matches:
    if match.group(4):
        serial_number = match.group(4)
        #print(serial_number)
        model=match.group(3)
        #print(model,"*****")
    elif match.group(2):
         timestamp = match.group(2).replace(',', '')
         lctimestamp = convert_filetime(timestamp)
         #print(lctimestamp)
    elif match.group(1):
         friendly_name=match.group(1)
         #print(friendly_name)
         

    if friendly_name and serial_number and model and lctimestamp:
        # Aggiungi le informazioni USB a usb_entries
        usb_entries.append({'Last Connected': lctimestamp, 'Friendly Name': friendly_name, 'Serial Number': serial_number, 'Model': model})
        friendly_name = ''
        serial_number = ''
        model = ''
        lctimestamp = ''
    #print(usb_entries,"*******")
# Stampa e scrivi nel file CSV per tutte le corrispondenze
for entry in usb_entries:
    print('Friendly Name:', entry['Friendly Name'])
    print('Serial Number:', entry['Serial Number'])
    print('Model:', entry['Model'])
    print('Timestamp:', entry['Last Connected'])
    
    # Crea o aggiungi una nuova riga nel file CSV
    with open(csv_filename, 'a', newline='') as csv_file:
        fieldnames = ['Last Connected', 'Friendly Name', 'Serial Number', 'Model']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Se il file è vuoto, scrivi l'header
        if os.path.getsize(csv_filename) == 0:
            writer.writeheader()

        # Scrivi una nuova riga nel file CSV
        writer.writerow(entry)

