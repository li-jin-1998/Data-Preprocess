import os
import shutil
import sys

from tqdm import tqdm

src_path = r'/mnt/algo-storage-server/Workspaces/fangqi/99_无牙'
dst_path = r"/home/lj/PycharmProjects/wyh/dataset/wyh"

# if os.path.exists(dst_path):
#     shutil.rmtree(dst_path)
os.makedirs(dst_path,exist_ok=True)

for file in os.listdir(src_path):
    if '20240422112129' not in file:
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
