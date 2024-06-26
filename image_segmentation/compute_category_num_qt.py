import json
import os
import shutil
import sys

import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, \
    QLabel, QLineEdit, QCheckBox, QTextEdit, QProgressBar
from tqdm import tqdm

CONFIG_FILE = 'ImageProcessingApp.json'


class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Processing App")
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        self.create_form()
        self.create_output_console()
        self.create_progress_bar()

        self.load_config()

    def create_form(self):
        form_layout = QVBoxLayout()

        self.src_directory_label = QLabel("Source Directory:", self)
        form_layout.addWidget(self.src_directory_label)

        self.src_directory_input = QLineEdit(self)
        form_layout.addWidget(self.src_directory_input)

        self.src_browse_button = QPushButton("Browse", self)
        self.src_browse_button.clicked.connect(self.browse_src_directory)
        form_layout.addWidget(self.src_browse_button)

        self.dst_directory_label = QLabel("Destination Directory:", self)
        form_layout.addWidget(self.dst_directory_label)

        self.dst_directory_input = QLineEdit(self)
        form_layout.addWidget(self.dst_directory_input)

        self.dst_browse_button = QPushButton("Browse", self)
        self.dst_browse_button.clicked.connect(self.browse_dst_directory)
        form_layout.addWidget(self.dst_browse_button)

        self.pixel_value_label = QLabel("Pixel Value:", self)
        form_layout.addWidget(self.pixel_value_label)

        self.pixel_value_input = QLineEdit(self)
        form_layout.addWidget(self.pixel_value_input)

        self.copy_files_checkbox = QCheckBox("Copy Files", self)
        form_layout.addWidget(self.copy_files_checkbox)

        self.process_button = QPushButton("Process", self)
        self.process_button.clicked.connect(self.process_images)
        form_layout.addWidget(self.process_button)

        self.layout.addLayout(form_layout)

    def create_output_console(self):
        self.output_console = QTextEdit(self)
        self.output_console.setReadOnly(True)
        self.layout.addWidget(self.output_console)

    def create_progress_bar(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.progress_bar)

    def log_output(self, message):
        self.output_console.append(message)

    def browse_src_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if directory:
            self.src_directory_input.setText(directory)

    def browse_dst_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
        if directory:
            self.dst_directory_input.setText(directory)

    def process_images(self):
        src_directory = self.src_directory_input.text()
        dst_directory = self.dst_directory_input.text()
        pixel_value = self.pixel_value_input.text()
        is_copy = self.copy_files_checkbox.isChecked()

        if not src_directory:
            self.log_output("Please select a source directory.")
            return

        if is_copy and not dst_directory:
            self.log_output("Please select a destination directory.")
            return

        if not pixel_value.isdigit():
            self.log_output("Please enter a valid pixel value.")
            return

        pixel_value = int(pixel_value)
        self.log_output(f"Starting image processing with pixel value {pixel_value}...")

        if is_copy:
            if os.path.exists(dst_directory):
                shutil.rmtree(dst_directory)
            os.makedirs(dst_directory, exist_ok=True)

        count = 0
        src_files = [entry for entry in os.scandir(src_directory) if entry.is_file() and entry.name.endswith('.png')]
        self.progress_bar.setMaximum(len(src_files))

        for idx, entry in enumerate(tqdm(src_files, desc="Processing masks")):
            mask_path = entry.path
            mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
            if mask is None:
                self.log_output(f"Error reading file: {mask_path}")
                continue
            if pixel_value in mask:
                count += 1
                if is_copy:
                    self.copy_files(mask_path, dst_directory, entry.name)

            self.progress_bar.setValue(idx + 1)

        self.log_output("-" * 100)
        self.log_output(f"Total masks with pixel value {pixel_value}: {count}")
        self.log_output(f"Total masks processed: {len(src_files)}")
        self.log_output("-" * 100)

        self.save_config()

    def copy_files(self, mask_path, dst_directory, file_name):
        shutil.copy(mask_path, os.path.join(dst_directory, file_name.replace('.png', 'mask.png')))
        image_path = mask_path.replace("/mask", "/image")
        shutil.copy(image_path, os.path.join(dst_directory, file_name.replace('.png', 'image.png')))

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                self.src_directory_input.setText(config.get('src_directory', ''))
                self.dst_directory_input.setText(config.get('dst_directory', ''))
                self.pixel_value_input.setText(str(config.get('pixel_value', '')))
                self.copy_files_checkbox.setChecked(config.get('is_copy', False))

    def save_config(self):
        config = {
            'src_directory': self.src_directory_input.text(),
            'dst_directory': self.dst_directory_input.text(),
            'pixel_value': int(self.pixel_value_input.text()) if self.pixel_value_input.text().isdigit() else '',
            'is_copy': self.copy_files_checkbox.isChecked()
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())
