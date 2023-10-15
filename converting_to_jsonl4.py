import os
import pandas as pd
from utils.basic_functions import *
from utils.date import *
from utils.constants import *
import datetime

directory_to_read_from = "xlsxFiles"
directory_to_write_in = "finalJsonFiles"

# List of Excel files to read
files_to_read = get_files_to_read(directory_to_read_from, ".xlsx")

print("number of files to read from: ", len(files_to_read))

# Create the 'jsonFiles' folder if it doesn't exist
if not os.path.exists(directory_to_write_in):
    os.makedirs(directory_to_write_in)

for filename in files_to_read:
    print("readind from: ", filename)
    # Read the second sheet of the Excel file
    df = pd.read_excel(os.path.join(directory_to_read_from, filename), sheet_name=1)

    # Convert and verify datetime64[ns] columns in DATE_COLUMNS
    for column in DATE_COLUMNS:
        if column in df.columns:
            # Convert to "mm/dd/yyyy" format
            if df[column].dtype == 'datetime64[ns]':
                df[column] = df[column].dt.strftime('%m/%d/%Y')
            else:
                # convert dd.mm.yyyy and yyyy-mm-dd to mm/dd/yyyy
                df[column] = df[column].apply(convert_date_format)
            # # Filter and print values of type datetime.time
            # time_values = df[df[column].apply(lambda x: isinstance(x, datetime.time))]
            # if not time_values.empty:
            #     print(f"Values of type datetime.time in column '{column}':")
            #     print(time_values[column][0])


            # Verification
            # original_values = pd.read_excel(os.path.join(directory_to_read_from, filename), dtype={column: str})[column]
            # if not all(df[column] == original_values):
            #     print(f"Warning: Transformed values in column {column} of {filename} don't match the original ones!")

    # Construct the output JSONL file name
    jsonl_filename = os.path.join(directory_to_write_in, os.path.splitext(filename)[0] + ".jsonl")

    # Write to JSONL format
    df.to_json(jsonl_filename, orient="records", lines=True)
