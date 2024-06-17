import os

src = r"/home/lj/PycharmProjects/Data/check2"

dst = "/home/lj/PycharmProjects/2D-Image-Segmentation/dataset"

dst_image_path = os.path.join(dst, "image")
dst_mask_path = os.path.join(dst, "mask")
print(len(os.listdir(dst_mask_path)))

image_paths = [p for p in os.listdir(src) if 'mask' not in p]
print(len(image_paths))
for p in image_paths:
    image_path = os.path.join(dst_image_path, p)
    mask_path = os.path.join(dst_mask_path, p)
    if os.path.exists(image_path) and os.path.exists(mask_path):
        print(image_path, mask_path)
        os.remove(image_path)
        os.remove(mask_path)
