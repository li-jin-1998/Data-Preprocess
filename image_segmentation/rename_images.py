import os

# 源文件夹路径
source_folder = r"D:\Projects\UNet\Dataset11\mask"

i = 0
# 遍历源文件夹中的图片文件
for filename in os.listdir(source_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # 构造原始文件路径和新文件路径
        source_file = os.path.join(source_folder, filename)
        new_filename = str(i).rjust(4, '0') + '.png'
        new_file = os.path.join(source_folder, new_filename)
        # 重命名并覆盖源文件
        os.rename(source_file, new_file)
        i = i + 1

print("重命名完成！")
