import pyvista as pv
import numpy as np

green_to_label = {255: 2, 192: 3, 129: 1, 64: 0}


def read_ply(path, is_label=False):
    mesh = pv.read(path)
    # print(mesh.n_points)
    points = mesh.points
    colors = mesh.active_scalars
    if is_label:
        labels = [green_to_label[i[1]] for i in colors]
        labels = np.array(labels).T

        # return {'points': points, 'colors': colors, 'labels': labels, 'num_points': mesh.n_points}
        return points, colors, labels, mesh.n_points
    else:
        return points, colors, mesh.n_points


if __name__ == '__main__':
    import time

    start_time = time.time()
    for i in range(10):
        p = read_ply('./gt.ply')
    end_time = time.time()

    run_time = end_time - start_time

    # 0.1s/per
    print("程序运行时间：", run_time)
    # print(p.shape, c.shape, l.shape)
    # for i, j, k in zip(p, c, l):
    #     print(i, j, k)
