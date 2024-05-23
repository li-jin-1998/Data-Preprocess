import os
import shutil

root_dir = "root"

folder_list = os.listdir(root_dir)
segment_path = "segment_result"

for folder in folder_list:
    folder_path = os.path.join(root_dir, folder)
    file_list = os.listdir(folder_path)
    new_folder = os.path.join(folder_path, segment_path)
    os.makedirs(new_folder)
    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        target_path = os.path.join(new_folder, filename)
        shutil.move(file_path, target_path)
        print("ori:{}  to  {}".format(file_path,target_path))
