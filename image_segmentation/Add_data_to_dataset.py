import os
import shutil
import sys

from tqdm import tqdm


def copy_files(src_dir, dst_dir, file_extension=".png"):
    """
    Copy files from source directory to destination directory.

    :param src_dir: Source directory.
    :param dst_dir: Destination directory.
    :param file_extension: File extension to filter files. Default is ".png".
    """
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)

    files_to_copy = [f for f in os.listdir(src_dir) if f.endswith(file_extension)]

    for file in tqdm(files_to_copy, desc=f"Copying files from {src_dir} to {dst_dir}", file=sys.stdout):
        src_path = os.path.join(src_dir, file)
        dst_path = os.path.join(dst_dir, file)
        try:
            shutil.copy(src_path, dst_path)
        except Exception as e:
            print(f"Error copying {src_path} to {dst_path}: {e}")


def main():
    src_base_dir = "/home/lj/PycharmProjects/2D-Image-Segmentation/dataset2"
    dst_base_dir = "/home/lj/PycharmProjects/2D-Image-Segmentation/dataset"

    copy_files(os.path.join(src_base_dir, "image"), os.path.join(dst_base_dir, "image"))
    copy_files(os.path.join(src_base_dir, "mask"), os.path.join(dst_base_dir, "mask"))


if __name__ == "__main__":
    main()
