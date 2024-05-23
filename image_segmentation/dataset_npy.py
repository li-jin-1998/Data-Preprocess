import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.utils.data import Dataset

torch.manual_seed(3407)  # reproducible


class MyDataset(Dataset):
    def __init__(self, image_path, mask_path):
        self.images = torch.tensor(np.load(image_path))  # 加载npy数据
        self.masks = torch.tensor(np.load(mask_path))
        # self.transforms = transform  # 转为tensor形式

    def __getitem__(self, index):
        image = self.images[index, :, :, :]  # 读取每一个npy的数据
        image = image.permute(2, 0, 1)
        image = np.array(image, np.float32)
        image = image / 127.5 - 1

        mask = self.masks[index, :, :]
        # mask=self.transforms(mask)
        return image, mask

    def __len__(self):
        return self.images.shape[0]


def compute_weights(masks_path):
    # calculate the weights of different classes based on train samples
    masks = np.load(masks_path)
    max_value = np.max(masks)
    sum_total = 0
    sum = np.zeros(max_value)
    for i in range(max_value):
        sum[i] = np.sum(masks == i)
        sum_total += sum[i]
    print(sum)
    weights_list = []
    for s in sum:
        weights_list.append((1 / s) * sum_total)
    print('Weights for different classes are:', weights_list)


def plot_data_loader_image(data_loader):
    plot_num = data_loader.batch_size

    for image, target in data_loader:
        plot_images = []
        plot_masks = []
        for i in range(plot_num):
            img = image[i].numpy().transpose(1, 2, 0)
            img = (img + 1) * 127.5
            # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img = np.uint8(img)

            plot_masks.append(target[i])
            plot_images.append(img)

        fig, axes = plt.subplots(plot_num // 2, 4, figsize=(8, 8))
        axes = axes.flatten()
        j = 0
        for img, lab in zip(plot_images, plot_masks):
            axes[j].imshow(img)
            axes[j].axis("off")
            axes[j + 1].imshow(lab)
            axes[j + 1].axis("off")
            j += 2
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    from parse_args import parse_args

    args = parse_args()

    images_npy_path = os.path.join(args.data_path, 'augmentation_train',
                                   'images_batch_0.npy')
    masks_npy_path = os.path.join(args.data_path, 'augmentation_train',
                                  'masks_batch_0.npy')

    # data = np.load(masks_npy_path)
    # print(data.shape)

    dataset = MyDataset(images_npy_path, masks_npy_path)
    data = torch.utils.data.DataLoader(dataset, batch_size=8, shuffle=True)
    plot_data_loader_image(data)
    # for image, target in data:
    #     print(image.shape, target.shape)

    # compute_weights(masks_npy_path)
