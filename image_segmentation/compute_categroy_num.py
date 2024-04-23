import os
import shutil

import cv2
import numpy as np
from tqdm import tqdm

src = "D:/Projects/UNet/Dataset10/mask/"

i = 0
for p in tqdm(os.listdir(src)):
    mask_path = os.path.join(src, p)
    mask = cv2.imread(mask_path)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask = np.array(mask)
    if 64 in mask:
        i = i + 1
        # print(mask_path)
print(i, len(os.listdir(src)))
