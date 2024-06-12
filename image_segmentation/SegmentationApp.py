import glob
import json
import os
import shutil
import sys
import time

import cv2
import labelme
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QFileDialog, QProgressBar, QDesktopWidget, QTextEdit


class WorkerThread(QThread):
    progress_updated = pyqtSignal(int)
    runtime_updated = pyqtSignal(float)
    operation_finished = pyqtSignal(str, float)
    operation_error = pyqtSignal(str)

    def __init__(self, operation, directories=None, output_panel=None):
        super().__init__()
        self.operation = operation
        self._is_running = True
        self.directories = directories
        self.output_panel = output_panel

    def run(self):
        try:
            self.execute_operation()
        except Exception as e:
            self.operation_error.emit(str(e))

    def execute_operation(self):
        if self.operation == "Labelme to mask":
            src = self.directories[0]
            dst = self.directories[1]
            self.simulate_labelme_to_mask(src, dst)
        elif self.operation == "Data split":
            self.simulate_data_split()
        elif self.operation == "Augmentation":
            self.simulate_augmentation()

    def simulate_labelme_to_mask(self, input_path, output_path):
        print(f"Converting {input_path} to {output_path}")
        if os.path.exists(output_path):
            print(f"Output directory {output_path} already exists. Deleting it...")
            # shutil.rmtree(output_path)
        os.makedirs(output_path, exist_ok=True)
        os.makedirs(os.path.join(output_path, 'image'), exist_ok=True)
        os.makedirs(os.path.join(output_path, 'mask'), exist_ok=True)
        class_name_to_id = {'gum': 0, '0': 1, '2': 2, '3': 3, '4': 4}

        json_file_names = glob.glob(os.path.join(input_path, '*.json'))
        start_time = time.time()
        for i, file_name in enumerate(json_file_names):
            # print(f"Processing {file_name}...")
            if not self._is_running:
                return

            base = os.path.splitext(os.path.basename(file_name))[0]
            out_img_file = os.path.join(output_path, 'image', base + '.png')
            out_mask_file = os.path.join(output_path, 'mask', base + '.png')
            # if os.path.exists(out_mask_file):
            #     continue

            label_file = labelme.LabelFile(filename=file_name)
            img = labelme.utils.img_data_to_arr(label_file.imageData)
            try:
                lbl, _ = labelme.utils.shapes_to_label(
                    img_shape=img.shape,
                    shapes=label_file.shapes,
                    label_name_to_value=class_name_to_id)
                mask = np.array(lbl)
                mask[mask == 0] = 129
                mask[mask == 1] = 0
                mask[mask == 2] = 255
                mask[mask == 3] = 192
                mask[mask == 4] = 64
                cv2.imwrite(out_mask_file, mask)
                shutil.copy(file_name.replace('json', 'tif'), out_img_file)

                elapsed_time = time.time() - start_time
                self.runtime_updated.emit(elapsed_time)
                self.progress_updated.emit(int((i + 1) / len(json_file_names) * 100))

            except Exception as e:
                self.operation_error.emit(str(e))

        elapsed_time = time.time() - start_time
        self.operation_finished.emit(self.operation, elapsed_time)

    def simulate_data_split(self):
        start_time = time.time()
        for i in range(101):
            if not self._is_running:
                return
            elapsed_time = time.time() - start_time
            self.runtime_updated.emit(elapsed_time)
            self.progress_updated.emit(i)
            self.msleep(10)
        elapsed_time = time.time() - start_time
        self.operation_finished.emit(self.operation, elapsed_time)

    def simulate_augmentation(self):
        start_time = time.time()
        for i in range(101):
            if not self._is_running:
                return
            elapsed_time = time.time() - start_time
            self.runtime_updated.emit(elapsed_time)
            self.progress_updated.emit(i)
            self.msleep(10)
        elapsed_time = time.time() - start_time
        self.operation_finished.emit(self.operation, elapsed_time)

    def stop(self):
        self._is_running = False


class FileOperationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Segmentation App")

        # Set initial position to the center of the screen
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen.width() // 2 - 450, screen.height() // 2 - 100, 900, 400)

        self.default_directories = self.load_default_directories()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.directory_layouts = []
        directories = ["data_dir", "dataset_dir"]
        # Add directory input fields
        for i in range(len(directories)):
            directory_layout = QHBoxLayout()
            label = QLabel(f"{directories[i]} :")
            directory_layout.addWidget(label)
            directory_input = QLineEdit(self.default_directories[i])
            directory_input.editingFinished.connect(self.save_default_directories)
            directory_layout.addWidget(directory_input)
            browse_button = QPushButton("Browse")
            browse_button.clicked.connect(lambda state, line_edit=directory_input: self.browse_directory(line_edit))
            directory_layout.addWidget(browse_button)
            self.directory_layouts.append(directory_layout)
            self.layout.addLayout(directory_layout)

        # Add confirmation button
        confirm_button = QPushButton("Confirm Directories")
        confirm_button.clicked.connect(self.confirm_directories)
        self.layout.addWidget(confirm_button)

        # Add output panel
        self.output_panel = QTextEdit()
        self.layout.addWidget(self.output_panel)

        # Add buttons and progress bars
        self.operation_widgets = []
        operations = ["Labelme to mask", "Data split", "Augmentation"]
        for operation in operations:
            operation_layout = QHBoxLayout()
            button = QPushButton(operation)
            button.setFixedWidth(150)  # Set fixed width for buttons
            button.clicked.connect(lambda state, p_operation=operation: self.perform_operation(p_operation))
            operation_layout.addWidget(button)
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            operation_layout.addWidget(progress_bar)
            stop_button = QPushButton("Stop")
            stop_button.setEnabled(False)  # Initially disabled
            stop_button.clicked.connect(lambda state, p_operation=operation: self.stop_operation(p_operation))
            operation_layout.addWidget(stop_button)
            runtime_label = QLabel("0.00 s")
            operation_layout.addWidget(runtime_label)
            self.operation_widgets.append((button, progress_bar, stop_button, runtime_label))
            self.layout.addLayout(operation_layout)

        # Add exit button
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(QApplication.instance().quit)
        self.layout.addWidget(exit_button)

        # Add stretch to center-align buttons
        self.layout.addStretch(1)

        self.threads = {}

    def browse_directory(self, line_edit):
        current_directory = line_edit.text()
        if current_directory:
            parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
        else:
            parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

        directory = QFileDialog.getExistingDirectory(self, "Select Directory", parent_directory)
        if directory:
            line_edit.setText(directory)
            self.save_default_directories()

    def confirm_directories(self):
        # Stop all running threads
        for operation, thread in self.threads.items():
            if thread.isRunning():
                thread.stop()
                thread.wait()

        # Reset all operation widgets
        for button, progress_bar, stop_button, runtime_label in self.operation_widgets:
            button.setEnabled(True)
            progress_bar.setValue(0)
            stop_button.setEnabled(False)
            runtime_label.setText("0.00 s")

        directories = [layout.itemAt(1).widget().text() for layout in self.directory_layouts]
        self.output_panel.append(f"Current Directories:\nData Directory: {directories[0]}\nDataset Directory: {directories[1]}")
        self.default_directories = directories

    def perform_operation(self, operation):
        button, progress_bar, stop_button, runtime_label = next(
            widget for widget in self.operation_widgets if widget[0].text() == operation
        )
        button.setEnabled(False)
        stop_button.setEnabled(True)

        progress_bar.setValue(0)  # Reset progress bar

        thread = WorkerThread(operation, directories=self.default_directories, output_panel=self.output_panel)
        thread.progress_updated.connect(progress_bar.setValue)
        thread.runtime_updated.connect(lambda runtime: self.update_runtime(runtime, runtime_label))
        thread.operation_finished.connect(self.operation_finished)
        thread.operation_error.connect(self.handle_operation_error)
        self.threads[operation] = thread
        thread.start()

    def stop_operation(self, operation):
        thread = self.threads.get(operation)
        if thread:
            thread.stop()
            self.operation_finished(operation)

    @pyqtSlot(str, float)
    def operation_finished(self, operation, runtime):
        button, progress_bar, stop_button, runtime_label = next(
            widget for widget in self.operation_widgets if widget[0].text() == operation
        )
        button.setEnabled(True)
        stop_button.setEnabled(False)
        self.output_panel.append(f"{operation} finished in {runtime:.2f} seconds")

    @pyqtSlot(str)
    def handle_operation_error(self, error_message):
        self.output_panel.append(f"Error: {error_message}")

    def update_runtime(self, runtime, runtime_label):
        runtime_label.setText(f"{runtime:.2f} s")

    def load_default_directories(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
            return config["default_directories"]
        except FileNotFoundError:
            return ["", ""]

    def save_default_directories(self):
        directories = [layout.itemAt(1).widget().text() for layout in self.directory_layouts]
        config = {"default_directories": directories}
        with open("config.json", "w") as f:
            json.dump(config, f)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOperationWindow()
    window.show()
    app.aboutToQuit.connect(window.save_default_directories)
    sys.exit(app.exec_())
