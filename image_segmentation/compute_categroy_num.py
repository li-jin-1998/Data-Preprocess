import os
import shutil

import cv2
import numpy as np
from tqdm import tqdm

pixel_value = 64

src = "/home/lj/PycharmProjects/2D-image-Segmentation/dataset/mask"
dst = "/home/lj/PycharmProjects/2D-image-Segmentation/dataset/mask_"+str(pixel_value)

if os.path.exists(dst):
    shutil.rmtree(dst)
os.makedirs(dst, exist_ok=True)

i = 0
for p in tqdm(os.listdir(src)):
    mask_path = os.path.join(src, p)
    mask = cv2.imread(mask_path)
    if mask is None:
        print(mask_path)
        continue
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask = np.array(mask)
    if pixel_value in mask:
        i = i + 1
        shutil.copy(mask_path, os.path.join(dst, p.replace('.png', 'mask.png')))
        image_path = mask_path.replace("/mask", "/image")
        shutil.copy(image_path, os.path.join(dst, p.replace('.png', 'image.png')))
        # print(mask_path)
print(i, len(os.listdir(src)))
