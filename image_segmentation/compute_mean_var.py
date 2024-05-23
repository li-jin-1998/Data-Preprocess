from PIL import Image
import numpy as np
from tqdm import tqdm


def get_files(dir):
    import os
    if not os.path.exists(dir):
        return []
    if os.path.isfile(dir):
        return [dir]
    result = []
    for subdir in os.listdir(dir):
        sub_path = os.path.join(dir, subdir)
        result += get_files(sub_path)
    return result


r = 0  # r mean
g = 0  # g mean
b = 0  # b mean

r_2 = 0  # r^2
g_2 = 0  # g^2
b_2 = 0  # b^2

total = 0
path = r'D:\Projects\UNet\Dataset8\data\train\image'
files = get_files(path)
count = len(files)

for image_file in tqdm(files):
    img = Image.open(image_file)
    img = img.resize((224, 224))
    img = np.asarray(img)
    img = img.astype('float32') / 255.
    total += img.shape[0] * img.shape[1]

    r += img[:, :, 0].sum()
    g += img[:, :, 1].sum()
    b += img[:, :, 2].sum()

    r_2 += (img[:, :, 0] ** 2).sum()
    g_2 += (img[:, :, 1] ** 2).sum()
    b_2 += (img[:, :, 2] ** 2).sum()

r_mean = r / total
g_mean = g / total
b_mean = b / total

r_var = r_2 / total - r_mean ** 2
g_var = g_2 / total - g_mean ** 2
b_var = b_2 / total - b_mean ** 2

print(path)
print('Mean is %s' % ([r_mean, g_mean, b_mean]))
print('Var is %s' % ([r_var, g_var, b_var]))
# Mean is [0.714666137812296, 0.45717883891661787, 0.39560794981912767]
# Var is [0.03108076526638215, 0.016456651595157634, 0.015651226655846645]