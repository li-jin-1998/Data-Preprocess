import os
import shutil
import sys

import cv2
import numpy as np
from tqdm import tqdm

from image_segmentation.parse_args import parse_args

args = parse_args()
src = os.path.join(args.dataset_dir, 'mask')
# src = "D:/Projects/UNet/Dataset14/mask/"

dst = src.replace('mask', 'color_mask')

if os.path.exists(dst):
    shutil.rmtree(dst)
os.makedirs(dst, exist_ok=True)


def check_class_distribution(masks, num_classes):
    class_counts = np.zeros(num_classes, dtype=int)
    mask[mask == 64.0] = 1.0
    mask[mask == 129.0] = 2.0
    mask[mask == 192.0] = 3.0
    mask[mask == 255.0] = 4.0
    for i in range(num_classes):
        class_counts[i] = np.sum(masks == i)
    return class_counts

num_classes = 5


i = 0
for p in tqdm(os.listdir(src)[::], file=sys.stdout):
    mask_path = os.path.join(src, p)
    image_path = mask_path.replace('mask', 'image')
    image_path = image_path.replace('MASK', 'IMAGE')

    image = cv2.imread(image_path)

    mask = cv2.imread(mask_path)
    # mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask = np.array(mask)

    # class_counts = check_class_distribution(mask, num_classes)
    # print(f"类别像素分布: {class_counts}")

    color_mask = image * (mask > 0)
    cv2.imwrite(mask_path.replace('mask', 'color_mask'), color_mask)
