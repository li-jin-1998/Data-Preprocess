import plyfile
import numpy as np

green_to_label = {255: 2, 192: 3, 129: 1, 64: 0}


def read_ply(path):
    # 读取 PLY 文件
    ply_data = plyfile.PlyData.read(path)

    # print(ply_data['vertex'].data)

    points = [ply_data['vertex'].data['x'], ply_data['vertex'].data['y'], ply_data['vertex'].data['z']]
    points = np.array([points[0], points[1], points[2]]).T

    colors = [ply_data['vertex'].data['red'], ply_data['vertex'].data['green'], ply_data['vertex'].data['blue']]
    colors = np.array([colors[0], colors[1], colors[2]]).T
    labels = [green_to_label[i] for i in ply_data['vertex'].data['green']]
    labels = np.array(labels).T

    return points, colors, labels


if __name__ == '__main__':
    import time

    start_time = time.time()
    for i in range(1):
        p, c, l = read_ply('./gt.ply')
    end_time = time.time()

    run_time = end_time - start_time

    # 0.2s/per
    print("程序运行时间：", run_time)

    print(p.shape, c.shape, l.shape)
    for i, j, k in zip(p, c, l):
        print(i, j, k)
