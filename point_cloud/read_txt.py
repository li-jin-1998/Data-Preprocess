def read_text_list(file_path):
    # 打开文件并读取内容
    with open(file_path, 'r') as f:
        content = f.readlines()
    # 关闭文件
    f.close()
    return content


if __name__ == '__main__':
    dst = r'D:\Projects\PointCloudSeg\Dataset\train.txt'
    text_list = read_text_list(dst)
    # print(text_list)
    # for line in text_list:
    #     print(line.strip())

    import os

    print([os.path.join(os.path.dirname(dst), 'data', line.strip()) for line in open(dst)])
