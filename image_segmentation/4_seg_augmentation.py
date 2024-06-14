import os
import shutil

import cv2
import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.segmaps import SegmentationMapsOnImage
from tqdm import tqdm

from config_path import DATASET_DIR, AUG_NUM, ensure_directory_exists

ia.seed(1)
p = 0.4

# Define the augmentation pipeline
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
    shutil.copy(image_path, os.path.join(output_dir, 'image', f'{base_name}[ORIGIN][IMAGE].png'))
    shutil.copy(mask_path, os.path.join(output_dir, 'mask', f'{base_name}[ORIGIN][MASK].png'))


def save_augmented_files(image_aug, mask_aug, output_dir, base_name, i):
    cv2.imwrite(os.path.join(output_dir, 'image', f'{base_name}[AUG][{i}][IMAGE].png'), image_aug)
    cv2.imwrite(os.path.join(output_dir, 'mask', f'{base_name}[AUG][{i}][MASK].png'), mask_aug.get_arr())


def seg_augmentation(mode='train'):
    print("-" * 20)
    print(f"Segmentation augmentation for {mode} mode.")
    print("-" * 20)

    input_dir = os.path.join(DATASET_DIR, 'data', mode)
    augmentation_output_dir = os.path.join(DATASET_DIR, 'data', f'augmentation_{mode}')
    ensure_directory_exists(augmentation_output_dir)
    ensure_directory_exists(os.path.join(augmentation_output_dir, 'image'))
    ensure_directory_exists(os.path.join(augmentation_output_dir, 'mask'))

    for path in tqdm(os.listdir(os.path.join(input_dir, 'image'))):
        base = os.path.splitext(path)[0]
        image_path = os.path.join(input_dir, 'image', path)
        mask_path = os.path.join(DATASET_DIR, 'mask', path)

        image = cv2.imread(image_path)
        mask = cv2.imread(mask_path)
        copy_original_files(image_path, mask_path, augmentation_output_dir, base)

        mask = SegmentationMapsOnImage(mask, shape=image.shape)

        for i in range(AUG_NUM):
            image_aug, mask_aug = seq(image=image, segmentation_maps=mask)
            save_augmented_files(image_aug, mask_aug, augmentation_output_dir, base, i)


if __name__ == '__main__':
    seg_augmentation('train')
    seg_augmentation('test')
