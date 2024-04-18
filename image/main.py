import cv2
import imgaug.augmenters as iaa
import numpy as np
import matplotlib.pyplot as plt

image0 = cv2.imread('test.png')
# 示例图像
image = np.expand_dims(image0, 0)
print(image.shape)
# 创建一些数据增强操作
augmenter = iaa.Sequential([
    iaa.AddToHue((0, 10)),
    # iaa.ChangeColorTemperature((1100, 5000)),
    # iaa.AddToHueAndSaturation((0, 10))

], random_order=True)  # apply augmenters in random order

# 应用数据增强
augmented_images = augmenter.augment_images(image)
print(augmented_images.shape)
# 显示原始图像和增强后的图像
plt.subplot(121)
plt.imshow(cv2.cvtColor(image0, cv2.COLOR_BGR2RGB))
plt.subplot(122)
plt.imshow(cv2.cvtColor(augmented_images[0], cv2.COLOR_BGR2RGB))
plt.show()
