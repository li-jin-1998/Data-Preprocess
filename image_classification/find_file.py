import os
import shutil
import glob

src_path = r'D:\Dataset\2D\外部收集\00_种植'
dst_path = r'D:\Projects\ScanSceneClassification\implant'

if os.path.exists(dst_path):
    shutil.rmtree(dst_path)
os.mkdir(dst_path)
paths = glob.glob(src_path + '*/*/*.tif')
i = 0
for path in paths:
    print(path)
    for p in (os.listdir(path)):
        if '_7_' in p:
            print(i, os.path.join(path, p))
            shutil.copy(os.path.join(path, p), os.path.join(dst_path, str(i).rjust(5, '0') + '.tif'))
            i = i + 1
