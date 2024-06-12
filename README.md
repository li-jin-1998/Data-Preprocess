# [Data-Preprocess](https://github.com/li-jin-1998/Data-Preprocess)

Some deep learning data preprocessing code。

# Preprocessing flow

## 2D Image Segmentation

- [Copy data from original data.](./image_segmentation/1_seg_copy_data.py)
- [Labelme to mask.](./image_segmentation/2_labelme_to_mask.py)
- [Data spilt.](./image_segmentation/3_data_split.py)
- [Data spilt for txt.](./image_segmentation/3_data_split_txt.py)
- [Augmentation.](./image_segmentation/4_seg_augmentation.py)
- [Augmentation for txt.](./image_segmentation/4_seg_augmentation_txt.py)

## Point Cloud Segmentation

- [Copy raw image from original data.](./point_cloud/1_raw_images_copy.py)
- [Transfer to point cloud.](./point_cloud/2_print_command.py)
- [Extract file.](./point_cloud/3_extract_file.py)
- [Data spilt.](./point_cloud/4_data_split.py)
- [Transfer to h5py.](./point_cloud/5_prepare_data.py)

## 2D Image Classification

- [Extract data from original data.](./image_classification/extract_file.py)
- [Data spilt.](./image_classification/data_split_txt.py)
- [Data clean.](./image_classification/data_clean.py)
