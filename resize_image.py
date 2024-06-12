import cv2
import matplotlib.pyplot as plt
import numpy as np

original_image = cv2.imread(r'/home/lj/PycharmProjects/2D-image-Segmentation/test.png')
original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

resized_image = cv2.resize(original_image, (512, 512), interpolation=cv2.INTER_CUBIC)
print(type(resized_image))
# resized_image = np.array(resized_image, np.float32)

plt.figure(figsize=(15, 5))
plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(original_image)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Resized Image")
plt.imshow(resized_image)
plt.axis('off')

plt.show()