import os


def is_file_not_empty(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # Check if the file size is greater than 0
        return os.path.getsize(file_path) > 0
    else:
        return False