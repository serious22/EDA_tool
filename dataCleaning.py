import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd



def cleaning_data(main_df):
        processing_window = tk.Toplevel()
        processing_window.title("Processing file")
        processing_window.geometry("250x150")


        label = tk.Label(processing_window,
                         text = 'Starting the cleaning process.')
        label.pack()

        main_df.drop_duplicates(inplace=True)  # using pandas

        label = tk.Label(processing_window,
                         text = 'Removed duplicated value')
        label.pack()

        #-------Handling missing values----------
        num_columns = main_df.select_dtypes(include=['int64', 'float64'])
        num_nan_columns = num_columns.columns[num_columns.isnull().any()]

        for i in num_nan_columns:
            mean = round(main_df[i].mean(),0)
            main_df[i].fillna(mean, inplace=True)

        threshold = 7  

        cat_columns = main_df.columns[main_df.nunique() < threshold]
        for i in cat_columns:
            if main_df[i].isnull().any() :
                freq = main_df[i].value_counts().idxmax()
                main_df[i].fillna(freq, inplace=True)

        label = tk.Label(processing_window,
                         text = 'Replaced missing values.')
        label.pack()

        #-------Feature Selection----------