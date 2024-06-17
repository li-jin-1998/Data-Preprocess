import os
import shutil
import sys

import cv2
import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.segmaps import SegmentationMapsOnImage
from tqdm import tqdm

from config_path import DATASET_DIR, ensure_directory_exists, AUG_NUM

ia.seed(1)
p = 0.4

# Define augmentation pipeline.
seq = iaa.Sequential([
    iaa.Sometimes(p, iaa.Rot90((1, 3), keep_size=False)),
    iaa.Sometimes(p, iaa.AddToSaturation((-10, 10))),
    iaa.Sometimes(p, iaa.MultiplyBrightness((0.8, 1.2))),
    iaa.Sometimes(p, iaa.LinearContrast((0.8, 1.2))),
    iaa.Sometimes(p, iaa.AddToHue((-10, 10))),
    iaa.Fliplr(p),
    iaa.Flipud(p)
], random_order=True)


def copy_original_files(image_path, mask_path, output_dir, base_name):
    """Copy original files to the augmentation output directory."""
    shutil.copy(image_path, os.path.join(output_dir, 'image', f'{base_name}[ORIGIN][IMAGE].png'))
    shutil.copy(mask_path, os.path.join(output_dir, 'mask', f'{base_name}[ORIGIN][MASK].png'))


def save_augmented_files(image_aug, mask_aug, output_dir, base_name, i):
    """Save augmented images and masks to the augmentation output directory."""
    cv2.imwrite(os.path.join(output_dir, 'image', f'{base_name}[AUG][{i}][IMAGE].png'), image_aug)
    cv2.imwrite(os.path.join(output_dir, 'mask', f'{base_name}[AUG][{i}][MASK].png'), mask_aug.get_arr())


def process_image(image_path, mask_path, augmentation_output_dir, base_name, aug_num):
    """Process a single image and save its augmented versions."""
    try:
        image = cv2.imread(image_path)
        mask = cv2.imread(mask_path)
        if mask is None or image is None:
            print(f"Skipping {image_path}: Unable to read image or mask.")
            return

        copy_original_files(image_path, mask_path, augmentation_output_dir, base_name)
        mask = SegmentationMapsOnImage(mask, shape=image.shape)

        for i in range(aug_num):
            image_aug, mask_aug = seq(image=image, segmentation_maps=mask)
            save_augmented_files(image_aug, mask_aug, augmentation_output_dir, base_name, i)

    except Exception as e:
        print(f"Error processing {image_path}: {e}")


def seg_augmentation(mode='train', aug_num=AUG_NUM):
    """Perform segmentation augmentation."""
    print("-" * 20)
    print(f"Seg {mode} augmentation.")
    print(f"num: {aug_num}")
    print("-" * 20)

    input_path = os.path.join(DATASET_DIR, 'data')
    txt_file = os.path.join(input_path, f'{mode}.txt')
    paths = sorted([line.strip() for line in open(txt_file)])
    augmentation_output_dir = os.path.join(input_path, f'augmentation_{mode}')

    ensure_directory_exists(augmentation_output_dir)
    ensure_directory_exists(os.path.join(augmentation_output_dir, 'image'))
    ensure_directory_exists(os.path.join(augmentation_output_dir, 'mask'))

    for path in tqdm(paths, file=sys.stdout):
        base = os.path.splitext(path)[0]
        image_path = os.path.join(DATASET_DIR, 'image', path)
        mask_path = os.path.join(DATASET_DIR, 'mask', path)

        process_image(image_path, mask_path, augmentation_output_dir, base, aug_num)


if __name__ == '__main__':
    import time

    start_time = time.time()
    seg_augmentation('train', 3)
    seg_augmentation('test', 2)
    print("--- %s seconds ---" % (time.time() - start_time))
