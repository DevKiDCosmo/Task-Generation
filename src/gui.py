from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Application")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon("icon.png"))

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Widgets
        self.label = QLabel("Hello, World!")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type something...")
        self.layout.addWidget(self.input_field)

        self.button = QPushButton("Click Me")
        self.button.clicked.connect(self.on_button_click)
        self.layout.addWidget(self.button)

t = MainWindow()
t.show()