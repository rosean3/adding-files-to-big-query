import os
import pandas as pd
from utils.basic_functions import *
from utils.constants import *

directory_to_read_from = "newTest"
directory_to_write_in = "newTest/jsonFiles"

# List of Excel files to read
files_to_read = get_files_to_read(directory_to_read_from, ".xlsx")

# Create the 'jsonFiles' folder if it doesn't exist
if not os.path.exists(directory_to_write_in):
    os.makedirs(directory_to_write_in)

# Iterate through each Excel file and convert it to JSONL
for filename in files_to_read:
    # Read the second sheet of the Excel file
    df = pd.read_excel(os.path.join(directory_to_read_from, filename))

    # Check and print the data types for the columns in DATE_COLUMNS
    for col in DATE_COLUMNS:
        if col in df.columns:
            print(f"Data type of column {col} in file {filename}: {df[col].dtype}")
            print(f"The value: {df[col][0]}")

    # Construct the output JSONL file name
    jsonl_filename = os.path.join(directory_to_write_in, os.path.splitext(filename)[0] + ".jsonl")

    # Write to JSONL format
    df.to_json(jsonl_filename, orient="records", lines=True)

    print(f"Converted {filename} to {jsonl_filename}")

# def try_convert_date(val, column_name, index):
#     """Attempt to convert the value to a date. Print an error message if unsuccessful."""
#     try:
#         return pd.to_datetime(val)
#     except Exception:
#         print(f"Error converting value '{val}' in column '{column_name}' at index {index}")
#         return val

# if not os.path.exists("jsonFileExtra"):
#     os.makedirs("jsonFileExtra")

# # Iterate through each Excel file and convert it to JSONL
# filename = "originais_sisreg_agendamento_202101.xlsx"
# # Read the second sheet of the Excel file
# df = pd.read_excel(filename, sheet_name=1)

# # Format date columns as "MM/DD/YYYY"
# date_columns = ['data_aut', 'data_exe', 'data_nasc', 'data_sol']  # Replace with actual column names
# for column in date_columns:
#     if column in df.columns:
#         # Convert column to datetime, and print values that fail conversion
#         df[column] = df[column].apply(lambda val: try_convert_date(val, column, df[column][df[column] == val].index[0]))
#         df[column] = df[column].dt.strftime("%m/%d/%Y")

# # Construct the output JSONL file name
# jsonl_filename = os.path.join("jsonFileExtra", os.path.splitext(filename)[0] + ".jsonl")

# # Write to JSONL format with dates in "MM/DD/YYYY" format
# df.to_json(jsonl_filename, orient="records", lines=True)

# print(f"Converted {filename} to {jsonl_filename}")



