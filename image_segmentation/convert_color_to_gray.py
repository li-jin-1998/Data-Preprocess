import os
import shutil

import cv2

# 设置输入和输出文件夹路径
input_folder = r'D:\Projects\UNet\Dataset\image2'
output_folder = r'D:\Projects\UNet\Dataset\implant_1_gray'

# 确保输出文件夹存在，如果不存在则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历输入文件夹中的所有图像文件
for filename in os.listdir(input_folder):
    # 检查文件是否为图像文件（扩展名为.jpg、.png等）
    if filename.endswith('.tif') or filename.endswith('.png'):
        # 构建输入文件的完整路径
        input_path = os.path.join(input_folder, filename)

        # 读取彩色图像
        color_image = cv2.imread(input_path)

        # 将彩色图像转换为灰度图像
        gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

        # 构建输出文件的完整路径
        shutil.copy(os.path.join(input_folder, filename), os.path.join(output_folder, filename))
        output_path = os.path.join(output_folder, filename.replace('.tif', '_gray.tif'))

        # 保存灰度图像到输出文件夹中
        cv2.imwrite(output_path, gray_image)

        print(f'Converted {input_path} to {output_path}')

print('Conversion completed!')
