import os
import shutil

from tqdm import tqdm

from parse_args import parse_args


def copy_data(src, dst):
    print("*" * 20)
    print("Copy data.")
    print("*" * 20)
    # files = ['20230314125819-select']
    #
    # for f in os.listdir(src):
    #     print("'"+f+"',")
    #     if "20230228115654" not in f and "bracket" not in f and "implant" not in f:
    #         files.append(f)
    files = os.listdir(src)
    print(len(files), files)
    i = 0

    for p in files:
        # if "bracket" in p or "implant" in p:
        #     continue
        file_path = os.path.join(src, p)
        print(file_path, len(os.listdir(file_path)))
        for p2 in tqdm(os.listdir(file_path)):
            if "color" in p2 and "tif" in p2:
                p3 = p2.replace('tif', 'json')
                tif_path = os.path.join(file_path, p2)
                json_path = os.path.join(file_path, p3)
                if os.path.exists(tif_path) and os.path.exists(json_path):
                    shutil.copy(tif_path, os.path.join(dst, p2))
                    shutil.copy(json_path, os.path.join(dst, p3))
                i = i + 1
    print(i)


if __name__ == '__main__':
    # src = r'D:\Dataset\数据管理_fq\02_待审核\新增扩展区域'
    # src2 = r'D:\Dataset\数据管理_fq\03_已查验\01_内部标注数据\王雅妮'
    # src3 = r'D:\Dataset\数据管理_fq\02_待审核\00_种植'
    src = r'D:\Dataset\数据管理_fq\02_待审核\07_无牙\四次修改_最新'

    args = parse_args()
    dst = args.initial_dir
    # if os.path.exists(dst):
    #     shutil.rmtree(dst)
    # os.mkdir(dst)
    copy_data(src, dst)
    # copy_data(src2, dst)
    # copy_data(src3, dst)
