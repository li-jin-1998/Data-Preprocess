import os
import shutil

from tqdm import tqdm


def copy_data(src, dst):
    print("*" * 20)
    print("Copy data.")
    print("*" * 20)
    
    files = os.listdir(src)
    print(len(files), files)
    i = 0

    for p in files:
        file_path = os.path.join(src, p)
        print(file_path, len(os.listdir(file_path)))
        dst_path = os.path.join(dst, p)
        if os.path.exists(dst_path):
            print('The file is existed.', dst_path)
            shutil.rmtree(dst_path)
        os.mkdir(dst_path)
        for p2 in tqdm(os.listdir(file_path)):
            if "tif" in p2:
                shutil.copy(os.path.join(file_path, p2), os.path.join(dst_path, p2))
                # print(os.path.join(file_path, p2), os.path.join(dst, p, p2))
                i = i + 1
    print(i)


if __name__ == '__main__':
    src = r'D:\Dataset\2D'

    dst = r'D:\Projects\PointCloudSeg\raw_images'
    # if os.path.exists(dst):
    #     shutil.rmtree(dst)
    # os.mkdir(dst)
    copy_data(src, dst)
