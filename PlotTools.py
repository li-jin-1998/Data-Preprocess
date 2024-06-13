import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        plt.tight_layout()

    def plot_line(self, data):
        self.ax.clear()
        self.ax.plot(data['x'], data['y'], marker='o', linestyle='-', color='b')
        self.ax.set_title('Line Plot')
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.draw()

    def plot_scatter(self, data):
        self.ax.clear()
        self.ax.scatter(data['x'], data['y'], color='r')
        self.ax.set_title('Scatter Plot')
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.draw()

    def plot_histogram(self, data):
        self.ax.clear()
        self.ax.hist(data['x'], bins=10, alpha=0.75, color='g')
        self.ax.set_title('Histogram')
        self.ax.set_xlabel('Value')
        self.ax.set_ylabel('Frequency')
        self.draw()

    def plot_bar(self, data):
        self.ax.clear()
        self.ax.bar(data['x'], data['y'], color='y')
        self.ax.set_title('Bar Plot')
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Scientific Plotting Tool')
        self.setGeometry(100, 100, 800, 600)

        self.canvas = PlotCanvas(self)
        self.setCentralWidget(self.canvas)

        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QAction('Open File', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        plot_menu = menubar.addMenu('Plot')

        line_plot_action = QAction('Line Plot', self)
        line_plot_action.triggered.connect(self.plot_line)
        plot_menu.addAction(line_plot_action)

        scatter_plot_action = QAction('Scatter Plot', self)
        scatter_plot_action.triggered.connect(self.plot_scatter)
        plot_menu.addAction(scatter_plot_action)

        histogram_action = QAction('Histogram', self)
        histogram_action.triggered.connect(self.plot_histogram)
        plot_menu.addAction(histogram_action)

        bar_plot_action = QAction('Bar Plot', self)
        bar_plot_action.triggered.connect(self.plot_bar)
        plot_menu.addAction(bar_plot_action)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Data File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            try:
                data = pd.read_csv(file_name)
                self.data = data
                QMessageBox.information(self, "Success", "File opened successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to open file: {e}")

    def plot_line(self):
        if hasattr(self, 'data'):
            self.canvas.plot_line(self.data)
        else:
            QMessageBox.warning(self, "Error", "No data available. Please open a CSV file first.")

    def plot_scatter(self):
        if hasattr(self, 'data'):
            self.canvas.plot_scatter(self.data)
        else:
            QMessageBox.warning(self, "Error", "No data available. Please open a CSV file first.")

    def plot_histogram(self):
        if hasattr(self, 'data'):
            self.canvas.plot_histogram(self.data)
        else:
            QMessageBox.warning(self, "Error", "No data available. Please open a CSV file first.")

    def plot_bar(self):
        if hasattr(self, 'data'):
            self.canvas.plot_bar(self.data)
        else:
            QMessageBox.warning(self, "Error", "No data available. Please open a CSV file first.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
