import pandas as pd
from io import StringIO
import numpy as np
from utils.basic_functions import *

headers = []
keeping_track = {}

directory_to_read = "jsonFiles"

files_to_read = get_files_to_read(directory_to_read, ".jsonl")

for filename in files_to_read:
    # print('reading file: ', filename)

    # ! Read the .jsonl file and get the first line
    with open(os.path.join(directory_to_read, filename), "r") as file:
        first_line = next(file)

    # ! Parse the first line as JSON and create a DataFrame
    df = pd.read_json(StringIO(first_line), lines=True)

    # ! Iterate through the columns and convert possible Unix timestamps to dates
    if headers == []:
        headers = [column for column in df.columns]
    else:
        new_headers = [header for header in df.columns if header not in headers]
        if new_headers:
            keeping_track[filename] = new_headers
            headers = headers + new_headers


headers.sort()
# print("headers: ", headers)
# print("headers length: ", len(headers))
# print("keeping_track: ", keeping_track)

