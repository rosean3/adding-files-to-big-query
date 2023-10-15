import pandas as pd
from datetime import datetime
import re

def try_convert_date_with_index(val, column_name, index):
    """Attempt to convert the value to a date. Print an error message if unsuccessful."""
    try:
        return pd.to_datetime(val)
    except Exception:
        print(f"Error converting value '{val}' in column '{column_name}' at index {index}")
        return val
    
def try_convert_date(val, column_name):
    """Attempt to convert the value to a date. Print an error message if unsuccessful."""
    try:
        return pd.to_datetime(val)
    except Exception:
        print(f"Error converting value '{val}' in column '{column_name}'")
        return val

def convert_unix_to_date(unix_timestamp_ms):
    """Convert Unix timestamp to mm/dd/yyyy format."""
    unix_timestamp_sec = unix_timestamp_ms / 1000
    return datetime.utcfromtimestamp(unix_timestamp_sec).strftime('%m/%d/%Y')

def convert_dd_mm_yyyy_to_mm_dd_yyyy(date_str):
    """Convert date from dd.mm.yyyy format to mm/dd/yyyy format."""
    day, month, year = date_str.split('.')

    if int(month) > 12:
        raise Exception(f"month is greater than 12: {month}")
    return f"{month}/{day}/{year}"

def convert_date(date_value):
    """Detect date format and convert accordingly."""
    # Check if date is in dd.mm.yyyy format
    if str(date_value).count('.') == 2:
        return convert_dd_mm_yyyy_to_mm_dd_yyyy(date_value)
    
    # Check if date is a Unix timestamp
    try:
        return convert_unix_to_date(int(date_value))
    except ValueError:
        raise Exception(f"Unrecognized date format: {date_value}")

def convert_date_format(date_str):
    """
    Convert a date string from various formats to "mm/dd/yyyy".

    Args:
    - date_str (str): Date string to be converted.

    Returns:
    - str: Converted date string in "mm/dd/yyyy" format.
    """
    date_str = str(date_str)
    # Pattern for "d.m.yyyy" or "dd.mm.yyyy"
    match_dmY = re.match(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", date_str)
    # Pattern for "yyyy-m-d" or "yyyy-mm-dd"
    match_Ymd = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", date_str)

    if match_dmY:
        day, month, year = match_dmY.groups()
        dt = datetime(year=int(year), month=int(month), day=int(day))
        result = dt.strftime('%m/%d/%Y')
        # print(f"{date_str} converted to {result}")
        return result

    elif match_Ymd:
        year, month, day = match_Ymd.groups()
        dt = datetime(year=int(year), month=int(month), day=int(day))
        result = dt.strftime('%m/%d/%Y')
        # print(f"{date_str} converted to {result}")
        return result

    else:
        raise ValueError(f"Date string {date_str} not in expected format.")
