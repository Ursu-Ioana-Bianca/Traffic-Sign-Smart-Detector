import os
from mlDetection.config import TRAIN_PATH, TEST_PATH


def update_file_paths(new_train_location, new_test_location):
    def process_file(file_path, new_location):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        with open(file_path, 'w') as file:
            for line in lines:
                parts = line.strip().split('/')
                parts[0:5] = new_location.strip().split('/')
                new_line = '/'.join(parts) + '\n'
                file.write(new_line)

    process_file(TRAIN_PATH, new_train_location)
    process_file(TEST_PATH, new_test_location)


if __name__ == "__main__":
    # Set the location of train/test folders on your computer.
    # Modify only these variables.
    new_train_location = r'D:\Documents\MASTER\Web\prepare_gtsrb\Traffic-Signs-Data-German\filtered_dataset\train'
    new_test_location = r'D:\Documents\MASTER\Web\prepare_gtsrb\Traffic-Signs-Data-German\filtered_dataset\test'

    update_file_paths(new_train_location, new_test_location)
