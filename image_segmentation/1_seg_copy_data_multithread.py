import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm


def copy_file(tif_path, json_path, dst):
    """
    Copy a single image and its corresponding JSON file to the destination directory.
    """
    try:
        shutil.copy(tif_path, os.path.join(dst, os.path.basename(tif_path)))
        shutil.copy(json_path, os.path.join(dst, os.path.basename(json_path)))
        return 1
    except Exception as e:
        print(f"Error while copying files: {e}")
        return 0


def copy_files(src, dst, max_workers=4):
    """
    Copy files from src to dst if they meet specific criteria using multiple threads.
    """
    try:
        files = os.listdir(src)
        print(f"Found {len(files)} directories in {src}")
        file_count = 0
        tasks = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for folder in files:
                folder_path = os.path.join(src, folder)
                if os.path.isdir(folder_path):
                    file_list = os.listdir(folder_path)
                    for file in tqdm(file_list, desc=f"Copying from {folder}", file=sys.stdout):
                        if ("color" in file and file.endswith("tif")) or ("Image" in file and file.endswith("png")):
                            json_file = file.replace('tif', 'json').replace('png', 'json')
                            tif_path = os.path.join(folder_path, file)
                            json_path = os.path.join(folder_path, json_file)
                            if os.path.exists(tif_path) and os.path.exists(json_path):
                                tasks.append(executor.submit(copy_file, tif_path, json_path, dst))

            for future in tqdm(as_completed(tasks), total=len(tasks), desc="Processing files", file=sys.stdout):
                file_count += future.result()

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
    dst = r"/home/lj/PycharmProjects/Data/Implant3"
    setup_destination_directory(dst)
    for src in src_dirs:
        copy_files(src, dst, max_workers=8)


def copy_edentulous():
    src = r'/mnt/algo-storage-server/Workspaces/fangqi/03_已完成/07_无牙颌'
    dst = r"/home/lj/PycharmProjects/Data/Edentulous2"
    setup_destination_directory(dst)
    copy_files(src, dst, max_workers=8)


def copy_additional():
    src = r'/mnt/algo-storage-server/Workspaces/fangqi/01_待标注/00_种植/0614'
    dst = r"/home/lj/PycharmProjects/Data/add3"
    setup_destination_directory(dst)
    copy_files(src, dst, max_workers=8)


if __name__ == '__main__':
    import time

    start_time = time.time()
    # copy_implant()
    copy_edentulous()
    # copy_additional()
    print(f"--- {time.time() - start_time:.2f} seconds ---")
