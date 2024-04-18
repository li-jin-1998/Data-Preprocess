import os
import h5py
import numpy as np
from tqdm import tqdm
import pyvista as pv

from read_ply2 import read_ply


def data_to_h5(txt_file, filename_h5, num=-1):
    file_list = sorted([os.path.join(os.path.dirname(txt_file), 'data', line.strip()) for line in open(txt_file)])[:num]
    max_point_num = 0
    colors = []
    for file in tqdm(file_list):
        # print(file)
        ply_data = read_ply(file.replace('_label', ''))
        colors.append(ply_data[1])
        max_point_num = max(max_point_num, ply_data[2])
    print('max_point_num:', max_point_num)

    batch_size = len(file_list)
    data = np.zeros((batch_size, max_point_num, 3))
    color = np.zeros((batch_size, max_point_num, 3))
    data_num = np.zeros(batch_size, dtype=np.int32)
    label = np.zeros((batch_size, max_point_num), dtype=np.int32)
    for i, file in enumerate(tqdm(file_list)):
        ply_data = read_ply(file, is_label=True)
        data[i, 0:ply_data[3], ...] = np.array(ply_data[0])
        color[i, 0:ply_data[3], ...] = np.array(colors[i])
        data_num[i] = ply_data[3]
        label[i, 0:ply_data[3]] = np.array(ply_data[2])

    print('Saving {}...'.format(filename_h5))
    file = h5py.File(filename_h5, 'w')
    file.create_dataset('data', data=data)
    file.create_dataset('color', data=color)
    file.create_dataset('data_num', data=data_num)
    file.create_dataset('label', data=label)
    file.close()


if __name__ == '__main__':
    dst = r'D:\Projects\PointCloudSeg\Dataset\test_label.txt'
    filename_h5 = r'D:\Projects\PointCloudSeg\Dataset\test_color.h5'
    import time

    start_time = time.time()

    data_to_h5(dst, filename_h5)
    data_to_h5(dst.replace('test', 'train'), filename_h5.replace('test', 'train'))

    end_time = time.time()
    run_time = end_time - start_time
    # 0.1s/per
    print("程序运行时间：", run_time)
