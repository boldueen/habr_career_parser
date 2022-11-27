import os
import math
from settings import DATA_FOLDER, ERROR_FOLDER, ERROR_FILEPATH


def initialize_data_folder():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)


def initialize_error_folder():
    if not os.path.exists(ERROR_FOLDER):
        os.makedirs(ERROR_FOLDER)
    
    # create a errors.txt
    with open(ERROR_FILEPATH, 'w') as r:
        pass


def chunks(lst, n):
    result = []
    chunk_size = math.ceil(len(lst)/n)
    for i in range(0, len(lst), chunk_size):
        result.append(lst[i:i + chunk_size]) 
    return result

