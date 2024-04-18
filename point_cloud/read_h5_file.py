import h5py
import numpy as np

filename_h5 =r'D:\Projects\PointCloudSeg\Dataset\test_color.h5'

data = h5py.File(filename_h5, 'r')
keys = list(data.keys())
print(keys)

print(type(data['data']))

points = []
labels = []
point_nums = []

points.append(data['data'][...].astype(np.float32))
points.append(data['color'][...].astype(np.float32))
labels.append(data['label'][...].astype(np.int64))
point_nums.append(data['data_num'][...].astype(np.int32))

print(points[0].shape)
print(points[1])
# print(np.concatenate(points, axis=0).shape)
print(labels[0].shape)
print(point_nums[0].shape)
