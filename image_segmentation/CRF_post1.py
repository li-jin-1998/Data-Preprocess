import cv2
import matplotlib.pyplot as plt
import numpy as np
import pydensecrf.densecrf as dcrf


def apply_crf(original_image, predicted_prob):
    """
    使用DenseCRF对分割结果进行后处理
    :param original_image: 原始图像，形状为 (H, W, 3)
    :param predicted_prob: 模型预测的概率图，形状为 (H, W, num_classes)
    :return: CRF后处理后的分割结果，形状为 (H, W)
    """
    h, w = original_image.shape[:2]
    num_classes = predicted_prob.shape[-1]

    # 创建DenseCRF模型
    d = dcrf.DenseCRF2D(w, h, num_classes)

    # 准备Unary能量项
    unary = np.moveaxis(predicted_prob, -1, 0)
    unary = -np.log(unary)
    unary = unary.reshape((num_classes, -1))
    unary = unary.copy(order='C').astype(np.float32)
    print(unary.shape)
    d.setUnaryEnergy(unary)

    # 增加颜色独立的边缘项
    d.addPairwiseGaussian(sxy=3, compat=3)

    # 增加颜色依赖的边缘项
    d.addPairwiseBilateral(sxy=80, srgb=13, rgbim=original_image, compat=10)

    # 进行推理
    Q = d.inference(10)

    # 获得最终结果
    map_result = np.argmax(Q, axis=0).reshape((h, w))

    return map_result


# 加载图像和模型预测结果的示例
# 假设original_image是原始图像，predicted_prob是模型预测的概率图
# 读取输入图像和分割结果（假设分割结果是一个概率图）
# 读取示例图像
original_image = cv2.imread(r'/home/lj/PycharmProjects/2D-image-Segmentation/test.png')
original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

# 创建示例预测概率图
# 假设有3个类别，形状为(H, W, num_classes)
H, W, _ = original_image.shape
num_classes = 3
predicted_prob = np.random.rand(H, W, num_classes)

# 应用CRF后处理
crf_result = apply_crf(original_image, predicted_prob)

# 显示结果
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.title("Original Image")
plt.imshow(original_image)
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title("Predicted Prob")
plt.imshow(np.argmax(predicted_prob, axis=-1))
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title("CRF Result")
plt.imshow(crf_result)
plt.axis('off')

plt.show()
