import os
import shutil
import sys

from tqdm import tqdm

src_path = r'D:\Dataset\2D\外部收集\07_无牙\2024Q1'
dst_path = r'D:/Projects/UNet/wyh_all2'

if os.path.exists(dst_path):
    shutil.rmtree(dst_path)
os.mkdir(dst_path)




for file in os.listdir(src_path):
    if 'zip' in file:
        continue
    src = os.path.join(src_path, file)
    dst = os.path.join(dst_path, file)
    print(src, dst)
    if os.path.exists(dst):
        print('Output directory already exists: ', dst)
        shutil.rmtree(dst)
    os.makedirs(dst)

    paths = sorted([p for p in os.listdir(src) if '_7_' in p and 'tif' in p])[::4]
    for p in tqdm(paths, file=sys.stdout):
        # print(os.path.join(src, p), os.path.join(dst, p))
        shutil.copy(os.path.join(src, p), os.path.join(dst, p))

    print(len(os.listdir(src)))
