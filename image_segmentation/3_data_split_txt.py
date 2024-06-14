import os
import shutil
import time
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from config_path import DATASET_DIR


def ensure_directory_exists(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)


def split_data(paths, test_size=0.2, random_state=2024, save_all_train=False):
    if save_all_train:
        return paths, []
    return train_test_split(paths, test_size=test_size, random_state=random_state)


def write_list_to_file(file_path, data_list):
    with open(file_path, 'w') as file:
        for item in tqdm(data_list, desc=f"Writing to {os.path.basename(file_path)}"):
            file.write(item + '\n')


def data_split(save_all_train=False):
    print("-" * 20)
    print("Data split.")
    print("-" * 20)

    origin_path = DATASET_DIR
    result_path = os.path.join(origin_path, 'data')

    ensure_directory_exists(result_path)

    paths = os.listdir(os.path.join(origin_path, 'image'))
    print(f"Total files: {len(paths)}")

    train, test = split_data(paths, save_all_train=save_all_train)
    print(f"Train set size: {len(train)}, Test set size: {len(test)}")

    write_list_to_file(os.path.join(result_path, 'train.txt'), train)
    write_list_to_file(os.path.join(result_path, 'test.txt'), test)


if __name__ == '__main__':
    start_time = time.time()
    data_split(save_all_train=False)
    print(f"--- {time.time() - start_time} seconds ---")
