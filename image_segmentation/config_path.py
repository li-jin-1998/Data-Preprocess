import os
import shutil


def ensure_directory_exists(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)


DATA_DIR = "/home/lj/PycharmProjects/Data/add3"

DATASET_DIR = "/home/lj/PycharmProjects/2D-Image-Segmentation/dataset"

AUG_NUM = 3
