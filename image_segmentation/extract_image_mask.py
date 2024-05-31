import os
import shutil

import cv2
import numpy as np
from tqdm import tqdm

src = "/home/lj/PycharmProjects/2D-image-Segmentation/dataset"

dst = r"/home/lj/PycharmProjects/Data/check"
if os.path.exists(dst):
    shutil.rmtree(dst)
os.makedirs(dst, exist_ok=True)

image_paths = os.path.join(src, "image")

for p in tqdm(os.listdir(image_paths)):
    if 'tlj' in p:
        mask_path = os.path.join(src, "mask", p)
        mask = cv2.imread(mask_path)
        if mask is None:
            print(mask_path)
            continue
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        mask = np.array(mask)
        if np.all(mask == 129):
            print(mask_path)
            shutil.copy(os.path.join(image_paths, p), os.path.join(dst, p))
            shutil.copy(mask_path, os.path.join(dst, p.replace('.png', '_mask.png')))
