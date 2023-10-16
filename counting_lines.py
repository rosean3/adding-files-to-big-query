import os
import pandas as pd
from utils.basic_functions import *
from utils.xlsx import *
import datetime

directory_to_read_from = "xlsxFiles"

# List of Excel files to read
files_to_read = get_files_to_read(directory_to_read_from, ".xlsx")
files_to_read.sort()

number_of_lines = {filename: 0 for filename in files_to_read}

print("number of files to read from: ", len(files_to_read))

for filename in files_to_read:
    number_of_lines[filename] = count_lines_xlsx(os.path.join(directory_to_read_from, filename))

number_of_lines = dict(sorted(number_of_lines.items()))

print('number of lines in each file: ', number_of_lines)
