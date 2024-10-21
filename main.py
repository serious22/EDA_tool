import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import dataCleaning as dc

main_df = pd.DataFrame

def start():

    dc.cleaning_data(main_df)

def select_excel_file():
    excel_filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    excel_filepath_label = ttk.Label(app,
              text=f'File {excel_filepath} successfully loaded.')
    excel_filepath_label.pack()

    global main_df
    main_df = pd.read_excel(excel_filepath)

    button = ttk.Button(app, text='Start', command=start)
    button.pack()

def select_csv_file():
    csv_filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    csv_filepath_label = ttk.Label(app,
              text=f'File {csv_filepath} successfully loaded.')
    csv_filepath_label.pack()

    global main_df
    main_df = pd.read_excel(csv_filepath)

    button = ttk.Button(app, text='Start', command=start)
    button.pack()

#<---MAIN WINDOW START--->
app = tk.Tk()
app.geometry("500x300")
app.title("Data Cleaning and Preprocessing Tool")

heading_label = ttk.Label(app, 
                  text='EDA Tool',
                  font=("Arial", 12))
heading_label.pack()
desc_label = ttk.Label(app, 
                  text='This is an automated eda tool. Use the button below to select file',
                  font=("Arial",9))
desc_label.pack()


button = ttk.Button(app, text='Select Excel File', command=select_excel_file)
button.pack()
button = ttk.Button(app, text='Select CSV File', command=select_csv_file)
button.pack()


app.mainloop()