import pandas as pd
from utils.constants import *
from utils.basic_functions import *
import re

existing_formats = []
existing_types = []

def is_valid_date_format(value, split_string):
    try:
        v1, v2, v3 = value.split(split_string)
        int(v1)
        int(v2)
        int(v3)
        return True
    except ValueError:
        return False

def identify_date_format(value):
    """Identify the date format of the value."""
    
    # Check for YYYY-MM-DD or YYYY-MM-DD HH:MM:SS format
    pattern1 = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    pattern2 = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

    if pattern1.match(value):
        return "yyyy-mm-dd"
    elif pattern2.match(value):
        return "yyyy-mm-dd hh:mm:ss"
    elif "." in value:
        if is_valid_date_format(value, "."):
            day, month, year = value.split(".")
            if int(day) > 12:
                return "dd.mm.yyyy"
            else:
                return "mm.dd.yyyy"
        else:
            return "Not recognized"
    elif "/" in value:
        if is_valid_date_format(value, "/"):
            month, day, year = value.split("/")
            if int(day) > 12:
                return "mm/dd/yyyy"
            else:
                return "dd/mm/yyyy"
    return "Not recognized"


def extract_date_formats_and_examples(df, columns, filename):
    """Identify and extract date formats and examples from the DataFrame."""
    format_examples = {}
    column_type = {}

    # Identify formats and examples for each column
    for column in columns:
        for value in df[column].dropna():
            value = str(value)

            date_format = identify_date_format(value)
            if date_format not in existing_formats:
                existing_formats.append(date_format)
            if date_format == "Not recognized":
                print(f"file {filename} has a date format that is not recognized: {value} in column {column}")
            if date_format:
                if column not in format_examples:
                    format_examples[column] = {}
                if date_format not in format_examples[column]:
                    if date_format == "dd/mm/yyyy" and "mm/dd/yyyy" in format_examples[column]:
                        continue
                    elif date_format == "mm/dd/yyyy" and "dd/mm/yyyy" in format_examples[column]:
                        format_examples[column].pop("dd/mm/yyyy")
                    if date_format == "mm.dd.yyyy" and "dd.mm.yyyy" in format_examples[column]:
                        continue
                    elif date_format == "dd.mm.yyyy" and "mm.dd.yyyy" in format_examples[column]:
                        format_examples[column].pop("mm.dd.yyyy")
                    format_examples[column][date_format] = value  # Store example
        column_type[column] = df[column].dtype
        if df[column].dtype not in existing_types:
            existing_types.append(df[column].dtype)
        if df[column].dtype != 'datetime64[ns]':
            print(f"file {filename} has a date type that is not datetime64[ns]: {df[column].dtype} in column {column}")

    return (format_examples, column_type)

def write_formats_to_txt(format_examples, output_file, column_type):
    """Write the identified date formats and examples to a txt file."""
    with open(output_file, 'w') as f:
        for column, formats in format_examples.items():
            f.write(f"Column: {column}\n")
            f.write(f"  Data type: {column_type[column]}\n")
            for date_format, example in formats.items():
                f.write(f"  Format: {date_format} | Example: {example}\n")
            f.write("\n")

def process_excel(input_excel_file, output_csv_file, output_txt_file):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(input_excel_file, sheet_name=1)

    # Desired columns
    columns_to_extract = DATE_COLUMNS
    existing_columns = [column for column in columns_to_extract if column in df.columns]

    # If no columns match, print a message and exit
    if not existing_columns:
        print("None of the desired columns were found in the Excel file.")
        return

    # Extract values from the existing columns
    extracted_data = df[existing_columns]
    extracted_data.to_csv(output_csv_file, index=False)

    # Extract date formats and examples
    (format_examples, column_type) = extract_date_formats_and_examples(df, existing_columns, input_excel_file)
    write_formats_to_txt(format_examples, output_txt_file, column_type)

directory_to_read_from = "newTest"
directory_to_write_in = "newTest/jsonFiles"

# List of Excel files to read
files_to_read = get_files_to_read(directory_to_read_from, ".xlsx")
# files_to_read = ["originais_sisreg_agendamento_202109(18.10.21).xlsx"]

print("number of files to read from: ", len(files_to_read))

# Create the directory_to_write_in folder if it doesn't exist
if not os.path.exists(directory_to_write_in):
    os.makedirs(directory_to_write_in)

# Iterate through each Excel file and extract the desired columns
for filename in files_to_read:
    print("reading from: ", filename)

    input_file = os.path.join(directory_to_read_from, filename)
    output_csv_file = os.path.join(directory_to_write_in, os.path.splitext(filename)[0] + ".csv")
    output_txt_file = os.path.join(directory_to_write_in, os.path.splitext(filename)[0] + ".txt")

    process_excel(input_file, output_csv_file,output_txt_file)

print("existing formats: ", existing_formats)
print("existing types: ", existing_types)