import os
import shutil
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from parse_args import parse_args


def data_spilt(args, save_all_train=False):
    print("*" * 20)
    print("Data split.")
    print("*" * 20)
    origin_path = args.dataset_dir
    result_path = os.path.join(origin_path, 'data')

    if os.path.exists(result_path):
        shutil.rmtree(result_path)
    os.mkdir(result_path)

    paths = os.listdir(os.path.join(origin_path, 'image'))
    print(len(paths))

    train, test = train_test_split(paths, test_size=0.2, random_state=101)
    if save_all_train:
        train = paths
    # print(train, test)
    print(len(train), len(test))
    with open(os.path.join(result_path, 'train.txt'), 'w') as file:
        for path in tqdm(train):
            file.write(path + '\n')
    with open(os.path.join(result_path, 'test.txt'), 'w') as file:
        for path in tqdm(test):
            file.write(path + '\n')

if __name__ == '__main__':
    args = parse_args()
    data_spilt(args, save_all_train=True)
