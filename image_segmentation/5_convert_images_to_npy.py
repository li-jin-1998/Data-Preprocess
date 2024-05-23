import os

import cv2
import numpy as np
import tqdm


def preprocess(image_path, mask_path, image_size):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (image_size, image_size), interpolation=cv2.INTER_CUBIC)
    # image = cv2.bilateralFilter(image, 2, 50, 50)  # remove images noise.
    # img = cv2.applyColorMap(img, cv2.COLORMAP_BONE)  # produce a pseudocolored image. 伪彩色
    # image = np.array(image, np.float32)
    # image = image / 127.5 - 1

    mask = cv2.imread(mask_path)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask = cv2.resize(mask, (image_size, image_size), interpolation=cv2.INTER_NEAREST)
    mask[mask == 64.0] = 1.0
    mask[mask == 129.0] = 2.0
    mask[mask == 192.0] = 3.0
    mask[mask == 255.0] = 4.0
    return image, mask


def save_batch(images, masks, batch_index, output_dir):
    images = np.array(images)
    masks = np.array(masks)

    try:
        np.save(os.path.join(output_dir, f'images_batch_{batch_index}.npy'), images)
        np.save(os.path.join(output_dir, f'masks_batch_{batch_index}.npy'), masks)
        print(f'Batch {batch_index} saved successfully.')
    except IOError as e:
        print(f"Error saving data: {e}")


def png_npy(input_dir, image_size=224, batch_size=10000):
    images = []
    masks = []
    batch_index = 0

    # 确保输入目录存在
    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist.")
        return

    image_dir = os.path.join(input_dir, 'image')
    mask_dir = os.path.join(input_dir, 'mask')

    if not os.path.exists(image_dir) or not os.path.exists(mask_dir):
        print(f"Image or mask directory does not exist.")
        return

    # 获取所有图像文件名
    image_paths = sorted(os.listdir(image_dir))

    for i, path in enumerate(tqdm.tqdm(image_paths[::])):
        image_path = os.path.join(image_dir, path)
        mask_path = os.path.join(mask_dir, path.replace("IMAGE", "MASK"))

        if not os.path.exists(image_path) or not os.path.exists(mask_path):
            print(f"Skipping {path}, corresponding mask or image not found.")
            continue

        # 处理图像和掩码
        image, mask = preprocess(image_path, mask_path, image_size=image_size)
        images.append(image)
        masks.append(mask)

        # 每 batch_size 张图像保存为一个 .npy 文件
        if len(images) == batch_size:
            save_batch(images, masks, batch_index, input_dir)
            images = []
            masks = []
            batch_index += 1

    # 保存最后一批图像
    if images:
        save_batch(images, masks, batch_index, input_dir)


if __name__ == '__main__':
    # from parse_args import parse_args

    # args = parse_args()
    data_path = r'/home/lj/PycharmProjects/2D-image-Segmentation/dataset/data'

    train_input_dir = os.path.join(data_path, 'augmentation_train')
    test_input_dir = os.path.join(data_path, 'augmentation_test')

    png_npy(train_input_dir, 224)
    png_npy(test_input_dir, 224)
