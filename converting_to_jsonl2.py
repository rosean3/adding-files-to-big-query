import os
import pandas as pd
from utils.basic_functions import *
from utils.date import *

directory_to_read_from = "xlsxFiles"
directory_to_write_in = "jsonFiles2"

# List of Excel files to read
files_to_read = get_files_to_read(directory_to_read_from, ".xlsx")

print("number of files to read from: ", len(files_to_read))

date_columns = ['data_aut', 'data_exe', 'data_nasc', 'data_sol']

# Create the directory_to_write_in folder if it doesn't exist
if not os.path.exists(directory_to_write_in):
    os.makedirs(directory_to_write_in)

# Iterate through each Excel file and convert it to JSONL
for filename in files_to_read:
    # Read the second sheet of the Excel file
    df = pd.read_excel(os.path.join(directory_to_read_from, filename), sheet_name=1)

    # Format date columns as "MM/DD/YYYY"
    for column in date_columns:
        if column in df.columns:
            # Convert column to datetime, and print values that fail conversion
            df[column] = df[column].apply(lambda val: try_convert_date(val, column))
            df[column] = df[column].dt.strftime("%m/%d/%Y")

    # Construct the output JSONL file name
    jsonl_filename = os.path.join(directory_to_write_in, os.path.splitext(filename)[0] + ".jsonl")

    # Write to JSONL format with dates in "MM/DD/YYYY" format
    df.to_json(jsonl_filename, orient="records", lines=True)

    print(f"Converted {filename} to {jsonl_filename}")