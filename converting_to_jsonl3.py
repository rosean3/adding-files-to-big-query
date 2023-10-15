import json
from utils.date import *
from utils.basic_functions import *

def process_file(input_file, output_file, date_columns):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line_number, line in enumerate(f_in, 1):
            record = json.loads(line)
            for column in date_columns:
                if column in record:
                    try:
                        record[column] = convert_date(record[column])
                    except Exception as e:
                        print(f"Error on line {line_number}, column '{column}', value: '{record[column]}'. Exception: {e}")
                        continue  # Skip to the next column or record if there's an error
            f_out.write(json.dumps(record) + '\n')


date_columns = ['data_aut', 'data_exe', 'data_nasc', 'data_sol']

directory_to_read_from = "jsonFiles"
directory_to_write_in = "jsonFiles3"

# List of Excel files to read
# files_to_read = get_files_to_read(directory_to_read_from, ".xlsx")

files_to_read = ['originais_sisreg_agendamento_202109(18.10.21).jsonl']

print("number of files to read from: ", len(files_to_read))

date_columns = ['data_aut', 'data_exe', 'data_nasc', 'data_sol']

# Create the directory_to_write_in folder if it doesn't exist
if not os.path.exists(directory_to_write_in):
    os.makedirs(directory_to_write_in)

# Iterate through each Excel file and convert it to JSONL
for filename in files_to_read:
    input_file = os.path.join(directory_to_read_from, filename)
    output_file = os.path.join(directory_to_write_in, os.path.splitext(filename)[0] + ".jsonl")

    process_file(input_file, output_file, date_columns)