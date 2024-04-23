import os
import shutil

import cv2
import numpy as np
from tqdm import tqdm

src_path = r'D:\Projects\ScanSceneClassification\extra'
dst_path = r'D:\Projects\ScanSceneClassification\clean'

if os.path.exists(dst_path):
    shutil.rmtree(dst_path)
os.mkdir(dst_path)

for path in tqdm(os.listdir(src_path)):
    image_path = os.path.join(src_path, path)

    image = cv2.imread(image_path)
    # if image is None:
    #     print(image_path)
    #     shutil.copy(image_path,os.path.join(dst_path, path))
    #     os.remove(image_path)

    brightness = np.mean(image)
    # if brightness < 90 or brightness > 165:
    if brightness < 70 or brightness > 200:
        # print(brightness, image_path)
        # shutil.copy(image_path, os.path.join(dst_path, path))
        os.remove(image_path)
