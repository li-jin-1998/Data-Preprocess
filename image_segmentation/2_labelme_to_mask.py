import glob
import os
import shutil
import sys

import cv2
import labelme
import numpy as np
from tqdm import tqdm

from config_path import DATA_DIR, DATASET_DIR

suffixes = ['png', 'tif']


def ensure_directory_exists(path):
    """Ensure the directory exists, if not, create it."""
    if os.path.exists(path):
        print(f'Output directory already exists: {path}')
        confirmation = input("Do you want to remove it? (y/n): ")
        if confirmation.lower() != 'y':
            print("Aborting...")
            sys.exit(1)
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)


def process_label_file(file_name, output_path, class_name_to_id):
    """Process a single label file to create corresponding image and mask."""
    suffix = ""
    for suffix in suffixes:
        if os.path.exists(file_name.replace('json', suffix)):
            continue
    base = os.path.basename(file_name).replace('json', suffix)
    out_img_file = os.path.join(output_path, 'image', base)
    out_mask_file = os.path.join(output_path, 'mask', base)

    if os.path.exists(out_mask_file):
        return

    try:
        label_file = labelme.LabelFile(filename=file_name)
        img = labelme.utils.img_data_to_arr(label_file.imageData)
        lbl, _ = labelme.utils.shapes_to_label(
            img_shape=img.shape,
            shapes=label_file.shapes,
            label_name_to_value=class_name_to_id
        )
        mask = np.array(lbl)
        mask[mask == 0] = 129
        mask[mask == 1] = 0
        mask[mask == 2] = 255
        mask[mask == 3] = 192
        mask[mask == 4] = 64
        cv2.imwrite(out_mask_file, mask)
        shutil.copy(file_name.replace('json', suffix), out_img_file)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")


def labelme_to_mask():
    """Convert labelme annotations to mask images."""
    print("-" * 20)
    print("Labelme to mask.")
    print("-" * 20)

    input_path = DATA_DIR
    output_path = DATASET_DIR

    ensure_directory_exists(output_path)
    ensure_directory_exists(os.path.join(output_path, 'image'))
    ensure_directory_exists(os.path.join(output_path, 'mask'))

    class_name_to_id = {'gum': 0, '0': 1, '2': 2, '3': 3, '4': 4}
    json_file_names = glob.glob(os.path.join(input_path, '*.json'))

    for file_name in tqdm(json_file_names, desc="Processing files", file=sys.stdout):
        process_label_file(file_name, output_path, class_name_to_id)


if __name__ == '__main__':
    import time

    start_time = time.time()
    labelme_to_mask()
    print(f"--- {time.time() - start_time:.2f} seconds ---")
