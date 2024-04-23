import os
import shutil
from sklearn.model_selection import train_test_split
from tqdm import tqdm


def data_spilt(dataset_path, item):
    print("*" * 20)
    print("Data split.", item)
    print("*" * 20)
    data_path = os.path.join(dataset_path, item)
    paths = os.listdir(data_path)
    train, test = train_test_split(paths, test_size=0.2, random_state=2024)
    # print(train, test)
    print(len(train), len(test))

    with open(os.path.join(dataset_path, 'train_' + item + '.txt'), 'w') as file:
        for path in tqdm(train):
            file.write(path + '\n')
    with open(os.path.join(dataset_path, 'test_' + item + '.txt'), 'w') as file:
        for path in tqdm(test):
            file.write(path + '\n')


if __name__ == '__main__':
    dst = r'D:\Projects\ScanSceneClassification'
    data_spilt(dst, "extra")
    data_spilt(dst, "intra")
