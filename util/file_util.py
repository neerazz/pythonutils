import os
import shutil
from typing import Sequence, List

import pandas as pd
from pandas import DataFrame


def delete_files_or_directory(path: str, dir_ref: str = None):
    if (not path.startswith("/")) and (dir_ref is not None):
        if dir_ref == ".":
            path = f"{os.getcwd()}/{path}"
        else:
            path = f"{dir_ref}/{path}"

    # Check if the path exists
    if os.path.exists(path):
        # Check if the path is a directory
        if os.path.isdir(path):
            # Delete all files in the directory
            shutil.rmtree(path)
            print(f"All files in the directory {path} have been deleted.")
        else:
            # Delete the file
            os.remove(path)
            print(f"The file {path} has been deleted.")
    else:
        # Print an error message
        print(f"Error: {path} not found.")


def read_from_file(path: str, dir_ref: str = None):
    # If the path does not start with "/", and a directory reference is provided
    if (not path.startswith("/")) and (dir_ref is not None):
        if dir_ref == ".":
            path = f"{os.getcwd()}/{path}"
        else:
            path = f"{dir_ref}/{path}"

    # Open the file in read mode
    with open(path, 'r') as f:
        # Read the lines from the file and remove newline characters
        lines = [line.strip() for line in f.readlines()]

    return lines


def read_from_file_as_string(path: str, dir_ref: str = None):
    # If the path does not start with "/", and a directory reference is provided
    if (not path.startswith("/")) and (dir_ref is not None):
        if dir_ref == ".":
            path = f"{os.getcwd()}/{path}"
        else:
            path = f"{dir_ref}/{path}"

    # Open the file in read mode
    with open(path, 'r') as f:
        # Read the data from the file
        data = f.read()

    return data


def read_from_xls(file_name: str, names: Sequence[str] = None, parse_dates: bool = False,
                  skip_rows: Sequence[int] = None) -> DataFrame:
    return pd.read_excel(file_name, names=names, parse_dates=parse_dates, skiprows=skip_rows)


def write_to_file(file_name, file_lines: List[str]):
    with open(file_name, 'w') as file:
        for line in file_lines:
            file.write(line)
            file.write("\n")


def append_to_file(file_name, file_lines: List[str]):
    with open(file_name, 'a') as file:
        for line in file_lines:
            file.write(line)
            file.write("\n")


if __name__ == "__main__":
    delete_files_or_directory("abc")
    delete_files_or_directory("abc", ".")
