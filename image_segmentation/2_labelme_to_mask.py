import glob
import os
import shutil

import cv2
import labelme
import numpy as np
import tqdm
from parse_args import parse_args


def labelme_to_mask(args):
    print("*" * 20)
    print("Labelme to mask.")
    print("*" * 20)
    input_path = args.initial_dir
    output_path = args.dataset_dir
    if os.path.exists(output_path):
        print('Output directory already exists: ', output_path)
        shutil.rmtree(output_path)
        # sys.exit(1)

    os.makedirs(output_path)

    os.makedirs(os.path.join(output_path, 'image'))
    os.makedirs(os.path.join(output_path, 'mask'))
    class_name_to_id = {'gum': 0, '0': 1, '2': 2, '3': 3, '4': 4}

    json_file_names = glob.glob(os.path.join(input_path, '*.json'))

    image_names = []
    for file_name in tqdm.tqdm(json_file_names):
        # print('Generating test sample from:', file_name)
        label_file = labelme.LabelFile(filename=file_name)
        base = os.path.splitext(os.path.basename(file_name))[0]
        out_img_file = os.path.join(output_path, 'image', base + '.png')
        out_mask_file = os.path.join(output_path, 'mask', base + '.png')
        shutil.copy(file_name.replace('json', 'tif'), out_img_file)
        # with open(out_img_file, 'wb') as f:
        #     f.write(label_file.imageData)
        img = labelme.utils.img_data_to_arr(label_file.imageData)
        lbl, _ = labelme.utils.shapes_to_label(
            img_shape=img.shape,
            shapes=label_file.shapes,
            label_name_to_value=class_name_to_id)
        mask = np.array(lbl)
        mask[mask == 0] = 129
        mask[mask == 1] = 0
        mask[mask == 2] = 255
        mask[mask == 3] = 192
        mask[mask == 4] = 64
        cv2.imwrite(out_mask_file, mask)
        # labelme.utils.lblsave(out_mask_file, lbl)


if __name__ == '__main__':
    args = parse_args()
    labelme_to_mask(args)
