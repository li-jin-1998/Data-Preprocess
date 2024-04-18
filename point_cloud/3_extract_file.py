import os
import shutil

from tqdm import tqdm

src = r'D:\Projects\PointCloudSeg\raw_images'

dst = r'D:\Projects\PointCloudSeg\Dataset\data'

if os.path.exists(dst):
    shutil.rmtree(dst)
os.makedirs(dst)

nums = 0

for f in os.listdir(src):
    file_path = os.path.join(src, f)
    print(file_path)

    paths = [p for p in os.listdir(file_path) if 'label' in p]

    if len(paths) == 0:
        continue

    nums += len(paths)
    print(nums)

    for p in tqdm(paths):
        label_ply_path = os.path.join(file_path, p)
        # print(label_ply_path, os.path.join(dst, f + '_' + p))
        p2 = p.replace('_label', '')
        ply_path = os.path.join(file_path, p2)
        # print(ply_path, os.path.join(dst, f + '_' + p2))
        p3 = p2.replace('_0_', '_7_').replace('ply', 'tif')
        image_path = os.path.join(file_path, p3)
        # print(image_path, os.path.join(dst, f + '_' + p3))
        shutil.copy(label_ply_path, os.path.join(dst, f + '_' + p))
        shutil.copy(ply_path, os.path.join(dst, f + '_' + p2))
        shutil.copy(image_path, os.path.join(dst, f + '_' + p3))

print(nums)
