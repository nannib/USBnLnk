import os
import csv
from pylnk3 import parse
from datetime import datetime


def format_with_tenths(dt):
    # Arrotonda i microsecondi a un decimo di secondo
    tenths = round(dt.microsecond / 100000, 1)
    return dt.strftime("%Y-%m-%d %H:%M:%S.") + str(tenths)[2:]

def parse_lnk_time(lnk_time):
    # Converte la stringa nel formato datetime
    return datetime.strptime(lnk_time, "%Y-%m-%d %H:%M:%S.%f")

def parse_lnk_file(lnk_filepath):
    try:
        with open(lnk_filepath, 'rb') as lnk_file:
            lnk_info = str(parse(lnk_file))  # Converti l'oggetto parse a stringa
            
            # Estrai i campi desiderati dalla stringa lnk_info
            volume_type = get_field_value(lnk_info, 'Volume Type')
            volume_serial_number = get_field_value(lnk_info, 'Volume Serial Number')
            #print("****************************",volume_type)
            # Verifica se il file LNK ha solo il campo Volume Type
            if volume_type.__contains__("'archive':"):
                access_time=''
                # Estrai informazioni specifiche per questo tipo di file LNK
                creation_time = get_field_value(lnk_info, 'Creation Time')
                modification_time = get_field_value(lnk_info, 'Modification Time')
                # Ottieni la data corrente nel formato desiderato
                current_time = datetime.now()
                formatted_time = format_with_tenths(current_time)
                access_time = get_field_value(lnk_info, 'Access Time')
                
                if format_with_tenths(parse_lnk_time(access_time)) == formatted_time:
                    access_time="1970-01-01 00:00:00.000000"
                    creation_time="1970-01-01 00:00:00.000000"
                    modification_time="1970-01-01 00:00:00.000000"
                
                used_path = get_field_value(lnk_info, 'Used Path')
                if not "%INTERNET" in used_path and not "%UNKNOWN" in used_path:
                    network_share = get_field_value(lnk_info, 'Network Share')
                    base_name = get_field_value(lnk_info, 'Base Name')
                else:
                    network_share=" "
                    base_name = " "
                #print("****************************",lnk_info)
                # Stampa a schermo
                print("Used Path:", used_path)
                print("Network Share:", network_share)
                print("Base Name:", base_name)
                print("Creation Time:", creation_time)
                print("Modification Time:", modification_time)
                print("Access Time:", access_time)
                

                # Scrivi nel file CSV
                write_to_csv(lnk_filepath, network_share, base_name, used_path, creation_time, modification_time, access_time)

            else:
                # Estrai i campi standard
                volume_serial_number = hex(int(get_field_value(lnk_info, 'Volume Serial Number')))[2:]
                path = get_field_value(lnk_info, 'Path')
                current_time = datetime.now()
                formatted_time = format_with_tenths(current_time)
                creation_time = get_field_value(lnk_info, 'Creation Time')
                modification_time = get_field_value(lnk_info, 'Modification Time')
                access_time = get_field_value(lnk_info, 'Access Time')
                if format_with_tenths(parse_lnk_time(access_time)) == formatted_time:
                    access_time="1970-01-01 00:00:00.000000"
                    creation_time="1970-01-01 00:00:00.000000"
                    modification_time="1970-01-01 00:00:00.000000"
                

                # Stampa a schermo
                """print("Volume Type:", volume_type)
                print("Volume Serial Number:", volume_serial_number)
                print("Path:", path)
                print("Creation Time:", creation_time)
                print("Modification Time:", modification_time)
                print("Access Time:", access_time)"""

                # Scrivi nel file CSV
                write_to_csv(lnk_filepath, volume_type, volume_serial_number, path, creation_time, modification_time, access_time)

    except Exception as e:
        print(f"Errore nel leggere il file LNK '{lnk_filepath}': {e}")

def get_field_value(lnk_info, field):
    start_index = lnk_info.find(f"{field}:")
    end_index = lnk_info.find('\n', start_index)
    value = lnk_info[start_index + len(field) + 2:end_index].strip()
    return value

def write_to_csv(lnk_filepath, volume_type, volume_serial_number, user_path, creation_time, modification_time, access_time):
    csv_filename = 'lnk_info.csv'

    # Scrivi le informazioni nel file CSV
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Scrivi le intestazioni una sola volta
        if csvfile.tell() == 0:
            csv_writer.writerow(["File LNK", "Volume Type", "Volume Serial Number", "User Path", "Creation Time", "Modification Time", "Access Time"])

        # Scrivi i valori sotto le rispettive intestazioni
        csv_writer.writerow([lnk_filepath, volume_type, volume_serial_number, user_path, creation_time, modification_time, access_time])
        csv_writer.writerow([])  # Aggiungi una riga vuota tra le informazioni di diversi file LNK

def read_recent_folder():
    recent_path = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Recent')

    for root, dirs, files in os.walk(recent_path):
        for file in files:
            if file.lower().endswith('.lnk'):
                lnk_filepath = os.path.join(root, file)
                parse_lnk_file(lnk_filepath)

if __name__ == "__main__":
    csv_filename = 'lnk_info.csv'
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
    read_recent_folder()



