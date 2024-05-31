import os
import shutil
import sys

from tqdm import tqdm

from parse_args import parse_args


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
        for p2 in tqdm(os.listdir(file_path), file=sys.stdout):
            if "color" in p2 and "tif" in p2:
                p3 = p2.replace('tif', 'json')
                tif_path = os.path.join(file_path, p2)
                json_path = os.path.join(file_path, p3)
                if os.path.exists(tif_path) and os.path.exists(json_path):
                    shutil.copy(tif_path, os.path.join(dst, p2))
                    shutil.copy(json_path, os.path.join(dst, p3))
                    i = i + 1
    print(i)


def copy_implant():
    src = r'/mnt/algo-storage-server/Workspaces/fangqi/03_已完成/初始'
    src2 = r'/mnt/algo-storage-server/Workspaces/fangqi/03_已完成/00_种植'

    # args = parse_args()
    # dst = args.data_dir
    dst = r"/home/lj/PycharmProjects/Data/Implant"

    # if os.path.exists(dst):
    #     shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)
    copy_data(src, dst)
    copy_data(src2, dst)


def copy_edentulous():
    src = r'/mnt/algo-storage-server/Workspaces/fangqi/03_已完成/07_无牙颌'

    # args = parse_args()
    # dst = args.data_dir
    dst = r"/home/lj/PycharmProjects/Data/Edentulous"
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)
    copy_data(src, dst)

def copy_additional():
    src = r'/mnt/algo-storage-server/Workspaces/fangqi/02_待审核/add_low_data'

    dst = r"/home/lj/PycharmProjects/Data/add"
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)
    copy_data(src, dst)


if __name__ == '__main__':
    # copy_implant()
    # copy_edentulous()
    copy_additional()
