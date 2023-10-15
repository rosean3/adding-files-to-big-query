import pandas as pd
import numpy as np
from io import StringIO

date_columns = ['data_aut', 'data_exe', 'data_nasc', 'data_sol']
date_types = {column: [] for column in date_columns}

# Function to detect if a value might be a Unix timestamp in milliseconds
def is_unix_timestamp(value):
    # A heuristic: Unix timestamp for year 2000 is 946684800000 and for year 2100 is 4102444800000
    return 946684800000 <= value <= 4102444800000

# Function to process each DataFrame row
def process_row(row, date_types):
    for column in row.index:
        if column in date_columns:
            value = row[column]
            # Checking for Unix timestamp
            if isinstance(value, (int, float, np.int64)) and is_unix_timestamp(value):
                tuple_value = ("timestamp", value)
                if tuple_value[0] not in [t[0] for t in date_types[column]]:
                    date_types[column].append(tuple_value)
                # Convert timestamp to datetime in the DataFrame
                row[column] = pd.to_datetime(value / 1000, unit='s')
            else:
                tuple_value = (type(value), value)
                if tuple_value[0] not in [t[0] for t in date_types[column]]:
                    date_types[column].append(tuple_value)
    return row

# Read the .jsonl file and process each line
with open("originais_sisreg_agendamento_202201.jsonl", "r") as file:
    for line in file:
        df = pd.read_json(StringIO(line), lines=True)
        df = df.apply(lambda row: process_row(row, date_types), axis=1)

print(date_types)
