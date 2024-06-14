import os
import shutil
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from config_path import DATASET_DIR, ensure_directory_exists


def create_subdirectories(base_path, subdirs):
    for subdir in subdirs:
        os.makedirs(os.path.join(base_path, subdir), exist_ok=True)


def copy_files(file_list, origin_path, dest_path, item):
    for file in tqdm(file_list, desc=f"Copying {item} files"):
        src_image_path = os.path.join(origin_path, 'image', file)
        dst_image_path = os.path.join(dest_path, 'image', file)
        src_mask_path = os.path.join(origin_path, 'mask', file)
        dst_mask_path = os.path.join(dest_path, 'mask', file)

        try:
            shutil.copy(src_image_path, dst_image_path)
            shutil.copy(src_mask_path, dst_mask_path)
        except Exception as e:
            print(f"Error copying {file}: {e}")


def data_split(save_all_train=False):
    print("-" * 20)
    print("Data split.")
    print("-" * 20)
    origin_path = DATASET_DIR
    result_path = os.path.join(origin_path, 'data')

    ensure_directory_exists(result_path)
    train_path = os.path.join(result_path, 'train')
    test_path = os.path.join(result_path, 'test')

    create_subdirectories(train_path, ['image', 'mask'])
    create_subdirectories(test_path, ['image', 'mask'])

    paths = os.listdir(os.path.join(origin_path, 'image'))
    print(f"Total files: {len(paths)}")

    train, test = train_test_split(paths, test_size=0.2, random_state=42)
    if save_all_train:
        train = paths

    print(f"Train set size: {len(train)}, Test set size: {len(test)}")

    copy_files(train, origin_path, train_path, 'train')
    copy_files(test, origin_path, test_path, 'test')


if __name__ == '__main__':
    data_split(save_all_train=False)
