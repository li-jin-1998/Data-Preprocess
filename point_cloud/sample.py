import random

# 原始列表
lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(lst[::2])
# 间隔采样
sampled_lst = random.sample(lst, 3)
print(sampled_lst)