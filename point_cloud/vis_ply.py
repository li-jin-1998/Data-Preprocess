import os
import glob
import random

import pyvista as pv


def display_multi_meshes(meshes: list, titles=None, point_size=3, opacity=1.0):
    num = len(meshes)
    for i in range(num):
        pl.subplot(0, i)
        if i == num - 1:
            pl.add_checkbox_button_widget(toggle_vis, position=(500.0, 20.0), value=True)

        if titles is not None:
            pl.add_title(titles[i], font_size=20, font='times')
        pl.show_axes()
        pl.add_mesh(meshes[i], point_size=point_size, scalars=meshes[i].active_scalars, style="points", rgb=True,
                    opacity=opacity, show_scalar_bar=False)
        pl.view_xy()
    pl.show()


def toggle_vis(flag=0):
    pl.clear()
    case_id = random.randint(0, len(gts))

    gt_path = os.path.join(gts[case_id])
    print('Test case:', gt_path)

    src_path = gt_path.replace('_label', '')
    meshes = []

    titles = ["Src", "Gt"]
    paths = [src_path, gt_path]

    for path in paths:
        meshes.append(pv.read(path))
    display_multi_meshes(meshes, titles)


if __name__ == '__main__':
    result_paths = glob.glob(r'D:\Projects\PointCloudSeg\Dataset\data\*')
    print(len(result_paths))
    gts = [p for p in result_paths if 'label' in p]

    pl = pv.Plotter(shape=(1, 2))
    pl.set_background([0.9, 0.9, 0.9])
    toggle_vis(0)