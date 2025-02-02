import os
from mlDetection.config import TRAIN_PATH, TEST_PATH, DATA_FILE
base_path = r"../config_files"

# File paths
train_file_path = os.path.join(base_path, "train.txt")
test_file_path = os.path.join(base_path, "test.txt")


def replace_backslashes(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    updated_lines = [line.replace('\\', '/') for line in lines]

    with open(file_path, 'w') as file:
        file.writelines(updated_lines)


# replace_backslashes(train_file_path)
# replace_backslashes(test_file_path)
replace_backslashes(DATA_FILE)
