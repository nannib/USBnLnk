# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 12:23:40 2024

@author: nanni bassetti https://nannibassetti.com
"""
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkcalendar import DateEntry
import pandas as pd
import time
import subprocess

class USBQueryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("USB_n_LNK - by Nanni Bassetti - nannibassetti.com")
        # Set the width and height of the window
        self.root.geometry("1200x600")
        # Run external programs
        self.run_external_program(["python", "nb_usb.py"])
        self.run_external_program(["python", "lnkfile.py"])
        # Create Tkinter variables
        self.start_datetime_var = tk.StringVar()
        self.end_datetime_var = tk.StringVar()

        # Create labels and entry fields for dates and times
        tk.Label(root, text="Start Date and Time:").grid(row=0, column=0, padx=10, pady=5)
        self.start_datetime_entry = DateEntry(root, textvariable=self.start_datetime_var, width=17, date_pattern="yyyy-mm-dd")
        self.start_datetime_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="End Date and Time:").grid(row=1, column=0, padx=10, pady=5)
        self.end_datetime_entry = DateEntry(root, textvariable=self.end_datetime_var, width=17, date_pattern="yyyy-mm-dd")
        self.end_datetime_entry.grid(row=1, column=1, padx=5, pady=5)

        # Combobox to select start time (hours and minutes)
        tk.Label(root, text="Start Time:").grid(row=0, column=2, padx=10, pady=5)
        self.start_hour_combobox = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(24)])
        self.start_hour_combobox.grid(row=0, column=3, padx=5, pady=5)
        self.start_hour_combobox.set("00")

        tk.Label(root, text="Start Minutes:").grid(row=0, column=4, padx=10, pady=5)
        self.start_minute_combobox = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(60)])
        self.start_minute_combobox.grid(row=0, column=5, padx=5, pady=5)
        self.start_minute_combobox.set("00")

        # Combobox to select end time (hours and minutes)
        tk.Label(root, text="End Time:").grid(row=1, column=2, padx=10, pady=5)
        self.end_hour_combobox = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(24)])
        self.end_hour_combobox.grid(row=1, column=3, padx=5, pady=5)
        self.end_hour_combobox.set("23")

        tk.Label(root, text="End Minutes:").grid(row=1, column=4, padx=10, pady=5)
        self.end_minute_combobox = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(60)])
        self.end_minute_combobox.grid(row=1, column=5, padx=5, pady=5)
        self.end_minute_combobox.set("59")

        # Button to execute the query
        ttk.Button(root, text="Execute Query", command=self.execute_query).grid(row=2, column=0, columnspan=6, pady=10)

        # Button to export data to CSV
        ttk.Button(root, text="Export CSV", command=self.export_to_csv).grid(row=0, column=6, rowspan=3, padx=10, pady=5)

        # Text area to display results
        self.result_text = scrolledtext.ScrolledText(root, width=122, height=25, wrap=tk.WORD)
        self.result_text.grid(row=3, column=0, columnspan=6, padx=10, pady=5)

        # Red button to exit the program
        ttk.Button(root, text="Exit", style="Red.TButton", command=root.destroy).grid(row=3, column=6, padx=10, pady=5)

    def execute_query(self):
        # Read CSV files
        usb_data = pd.read_csv("usb_history.csv")
        lnk_data = pd.read_csv("lnk_info.csv")
        tk.Label(root, text="        ").grid(row=0, column=8, rowspan=3, padx=10, pady=8)
        # Convert date columns to datetime format for querying
        usb_data["Last Connected"] = pd.to_datetime(usb_data["Last Connected"])
        lnk_data["Access Time"] = pd.to_datetime(lnk_data["Access Time"])

        # Get start date and time from GUI
        start_date = pd.to_datetime(self.start_datetime_var.get())
        start_hour = int(self.start_hour_combobox.get())
        start_minute = int(self.start_minute_combobox.get())

        # Set start time
        start_datetime = pd.Timestamp(f"{start_date.year}-{start_date.month}-{start_date.day} {start_hour}:{start_minute}:00")

        # Get end date and time from GUI
        end_date = pd.to_datetime(self.end_datetime_var.get())
        end_hour = int(self.end_hour_combobox.get())
        end_minute = int(self.end_minute_combobox.get())

        # Set end time
        end_datetime = pd.Timestamp(f"{end_date.year}-{end_date.month}-{end_date.day} {end_hour}:{end_minute}:59")

        # Execute the query based on dates and times
        usb_matches = usb_data[(usb_data["Last Connected"] >= start_datetime) & (usb_data["Last Connected"] <= end_datetime)]
        # Sort results by ascending date and time
        usb_matches.sort_values(by=["Last Connected"], inplace=True)

        # Find matches in lnk_info.csv files
        lnk_matches = lnk_data[(lnk_data["Access Time"] >= start_datetime) & (lnk_data["Access Time"] <= end_datetime)]
        lnk_matches.sort_values(by=["Access Time"], inplace=True)

 # Display the results in the text area
        self.result_text.delete(1.0, tk.END)  # Clear the text area
        if usb_matches.empty:
            self.result_text.insert(tk.END, "No data found in the selected time interval!\n")
        for index, row in usb_matches.iterrows():
             self.result_text.insert(tk.END, f"USB: {row['Friendly Name']} S/N:{row['Serial Number']}\n")
             self.result_text.insert(tk.END, f"Connection Date: {row['Last Connected']}\n")

             for lnk_index, lnk_row in lnk_matches.iterrows():
                 self.result_text.insert(tk.END, f"RESOURCE: {lnk_row['User Path']} - Access Time: {lnk_row['Access Time']} - {lnk_row['Volume Type']} - {lnk_row['Volume Serial Number']} \n\n")

    def export_to_csv(self):
        # Get data from the text area
        data_to_export = self.result_text.get(1.0, tk.END)
        timestamp = time.strftime("%Y%m%d%H%M%S")
        # Write data to a CSV file
        with open(f"exported_data_{timestamp}.csv", "w") as file:
            file.write(data_to_export)
            tk.Label(root, text="Done!").grid(row=0, column=8, rowspan=3, padx=10, pady=8)
    def run_external_program(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()

if __name__ == "__main__":
    root = tk.Tk()

    # Style for the red button
    root.tk_setPalette(background='#ececec', foreground='black',
                       activeBackground='#d9d9d9', activeForeground='black')

    style = ttk.Style(root)
    style.configure("Red.TButton", foreground="black", background="red")

    app = USBQueryApp(root)
    root.mainloop()
