import os

from tqdm import tqdm

src = "/home/lj/PycharmProjects/2D-image-Segmentation/dataset"

image_paths = os.path.join(src, "image")
mask_paths = os.path.join(src, "mask")

key = '[tlj][610_upper_color]'

for p in tqdm(os.listdir(image_paths)):
    if key in p:
        image_path = os.path.join(image_paths, p)
        os.remove(image_path)
        print(image_path)

for p in tqdm(os.listdir(mask_paths)):
    if key in p:
        mask_path = os.path.join(mask_paths, p)
        os.remove(mask_path)
        print(mask_path)
