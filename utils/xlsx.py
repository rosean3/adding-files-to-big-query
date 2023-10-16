import openpyxl

def count_lines_xlsx(file_path):
    """
    Count the number of lines in an xlsx file excluding the header.
    
    Args:
    - file_path (str): Path to the .xlsx file.
    
    Returns:
    - int: Number of lines excluding the header.
    """
    # Load the workbook and select the first sheet
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.worksheets[1]

    # Count the number of lines, subtracting 1 for the header
    line_count = max(sheet.max_row - 1, 0)
    
    return line_count