import os
import shutil
from sklearn.model_selection import train_test_split
from tqdm import tqdm


def data_spilt(dataset_path):
    print("*" * 20)
    print("Data split.")
    print("*" * 20)
    data_path = os.path.join(dataset_path, 'data')
    paths = [p for p in os.listdir(data_path) if 'label' in p][::2]
    train, test = train_test_split(paths, test_size=0.3, random_state=42)
    # print(train, test)
    print(len(train), len(test))

    with open(os.path.join(dataset_path, 'train_label.txt'), 'w') as file:
        for path in tqdm(train):
            file.write(path + '\n')
    with open(os.path.join(dataset_path, 'test_label.txt'), 'w') as file:
        for path in tqdm(test):
            file.write(path + '\n')

    with open(os.path.join(dataset_path, 'train.txt'), 'w') as file:
        for path in tqdm(train):
            file.write(path.replace('_label', '') + '\n')
    with open(os.path.join(dataset_path, 'test.txt'), 'w') as file:
        for path in tqdm(test):
            file.write(path.replace('_label', '') + '\n')

if __name__ == '__main__':
    dst = r'D:\Projects\PointCloudSeg\Dataset'
    data_spilt(dst)
