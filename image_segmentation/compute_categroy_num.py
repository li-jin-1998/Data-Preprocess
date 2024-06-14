import os
import shutil

import cv2
from tqdm import tqdm

pixel_value = 192
is_copy = False

src = "/home/lj/PycharmProjects/2D-image-Segmentation/dataset/mask"

if is_copy:
    dst = f"/home/lj/PycharmProjects/2D-image-Segmentation/dataset/mask_{pixel_value}"
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)

count = 0
src_files = [entry for entry in os.scandir(src) if entry.is_file() and entry.name.endswith('.png')]

for entry in tqdm(src_files, desc="Processing masks"):
    mask_path = entry.path
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        print(f"Error reading file: {mask_path}")
        continue
    if pixel_value in mask:
        count += 1
        if is_copy:
            shutil.copy(mask_path, os.path.join(dst, entry.name.replace('.png', 'mask.png')))
            image_path = mask_path.replace("/mask", "/image")
            shutil.copy(image_path, os.path.join(dst, entry.name.replace('.png', 'image.png')))

print(f"Total masks with pixel value {pixel_value}: {count}")
print(f"Total masks processed: {len(src_files)}")
