import json
import os
import re
import sys

import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QHBoxLayout, QFileDialog, \
    QMessageBox, QListWidget, QListWidgetItem, QVBoxLayout, QSplitter, QToolBar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# 全局变量用于存储配置文件路径
CONFIG_FILE = 'PlotLossApp.json'


# 从txt文件读取数据
def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        data_text = file.read()
    return data_text


# 自定义列表控件
class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    # 设置目录并加载txt文件列表
    def set_directory(self, directory):
        self.clear()
        file_list = [file for file in os.listdir(directory) if file.endswith('.txt')]
        for file_name in sorted(file_list):
            item = QListWidgetItem(file_name)
            self.addItem(item)


# 主绘图窗口类
class PlotWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file_path = None

        self.figure = plt.figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def plot_data(self, file_path):
        data_text = read_txt_file(file_path)
        self.current_file_path = file_path

        train_loss_values = []
        val_loss_values = []

        matches = re.findall(r'train_loss: ([\d.]+)\nval_loss: ([\d.]+)', data_text)

        for match in matches:
            train_loss_values.append(float(match[0]))
            val_loss_values.append(float(match[1]))

        # 清空绘图区域
        self.figure.clear()

        # 绘制折线图
        ax = self.figure.add_subplot(111)
        ax.plot(train_loss_values, marker='o', linestyle='-', color='b', label='Train Loss')
        ax.plot(val_loss_values, marker='o', linestyle='-', color='r', label='Val Loss')
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Loss')
        ax.set_title('Training and Validation Loss')
        ax.legend()
        ax.grid(True)
        self.canvas.draw()

    def save_plot(self):
        if self.current_file_path:
            png_file_path = self.current_file_path.replace('.txt', '.png')
            self.figure.savefig(png_file_path)
            QMessageBox.information(self, "Saved", f"Plot saved as {png_file_path}")


# 主窗口类
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置默认窗口大小和位置
        self.default_width = 800
        self.default_height = 600
        self.resize(self.default_width, self.default_height)
        self.center()

        # 加载配置文件
        self.load_config()

        # 创建状态栏
        self.statusBar = self.statusBar()
        self.statusBar.showMessage('Ready')

        # 创建中央部件并设置布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # 创建分割器
        self.splitter = QSplitter(Qt.Horizontal)

        # 创建绘图窗口
        self.plot_window = PlotWindow(self)
        self.splitter.addWidget(self.plot_window)

        # 创建文件列表视图
        self.file_list_widget = CustomListWidget(self)
        self.file_list_widget.itemClicked.connect(self.open_file_from_list)
        self.splitter.addWidget(self.file_list_widget)

        self.layout.addWidget(self.splitter)

        # 创建菜单栏
        self.create_menu()

        # 创建工具栏
        self.create_toolbar()

    # 创建菜单栏
    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_dir_action = QAction('Open Directory', self)
        open_dir_action.setShortcut('Ctrl+D')
        open_dir_action.triggered.connect(self.open_directory)
        file_menu.addAction(open_dir_action)

    # 创建工具栏
    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        save_plot_action = QAction('Save Plot', self)
        save_plot_action.setShortcut('Ctrl+S')
        save_plot_action.triggered.connect(self.plot_window.save_plot)
        toolbar.addAction(save_plot_action)

    # 打开目录选择文件
    def open_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Open Directory", self.last_open_dir)
        if directory:
            self.last_open_dir = directory
            self.file_list_widget.set_directory(directory)
            self.save_config()  # 保存配置文件
            self.statusBar.showMessage(f'Directory opened: {directory}')

    # 打开列表中的文件
    def open_file_from_list(self, item):
        file_name = item.text()
        file_path = os.path.join(self.last_open_dir, file_name)
        self.plot_window.plot_data(file_path)
        self.statusBar.showMessage(f'File opened: {file_path}')

    # 加载配置文件
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                self.last_open_dir = config.get('last_open_dir', '')
                self.resize(config.get('window_width', self.default_width),
                            config.get('window_height', self.default_height))
                self.move(config.get('window_position_x', 0), config.get('window_position_y', 0))
        else:
            self.last_open_dir = ''
            self.resize(self.default_width, self.default_height)
            self.center()

    # 保存配置文件
    def save_config(self):
        config = {
            'last_open_dir': self.last_open_dir,
            'window_width': self.width(),
            'window_height': self.height(),
            'window_position_x': self.x(),
            'window_position_y': self.y()
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)

    # 窗口居中显示
    def center(self):
        screen = QApplication.primaryScreen()
        screen_size = screen.availableSize()
        self.move((screen_size.width() - self.width()) // 2, (screen_size.height() - self.height()) // 2)


# 主程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
