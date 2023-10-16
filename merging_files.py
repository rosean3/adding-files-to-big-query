import os
import json
from utils.basic_functions import *
from finding_headers import headers

headers_set = set(headers)

def merge_jsonl_files(file_paths):
    merged_data = []
    all_columns = set()

    for file_path in file_paths:
        filename = file_path.split("/")[-1]
        print("reading from", filename)

        with open(file_path, 'r') as file:
            for line in file:
                try:
                    data = json.loads(line)
                    merged_data.append(data)
                    all_columns.update(data.keys())  # add the keys/columns to the set
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON in file: {file_path}")
                    continue
    
    if all_columns == headers_set:
        return (merged_data, True)
    return (merged_data, False)

def write_merged_data_to_jsonl(merged_data, output_file):
    with open(output_file, 'w') as file:
        for item in merged_data:
            json_line = json.dumps(item)
            file.write(json_line + '\n')

def chunked_files(files, chunk_size):
    """Yield successive chunked lists of files."""
    for i in range(0, len(files), chunk_size):
        yield files[i:i + chunk_size]

directory_to_read_from = "finalJsonFiles"
directory_to_write_in = "mergedJsonFiles"

# List of Excel files to read
files_to_read = get_files_to_read(directory_to_read_from, ".jsonl")

print("number of files to merge: ", len(files_to_read))

# Create the directory_to_write_in folder if it doesn't exist
if not os.path.exists(directory_to_write_in):
    os.makedirs(directory_to_write_in)

chunk_size = 5  # Adjust this as needed. It defines how many files are merged into one output file.

chunked = list(chunked_files(files_to_read, chunk_size))

for index, chunk in enumerate(chunked, 1):
    print(f"Chunk {index}:", chunk)

for idx, file_chunk in enumerate(chunked_files(files_to_read, chunk_size), start=1):
    output_filename = os.path.join(directory_to_write_in, f'merged{idx}.jsonl')
    
    # Call the function to merge the JSONL files in chunks
    (merged_data_chunk, hasAllHeaders) = merge_jsonl_files([os.path.join(directory_to_read_from, file) for file in file_chunk])

    if hasAllHeaders:
        print(f"all headers present in chunk {idx}")

    print(f"data merged for chunk {idx}")

    # Save merged data to a new JSONL file for each chunk
    write_merged_data_to_jsonl(merged_data_chunk, output_filename)
