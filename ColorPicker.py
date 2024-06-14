import sys
import pyautogui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QColorDialog, QTextEdit
from PyQt5.QtGui import QColor, QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt, QTimer


class ColorPickerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Color Picker")
        self.setGeometry(100, 100, 400, 300)
        self.center()

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Color display label
        self.color_label = QLabel(self)
        self.color_label.setFixedSize(100, 100)
        self.color_label.setStyleSheet("background-color: white;")
        self.layout.addWidget(self.color_label, alignment=Qt.AlignCenter)

        # RGB value label
        self.rgb_label = QLabel("RGB: (255, 255, 255)", self)
        self.layout.addWidget(self.rgb_label, alignment=Qt.AlignCenter)

        # HEX value label
        self.hex_label = QLabel("HEX: #FFFFFF", self)
        self.layout.addWidget(self.hex_label, alignment=Qt.AlignCenter)

        # Pick color button
        self.pick_color_button = QPushButton("Pick Color from Dialog", self)
        self.pick_color_button.clicked.connect(self.open_color_dialog)
        self.layout.addWidget(self.pick_color_button, alignment=Qt.AlignCenter)

        # Pick screen color button
        self.pick_screen_color_button = QPushButton("Pick Color from Screen", self)
        self.pick_screen_color_button.clicked.connect(self.activate_color_picker_mode)
        self.layout.addWidget(self.pick_screen_color_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

        self.picking_color = False
        self.mouse_pos = None

    def center(self):
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        self.move((rect.width() - self.width()) // 2, (rect.height() - self.height()) // 2)

    def open_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.update_color_display(color)

    def activate_color_picker_mode(self):
        self.hide()
        self.picking_color = True
        self.setMouseTracking(True)  # 开启鼠标跟踪
        QTimer.singleShot(500, self.show)

    def mouseMoveEvent(self, event):
        if self.picking_color:
            self.mouse_pos = event.pos()
            self.update()

    def mousePressEvent(self, event):
        if self.picking_color:
            self.picking_color = False
            x, y = self.mouse_pos.x(), self.mouse_pos.y()
            pixel_color = pyautogui.screenshot().getpixel((x, y))
            color = QColor(pixel_color[0], pixel_color[1], pixel_color[2])
            self.update_color_display(color)

    def paintEvent(self, event):
        if self.picking_color and self.mouse_pos is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            # Draw crosshair lines
            painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
            painter.drawLine(self.mouse_pos.x(), 0, self.mouse_pos.x(), self.height())
            painter.drawLine(0, self.mouse_pos.y(), self.width(), self.mouse_pos.y())

    def update_color_display(self, color):
        self.color_label.setStyleSheet(f"background-color: {color.name()};")
        self.rgb_label.setText(f"RGB: ({color.red()}, {color.green()}, {color.blue()})")
        self.hex_label.setText(f"HEX: {color.name().upper()}")

    def show(self):
        super().show()
        self.activateWindow()
        self.raise_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ColorPickerApp()
    window.show()
    sys.exit(app.exec_())
