import os
import shutil
import sys

import cv2
import imgaug as ia
import imgaug.augmenters as iaa
import tqdm
from imgaug.augmentables.segmaps import SegmentationMapsOnImage

from parse_args import parse_args

ia.seed(1)
p = 0.4
# Define our augmentation pipeline.
seq = iaa.Sequential([
    # iaa.Dropout([0.05, 0.2]),      # drop 5% or 20% of all pixels
    # iaa.Sharpen((0.0, 1.0)),       # sharpen the image
    # iaa.Affine(rotate=(-45, 45)),  # rotate by -45 to 45 degrees (affects segmaps)
    # iaa.ElasticTransformation(alpha=50, sigma=5),  # apply water effect (affects segmaps)
    # iaa.Sometimes(p, iaa.ChangeColorTemperature((3000, 7000))),
    # iaa.Resize((224, 224)),
    # iaa.Rotate((0, 360)),
    iaa.Sometimes(p, iaa.Rot90((1, 3), keep_size=False)),
    # iaa.Sometimes(p, iaa.Rotate(90, order=0, fit_output=False)),
    iaa.Sometimes(p, iaa.AddToSaturation((-8, 8))),
    iaa.Sometimes(p, iaa.MultiplyBrightness((0.8, 1.2))),
    iaa.Sometimes(p, iaa.LinearContrast((0.8, 1.2))),
    iaa.Sometimes(p, iaa.AddToHue((-8, 8))),
    iaa.Fliplr(p),
    iaa.Flipud(p)
], random_order=True)


def seg_augmentation(args, mode='train'):
    print("*" * 20)
    print(f"Seg {mode} augmentation.")
    print(f"num: {args.aug_nums}")
    print("*" * 20)
    input_path = os.path.join(args.dataset_dir, 'data')
    txt_file = os.path.join(input_path, mode + '.txt')
    paths = sorted([line.strip() for line in open(txt_file)])
    augmentation_output_dir = os.path.join(input_path, 'augmentation_' + mode)

    if os.path.exists(augmentation_output_dir):
        shutil.rmtree(augmentation_output_dir)
    os.mkdir(augmentation_output_dir)
    os.mkdir(os.path.join(augmentation_output_dir, 'image'))
    os.mkdir(os.path.join(augmentation_output_dir, 'mask'))

    for path in tqdm.tqdm(paths, file=sys.stdout):
        base = path.split('.')[0]
        image_path = os.path.join(os.path.join(args.dataset_dir, 'image'), path)
        mask_path = os.path.join(os.path.join(args.dataset_dir, 'mask'), path)

        shutil.copy(image_path, os.path.join(augmentation_output_dir, 'image',
                                             base + '[ORIGIN][IMAGE].png'))
        shutil.copy(mask_path, os.path.join(augmentation_output_dir, 'mask',
                                            base + '[ORIGIN][MASK].png'))
        if mode == 'test':
            continue
        image = cv2.imread(image_path)
        mask = cv2.imread(mask_path)
        if mask is None or image is None:
            print(image_path)
            continue
        mask = SegmentationMapsOnImage(mask, shape=image.shape)
        for i in range(args.aug_nums):
            image_aug, mask_aug = seq(image=image, segmentation_maps=mask)
            cv2.imwrite(os.path.join(augmentation_output_dir, 'image',
                                     base + '[AUG][{}][IMAGE].png'.format(i)), image_aug)
            cv2.imwrite(os.path.join(augmentation_output_dir, 'mask',
                                     base + '[AUG][{}][MASK].png'.format(i)), mask_aug.get_arr())


if __name__ == '__main__':
    import time

    start_time = time.time()
    args = parse_args()
    args.aug_nums = 2
    seg_augmentation(args, 'train')
    seg_augmentation(args, 'test')
    print("--- %s seconds ---" % (time.time() - start_time))
