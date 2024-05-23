import os

'''
@echo off

CALL   cls

CALL chcp 65001

CALL capture_test.exe --input-dir="./images"

echo done!

pause

EXIT /B
'''

src = r'D:\Projects\PointCloudSeg\raw_images'

# 打开文件，'w' 表示以写入模式打开文件，如果文件已存在则会清空内容
with open(r'C:\Users\Data\Desktop\capture3.0\example.bat', 'w') as file:
    # 写入内容
    file.write('@echo off\n\n')
    file.write('CALL   cls\n\n')
    file.write('CALL chcp 65001\n\n')

    for p in os.listdir(src):
        s = "CALL capture_test.exe --input-dir=\"" + os.path.join(src, p) + "\"\n\n"
        file.write(s)
        file.write('echo ' + p + ' done!\n\n')
    file.write('pause\n\n')
    file.write('EXIT /B\n\n')
