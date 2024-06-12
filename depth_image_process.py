import cv2
import numpy as np

# 读取深度图像
depth_image = cv2.imread('depth.png', cv2.IMREAD_UNCHANGED)

# 高斯滤波
gaussian_filtered = cv2.GaussianBlur(depth_image, (3, 3), 0) * 5
depth = cv2.GaussianBlur(depth_image, (3, 3), 0)
depth = np.array(depth, np.float32)
depth[depth > 0] = (depth[depth > 0]) / np.max(depth)
depth[depth > 1] = 1
depth[depth < 0] = 0
depth = depth * 255
cv2.imwrite('depth_2.png', depth)

# 均值滤波
mean_filtered = cv2.blur(depth, (3, 3))
print(mean_filtered)

cv2.imwrite('gaussian_filtered.png', gaussian_filtered)
cv2.imwrite('mean_filtered.png', mean_filtered)
