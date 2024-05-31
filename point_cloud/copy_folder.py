import shutil
import os

def copy_directory(source, target):
    if os.path.exists(target):
        shutil.rmtree(target)  # 删除目标目录
    shutil.copytree(source, target)

# 定义源目录和目标目录
source_dir = "/mnt/algo-storage-server/Projects/RangeImageSeg/Dataset"
target_dir = "/home/lj/PycharmProjects/RangeImageSeg/Dataset"

# 拷贝文件夹
copy_directory(source_dir, target_dir)
