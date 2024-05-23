import os

name = '有异物'
new_name = 'et_06'
# 源文件夹路径
folder = r"D:\Dataset\数据管理_fq\02_待审核\07_无牙\四次修改_最新"

source_folder = os.path.join(folder, name)

i = 0
# 遍历源文件夹中的图片文件
for filename in os.listdir(source_folder):
    if name in filename:
        # 构造原始文件路径和新文件路径
        source_file = os.path.join(source_folder, filename)
        new_filename = filename.replace(name, new_name)
        new_file = os.path.join(source_folder, new_filename)
        print(source_file, new_file)
        # 重命名并覆盖源文件
        os.rename(source_file, new_file)
        i = i + 1
if os.path.exists(os.path.join(folder, new_name)):
    exit(1)
os.rename(source_folder, os.path.join(folder, new_name))
print("重命名完成！")
