import os
import shutil

from tqdm import tqdm

src_path = r'D:\Projects\ScanSceneClassification\implant'
dst_path = r'D:\Projects\ScanSceneClassification\intra'

# if os.path.exists(dst_path):
#     shutil.rmtree(dst_path)
# os.mkdir(dst_path)

i = 0
for path in tqdm(os.listdir(src_path)[::4]):
    # print(i, path)
    shutil.copy(os.path.join(src_path, path), os.path.join(dst_path, 'implant_'+str(i).rjust(5, '0') + '.tif'))
    i = i + 1
