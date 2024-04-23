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
    train_path = os.path.join(result_path, 'train')
    test_path = os.path.join(result_path, 'test')

    os.mkdir(train_path)
    os.mkdir(test_path)
    for item in ['image', 'mask']:
        os.mkdir(os.path.join(train_path, item))
        os.mkdir(os.path.join(test_path, item))

    paths = os.listdir(os.path.join(origin_path, item))
    print(len(paths))

    train, test = train_test_split(paths, test_size=0.2, random_state=42)
    if save_all_train:
        train = paths
    # print(train, test)
    print(len(train), len(test))

    for path in tqdm(train):
        shutil.copy(os.path.join(origin_path, 'image', path), os.path.join(train_path, 'image', path))
        shutil.copy(os.path.join(origin_path, 'mask', path), os.path.join(train_path, 'mask', path))
    for path in tqdm(test):
        shutil.copy(os.path.join(origin_path, 'image', path), os.path.join(test_path, 'image', path))
        shutil.copy(os.path.join(origin_path, 'mask', path), os.path.join(test_path, 'mask', path))


if __name__ == '__main__':
    args = parse_args()
    data_spilt(args, save_all_train=True)
