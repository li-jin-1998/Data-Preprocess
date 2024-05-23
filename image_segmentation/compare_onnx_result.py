import os
import shutil
import glob
from tqdm import tqdm

src_path1 = r'D:\Projects\UNet\onnx—predict3'
# src_path2 = r'D:\Projects\UNet\onnx—predict2'

dst_path = r'D:/Projects/UNet/compare2/'

if os.path.exists(dst_path):
    shutil.rmtree(dst_path)
os.mkdir(dst_path)

paths = glob.glob(src_path1 + '/*/*.*')
print(len(paths))

for path in tqdm(paths):
    path2 = path.replace('onnx—predict3', 'onnx—predict2')
    if os.path.exists(path2):
        result_path = path.replace('onnx—predict3', 'compare2')
        if not os.path.exists(os.path.dirname(result_path)):
            os.mkdir(os.path.dirname(result_path))

        result_path2 = result_path.replace('_predict', '_predict2')

        if os.path.exists(result_path):
            continue

        shutil.copy(path, result_path)
        if 'predict' in result_path:
            shutil.copy(path2, result_path2)

