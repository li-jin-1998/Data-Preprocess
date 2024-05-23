import imageio
import numpy as np
import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.segmaps import SegmentationMapsOnImage

ia.seed(1)

# Load an example image (uint8, 128x128x3).
image = ia.quokka(size=(128, 128), extract="square")

# Define an example segmentation map (int32, 128x128).
# Here, we arbitrarily place some squares on the image.
# Class 0 is our intended background class.
segmap = np.zeros((128, 128, 1), dtype=np.int32)
segmap[28:71, 35:85, 0] = 1
segmap[10:25, 30:45, 0] = 2
segmap[10:25, 70:85, 0] = 3
segmap[10:110, 5:10, 0] = 4
segmap[118:123, 10:110, 0] = 5
segmap = SegmentationMapsOnImage(segmap, shape=image.shape)

p = 0.9
# Define our augmentation pipeline.
seq = iaa.Sequential([
    # iaa.Dropout([0.05, 0.2]),      # drop 5% or 20% of all pixels
    # iaa.Sharpen((0.0, 1.0)),       # sharpen the image
    # iaa.Affine(rotate=(-45, 45)),  # rotate by -45 to 45 degrees (affects segmaps)
    # iaa.ElasticTransformation(alpha=50, sigma=5),  # apply water effect (affects segmaps)
    # iaa.Resize((224, 224)),
    # iaa.Rotate((0, 360)),
    # iaa.Add((-100, 100)),
    iaa.Rot90(1, keep_size=False),
    # iaa.Sometimes(p, iaa.Rotate([90, 180, 270], order=0, fit_output=False)),
    # iaa.Sometimes(p, iaa.AddToSaturation((-8, 8))),
    # iaa.Sometimes(p, iaa.AddToBrightness((-20, 20))),
    # iaa.Sometimes(p, iaa.LinearContrast((0.8, 1.2))),
    iaa.ChangeColorTemperature((3000, 7000)),
    iaa.Sometimes(p, iaa.MultiplyHue((0.8,1.2))),
    # iaa.Multiply((0.8, 1.2), per_channel=0.5)
    # iaa.Fliplr(p),
    # iaa.Flipud(p)
    # iaa.AddToSaturation((-10, 10)),
    # iaa.LinearContrast((0.6, 1.4)),
    # iaa.AddToHue((-100, 100)),
    # iaa.Fliplr(0.5),
], random_order=True)

# Augment images and segmaps.
images_aug = []
segmaps_aug = []
print(image.shape, segmap.shape)
for _ in range(5):
    images_aug_i, segmaps_aug_i = seq(image=image, segmentation_maps=segmap)
    print(images_aug_i.shape, type(segmaps_aug_i))

    images_aug.append(images_aug_i)
    segmaps_aug.append(segmaps_aug_i)

cells = []
for image_aug, segmap_aug in zip(images_aug, segmaps_aug):
    cells.append(image)  # column 1
    cells.append(segmap.draw_on_image(image)[0])  # column 2
    cells.append(image_aug)  # column 3
    cells.append(segmap_aug.draw_on_image(image_aug)[0])  # column 4
    cells.append(segmap_aug.draw(size=image_aug.shape[:2])[0])  # column 5

# Convert cells to a grid image and save.
grid_image = ia.draw_grid(cells, cols=5)
imageio.imwrite("example_segmaps.jpg", grid_image)
