import os
import shutil
import glob

from tqdm import tqdm

src_path = r'D:\Projects\ScanSceneClassification\data\intra'
dst_path = r'D:\Projects\ScanSceneClassification\intra'

# if os.path.exists(dst_path):
#     shutil.rmtree(dst_path)
# os.mkdir(dst_path)

paths = glob.glob(src_path + '/*')
print(len(paths))
i = 0
for path in paths:
    print(path)
    for p in tqdm(os.listdir(path)[::4]):
        if '_7_' in p:
            # print(i, os.path.join(path, p))
            shutil.copy(os.path.join(path, p), os.path.join(dst_path,'intra_'+ str(i).rjust(5, '0') + '.tif'))
            i = i + 1
