import json
import os
import sys

import numpy as np
from PIL import Image
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QGuiApplication, QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, \
    QListWidget, QGridLayout, QScrollArea, QMessageBox, QFileDialog, QSplitter, QCheckBox, QShortcut, QLineEdit


class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.imageBrowser = parent

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        current_item = self.currentItem()
        if current_item:
            self.imageBrowser.displayImages(current_item)


class ImageBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadLastSettings()

    def initUI(self):
        self.setWindowTitle('图像浏览器')
        self.setGeometry(100, 100, 1200, 900)  # 调整窗口初始大小

        # 主布局
        self.mainLayout = QVBoxLayout()

        # 创建分割器
        self.splitter = QSplitter(Qt.Horizontal)

        # 左侧布局（包含图像显示区域）
        self.leftWidget = QWidget()
        self.leftLayout = QVBoxLayout(self.leftWidget)

        # 文件选择按钮
        self.btnLoadDirectory = QPushButton('打开目录', self)
        self.btnLoadDirectory.clicked.connect(self.loadDirectory)
        self.leftLayout.addWidget(self.btnLoadDirectory)

        # 添加计算开关和指标标签的水平布局
        self.switchLayout = QHBoxLayout()
        self.calcSwitch = QCheckBox('计算Dice和IoU', self)
        self.switchLayout.addWidget(self.calcSwitch)

        self.diceLabel = QLabel('', self)
        self.switchLayout.addWidget(self.diceLabel)
        self.iouLabel = QLabel('', self)
        self.switchLayout.addWidget(self.iouLabel)

        self.leftLayout.addLayout(self.switchLayout)

        # 图像显示区域
        self.imageGrid = QGridLayout()
        self.imageGrid.setSpacing(10)

        self.imageContainer = QWidget()
        self.imageContainer.setLayout(self.imageGrid)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.imageContainer)

        self.leftLayout.addWidget(self.scrollArea)

        # 右侧布局（包含文件列表和指标显示）
        self.rightWidget = QWidget()
        self.rightLayout = QVBoxLayout(self.rightWidget)

        # 显示当前目录的标签
        self.currentDirLabel = QLabel(self)
        self.rightLayout.addWidget(self.currentDirLabel)

        # 搜索框
        self.searchBox = QLineEdit(self)
        self.searchBox.setPlaceholderText('搜索文件...')
        self.searchBox.textChanged.connect(self.filterFiles)
        self.rightLayout.addWidget(self.searchBox)

        self.fileList = CustomListWidget(self)
        self.fileList.itemClicked.connect(self.displayImages)
        self.rightLayout.addWidget(self.fileList)

        # 退出按钮
        self.btnExit = QPushButton('退出', self)
        self.btnExit.clicked.connect(self.close)
        self.rightLayout.addWidget(self.btnExit)

        # 截图按钮
        self.btnScreenshot = QPushButton('截图', self)
        self.btnScreenshot.clicked.connect(self.takeScreenshot)
        self.rightLayout.addWidget(self.btnScreenshot)

        # 将左侧布局和右侧布局添加到分割器
        self.splitter.addWidget(self.leftWidget)
        self.splitter.addWidget(self.rightWidget)

        # 将分割器添加到主布局
        self.mainLayout.addWidget(self.splitter)

        self.setLayout(self.mainLayout)

        # 设置快捷键
        self.shortcutScreenshot = QShortcut(QKeySequence('Ctrl+A'), self)
        self.shortcutScreenshot.activated.connect(self.takeScreenshot)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        super().keyPressEvent(event)

    def loadLastSettings(self):
        # 读取上次保存的窗口几何信息和目录路径
        try:
            with open('settings.json', 'r') as f:
                data = json.load(f)
                self.lastDirectory = data.get('last_directory', os.getcwd())
                self.setGeometry(QRect(*data['geometry']))
                self.splitter.setSizes(data['splitter_sizes'])
                self.currentDirLabel.setText(f"当前目录: {self.lastDirectory}")
        except (FileNotFoundError, KeyError):
            self.lastDirectory = os.getcwd()

    def saveLastSettings(self):
        # 保存当前窗口几何信息和目录路径到JSON文件
        data = {
            'last_directory': self.lastDirectory,
            'geometry': [self.geometry().x(), self.geometry().y(), self.geometry().width(), self.geometry().height()],
            'splitter_sizes': self.splitter.sizes()
        }
        with open('settings.json', 'w') as f:
            json.dump(data, f)

    def loadDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, "选择目录", self.lastDirectory)
        if directory:
            self.lastDirectory = directory
            self.saveLastSettings()

            self.fileList.clear()
            self.imageFiles = []
            for root, _, files in os.walk(directory):
                for file in sorted(files):
                    if file.endswith('image.png'):
                        full_path = os.path.join(root, file)
                        self.imageFiles.append(full_path)
                        self.fileList.addItem(file)  # 只显示文件名而不是完整路径

            self.currentDirLabel.setText(f"当前目录: {directory}")

            # 默认选中第一个文件
            if self.imageFiles:
                self.fileList.setCurrentRow(0)
                self.displayImages(self.fileList.currentItem())
            else:
                QMessageBox.information(self, "信息", "所选目录中没有匹配的图像文件")

    def filterFiles(self):
        filter_text = self.searchBox.text().lower()
        for row in range(self.fileList.count()):
            item = self.fileList.item(row)
            item.setHidden(filter_text not in item.text().lower())

    def displayImages(self, item):
        selected_file = item.text()
        self.clearImages()

        image_types = ['image.png', 'mask.png', 'predict.png']
        col = 0

        image_paths = []  # 存储图像路径

        for image_type in image_types:
            image_path = os.path.join(self.lastDirectory, selected_file.replace('image.png', image_type))
            image_paths.append(image_path)

            if os.path.exists(image_path):
                label = QLabel(self)
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)  # 调整图像大小
                label.setPixmap(pixmap)
                self.imageGrid.addWidget(label, 0, col)  # 将图片显示在第一行
                col += 1

        if self.calcSwitch.isChecked() and len(image_paths) == 3:  # 确保有三张图像且开关开启
            dice_coefficient = calculate_dice(image_paths[1], image_paths[2])
            iou = calculate_iou(image_paths[1], image_paths[2])
            self.diceLabel.setText(f"Dice: {dice_coefficient:.4f}")
            self.iouLabel.setText(f"IoU: {iou:.4f}")
        else:
            self.diceLabel.setText('')
            self.iouLabel.setText('')

    def clearImages(self):
        for i in reversed(range(self.imageGrid.count())):
            widget = self.imageGrid.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def takeScreenshot(self):
        screen = QGuiApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId())
        clipboard = QGuiApplication.clipboard()
        clipboard.setPixmap(screenshot)

        # 保存截图到程序当前目录
        screenshot_path = os.path.join(os.getcwd(), 'screenshot.png')
        screenshot.save(screenshot_path, 'png')

        QMessageBox.information(self, "截图", f"截图已保存到剪切板和当前目录\n{os.getcwd()}")

    def closeEvent(self, event):
        # 在窗口关闭事件中保存设置
        self.saveLastSettings()
        super().closeEvent(event)


def calculate_dice(image1_path, image2_path):
    image1 = Image.open(image1_path).convert('L')
    image2 = Image.open(image2_path).convert('L')

    image1 = np.array(image1)
    image2 = np.array(image2)

    intersection = np.sum((image1 == image2) & (image1 > 0))
    sum_images = np.sum(image1 > 0) + np.sum(image2 > 0)

    dice_coefficient = (2.0 * intersection + 1) / (sum_images + 1)  # 添加平滑因子
    return dice_coefficient


def calculate_iou(image1_path, image2_path):
    image1 = Image.open(image1_path).convert('L')
    image2 = Image.open(image2_path).convert('L')

    image1 = np.array(image1)
    image2 = np.array(image2)

    intersection = np.sum((image1 == image2) & (image1 > 0))
    union = np.sum((image1 > 0) | (image2 > 0))

    iou = (intersection + 1) / (union + 1)  # 添加平滑因子
    return iou


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageBrowser()
    ex.show()
    sys.exit(app.exec_())
