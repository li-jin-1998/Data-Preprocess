import os
import shutil

from tqdm import tqdm

src_path = r'D:\git'
dst_path = r'D:\牙模数据'

file_list = ["20240419101122", "scene1", "bug4016", "mix_extra",
             "metal", "images18", "20240419135140", "20240419135526",
             "20240419145634","20240419150214","20240419150630",
             "20240419150828","20240419151141","20240419152935","20240419153242"]

for file in file_list:
    source_path = os.path.join(src_path, file)
    result_path = os.path.join(dst_path, file)
    if os.path.exists(result_path):
        print(result_path, " exist.")
        continue
    os.makedirs(result_path, exist_ok=True)

    i = 0
    for path in tqdm(os.listdir(source_path)):
        if '_7_' in path:
            shutil.copy(os.path.join(source_path, path), os.path.join(result_path, path))
            i = i + 1
    print(file, i)
