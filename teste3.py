import pandas as pd
from io import StringIO
import numpy as np

date_columns = ['data_aut', 'data_exe', 'data_nasc', 'data_sol']
date_types = {column: [] for column in date_columns}

# Read the .jsonl file and get the first line
with open("originais_sisreg_agendamento_202201.jsonl", "r") as file:
    first_line = next(file)

# Parse the first line as JSON and create a DataFrame
df = pd.read_json(StringIO(first_line), lines=True)

# Function to detect if a value might be a Unix timestamp in milliseconds
def is_unix_timestamp(value):
    # A heuristic: Unix timestamp for year 2000 is 946684800000 and for year 2100 is 4102444800000
    return 946684800000 <= value <= 4102444800000

# Iterate through the columns and convert possible Unix timestamps to dates
for column in df.columns:
    first_value = df[column].iloc[0]
    if isinstance(first_value, (int, float, np.int64)) and is_unix_timestamp(first_value):
        print(f"column {column} is a timestamp")
        df[column] = pd.to_datetime(df[column] / 1000, unit='s')

    column_type = type(df[column].iloc[0])
    print(f"column {column} is {column_type}")

