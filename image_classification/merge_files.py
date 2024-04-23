import os
import shutil
import glob

from tqdm import tqdm

src_path = r'D:\牙模数据'
dst_path = r'D:\extra_data'

images = glob.glob(src_path + '/*/*.tif')

print(len(images))

# if os.path.exists(dst_path):
#     shutil.rmtree(dst_path)
# os.makedirs(dst_path)

for file in os.listdir(src_path):
    source_path = os.path.join(src_path, file)
    i = 0
    for path in tqdm(os.listdir(source_path)):
        if '_7_' in path:
            shutil.copy(os.path.join(source_path, path), os.path.join(dst_path, file + "_" + path))
            i = i + 1
    print(file, i)
