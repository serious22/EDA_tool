import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
from sklearn.feature_selection import VarianceThreshold


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
        X = num_columns
        variances = X.var()
        sorted_variances = variances.sort_values(ascending=False)

        features_to_keep = (len(sorted_variances) // 2) + 1  # Half + 1

        top_features = sorted_variances.index[:features_to_keep] #selected on the top features

        X_high_variance = X[top_features]
        # Remove features with low variance
        tVt = 1
        selector = VarianceThreshold(threshold=tVt) 
        X_filtered = selector.fit_transform(X_high_variance) #filtering if the features are still below threshold.

        selected_columns = X_high_variance.columns[selector.get_support()]

        X_filtered_df = pd.DataFrame(X_filtered, columns=selected_columns)

        main_df_filtered = main_df.copy()

        main_df_filtered = main_df_filtered.drop(columns=num_columns.columns)
        main_df_filtered = pd.concat([main_df_filtered, X_filtered_df], axis=1)#to keep the categorical columns as well

        main_df = main_df_filtered.copy()

        label = tk.Label(processing_window,
                         text = 'Important features have been selected for further processing.')
        label.pack()