import numpy as np


def random_sample(num_points, num_choices):
    # 如果选取的数目大于可选数目，使用抽样方法
    if num_choices > num_points:
        # 随机抽样，确保选取的数字不会重复
        # indices = np.random.choice(num_points, size=num_points, replace=False)
        indices = np.arange(0, num_points)
        # 如果需要重复抽样直到满足选取数目的条件，可以使用以下代码
        indices = np.concatenate([indices, np.random.choice(num_points, size=num_choices - num_points, replace=True)])
    else:
        # 如果可选数目大于等于选取的数目，直接进行随机选择
        indices = np.random.choice(num_points, size=num_choices, replace=False)
    return indices


# 定义数字序列
array = np.array([1, 2, 3, 4, 5, 8, 2])

# 选取的数目
num_choices = 12
indices = random_sample(len(array), num_choices)
print(indices)
print(array[indices])
print(np.unique(indices))
