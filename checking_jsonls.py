import pandas as pd
import re
import os
from utils.basic_functions import *
from utils.date import *
from utils.constants import *
import datetime

def check_date_format(date_str):
    """Check if a string matches the mm/dd/yyyy format."""
    pattern = re.compile(r"^(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])/\d{4}$")
    return bool(pattern.match(date_str))

directory_to_read_from = "finalJsonFiles"

# List of Excel files to read
files_to_read = get_files_to_read(directory_to_read_from, ".jsonl")

print("number of files to read from: ", len(files_to_read))

for filename in files_to_read:
    print("readind from: ", filename)

    # Read the .jsonl file into a DataFrame
    df = pd.read_json(os.path.join(directory_to_read_from, filename), lines=True)
    
    for column in DATE_COLUMNS:
        if column in df.columns:
            incorrect_dates = df[~df[column].astype(str).apply(check_date_format)]
            if not incorrect_dates.empty:
                print(f"Values in column '{column}' that don't match mm/dd/yyyy format:")
                print(incorrect_dates[column])