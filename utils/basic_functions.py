
import os

def get_files_to_read(directory, *args):
    # Ensure provided args are in tuple format
    extensions = tuple(args)

    # Get the current directory
    files_directory = os.path.join(os.getcwd(), directory)

    # List all files in the current directory
    files_in_directory = os.listdir(files_directory)

    # Filter the list to include only files with the desired extensions
    files_to_read = [file for file in files_in_directory if file.endswith(extensions)]

    return files_to_read

# Function to detect if a value might be a Unix timestamp in milliseconds
def is_unix_timestamp(value):
    # A heuristic: Unix timestamp for year 2000 is 946684800000 and for year 2100 is 4102444800000
    return 946684800000 <= value <= 4102444800000