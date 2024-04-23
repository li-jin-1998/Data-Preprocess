import argparse
import os
import random
import shutil

from PIL import ImageEnhance
import PIL.Image
import tqdm
from parse_args import parse_args


def enhance_h(image, hue=6):
    image = image.convert('HSV')
    image = image.point(lambda x: (x + hue))
    image = image.convert('RGB')
    return image


def seg_augmentation_old(args, mode='train'):
    input_path = os.path.join(args.dataset_dir, 'data')
    input_dir = os.path.join(input_path, mode)
    augmentation_output_dir = os.path.join(input_path, 'augmentation2_' + mode)
    if os.path.exists(augmentation_output_dir):
        shutil.rmtree(augmentation_output_dir)
    os.mkdir(augmentation_output_dir)
    os.mkdir(os.path.join(augmentation_output_dir, 'image'))
    os.mkdir(os.path.join(augmentation_output_dir, 'mask'))

    for path in tqdm.tqdm(os.listdir(os.path.join(input_dir, 'image'))):
        base = path.split('.')[0]
        image = PIL.Image.open(
            os.path.join(os.path.join(input_dir, 'image'), path))
        mask = PIL.Image.open(
            os.path.join(os.path.join(input_dir, 'mask'), path))
        image.save(os.path.join(augmentation_output_dir, 'image',
                                base + '[ORIGIN].png'))
        mask.save(os.path.join(augmentation_output_dir, 'mask',
                               base + '[ORIGIN].png'))

        image_flr = image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        mask_flr = mask.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        image_flr.save(os.path.join(augmentation_output_dir, 'image',
                                    base + '[FLIP_LEFT_RIGHT].png'))
        mask_flr.save(os.path.join(augmentation_output_dir, 'mask',
                                   base + '[FLIP_LEFT_RIGHT].png'))

        image_ftp = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        mask_ftp = mask.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        image_ftp.save(os.path.join(augmentation_output_dir, 'image',
                                    base + '[FLIP_TOP_BOTTOM].png'))
        mask_ftp.save(os.path.join(augmentation_output_dir, 'mask',
                                   base + '[FLIP_TOP_BOTTOM].png'))
        # 随机旋转图像
        # seed = random.randint(0, 360)
        # image_rot = image.rotate(seed)
        # mask_rot = mask.rotate(seed)
        # image_rot.save(os.path.join(augmentation_output_dir, 'image',
        #                             base + '[ROTATE].png'))
        # mask_rot.save(os.path.join(augmentation_output_dir, 'mask',
        #                            base + '[ROTATE].png'))
        # 随机缩放图像
        # scale = random.uniform(0.8, 1.2)
        # image_scale = image.resize((int(image.width * scale), int(image.height * scale)))
        # mask_scale = mask.resize((int(image.width * scale), int(image.height * scale)))
        # image_scale.save(os.path.join(augmentation_output_dir, 'image',
        #                               base + '[SCALE].png'))
        # mask_scale.save(os.path.join(augmentation_output_dir, 'mask',
        #                              base + '[SCALE].png'))

        # 随机调整亮度
        brightness = ImageEnhance.Brightness(image)
        seed2 = random.uniform(0.8, 1.2)
        bright_image = brightness.enhance(seed2)
        bright_mask = mask
        bright_image.save(os.path.join(augmentation_output_dir, 'image',
                                       base + '[BRIGHT].png'))
        bright_mask.save(os.path.join(augmentation_output_dir, 'mask',
                                      base + '[BRIGHT].png'))

        # 随机调整对比度
        seed3 = random.uniform(0.8, 1.2)
        contrast = ImageEnhance.Contrast(image)
        contrast_image = contrast.enhance(seed3)
        contrast_mask = mask
        contrast_image.save(os.path.join(augmentation_output_dir, 'image',
                                         base + '[ENHANCE].png'))
        contrast_mask.save(os.path.join(augmentation_output_dir, 'mask',
                                        base + '[ENHANCE].png'))

        # 调整色相
        seed4 = random.randint(3, 8)
        h_image = enhance_h(image, seed4)
        h_image.save(os.path.join(augmentation_output_dir, 'image',
                                  base + '[ENHANCE_H].png'))
        mask.save(os.path.join(augmentation_output_dir, 'mask',
                               base + '[ENHANCE_H].png'))

        seed5 = random.randint(-7, -2)
        h_image2 = enhance_h(image, seed5)
        h_image2.save(os.path.join(augmentation_output_dir, 'image',
                                   base + '[ENHANCE_H2].png'))
        mask.save(os.path.join(augmentation_output_dir, 'mask',
                               base + '[ENHANCE_H2].png'))


if __name__ == '__main__':
    args = parse_args()
    seg_augmentation_old(args, 'train')
    seg_augmentation_old(args, 'test')
