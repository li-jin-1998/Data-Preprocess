import os
import shutil
import sys

from tqdm import tqdm


def copy_files(src, dst):
    """
    Copy files from src to dst if they meet specific criteria.
    """
    try:
        files = os.listdir(src)
        print(f"Found {len(files)} directories in {src}")
        file_count = 0

        for folder in files:
            folder_path = os.path.join(src, folder)
            if os.path.isdir(folder_path):
                for file in tqdm(os.listdir(folder_path), desc=f"Copying from {folder}", file=sys.stdout):
                    if ("color" in file and file.endswith("tif")) or ("Image" in file and file.endswith("png")):
                        json_file = file.replace('tif', 'json').replace('png', 'json')
                        tif_path = os.path.join(folder_path, file)
                        json_path = os.path.join(folder_path, json_file)
                        if os.path.exists(tif_path) and os.path.exists(json_path):
                            shutil.copy(tif_path, os.path.join(dst, file))
                            shutil.copy(json_path, os.path.join(dst, json_file))
                            file_count += 1
        print(f"Total files copied: {file_count}")
    except Exception as e:
        print(f"Error while copying files: {e}")


def setup_destination_directory(dst):
    """
    Ensure the destination directory exists; create if it doesn't.
    """
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)


def copy_implant():
    src_dirs = [
        r'/mnt/algo-storage-server/Workspaces/fangqi/03_已完成/初始',
        r'/mnt/algo-storage-server/Workspaces/fangqi/03_已完成/00_种植'
    ]
    dst = r"/home/lj/PycharmProjects/Data/Implant2"
    setup_destination_directory(dst)
    for src in src_dirs:
        copy_files(src, dst)


def copy_edentulous():
    src = r'/mnt/algo-storage-server/Workspaces/fangqi/03_已完成/07_无牙颌'
    dst = r"/home/lj/PycharmProjects/Data/Edentulous"
    setup_destination_directory(dst)
    copy_files(src, dst)


def copy_additional():
    src = r'/mnt/algo-storage-server/Workspaces/fangqi/01_待标注/00_种植/0614'
    dst = r"/home/lj/PycharmProjects/Data/add3"
    setup_destination_directory(dst)
    copy_files(src, dst)


if __name__ == '__main__':
    import time

    start_time = time.time()
    # copy_implant()
    # copy_edentulous()
    copy_additional()
    print("--- %s seconds ---" % (time.time() - start_time))
