import meshio
import numpy as np

green_to_label = {255: 2, 192: 3, 129: 1, 64: 0}


def read_ply(path):
    mesh = meshio.read(path)
    points = mesh.points
    colors = [mesh.point_data['red'], mesh.point_data['green'], mesh.point_data['blue']]
    colors = np.array([colors[0], colors[1], colors[2]]).T

    labels = [green_to_label[i] for i in mesh.point_data['green']]
    labels = np.array(labels).T

    return points, colors, labels


if __name__ == '__main__':
    import time

    start_time = time.time()
    for i in range(10):
        p, c, l = read_ply('./gt.ply')
    end_time = time.time()

    run_time = end_time - start_time

    # 0.112s/per
    print("程序运行时间：", run_time)
    print(p.shape, c.shape, l.shape)
    # for i, j, k in zip(p, c, l):
    #     print(i, j, k)
