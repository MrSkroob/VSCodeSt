import sys

from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QMainWindow, QGridLayout, QLabel, QPushButton, QColorDialog
from PyQt6.QtCore import pyqtSignal


class ClickableLineEdit(QLineEdit):
    """Wrapper class which adds a mouse click signal to QLineEdit"""
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()
        QLineEdit.mousePressEvent(self, event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversion tool")

        widget = QWidget()
        layout = QGridLayout()

        widget.setLayout(layout)

        feet_label = QLabel("Feet")
        metre_label = QLabel("Metres")

        self.feet_lineedit = ClickableLineEdit()
        self.metre_lineedit = ClickableLineEdit()

        # self.set_theme_button = QPushButton("Select theme")-
        # self.set_theme_button.clicked.connect(self.open_colour_dialogue)

        layout.addWidget(feet_label, 0, 0)
        layout.addWidget(metre_label, 1, 0)
        layout.addWidget(self.feet_lineedit, 0, 1)
        layout.addWidget(self.metre_lineedit, 1, 1)
        layout.addWidget(self.set_theme_button, 2, 0)

        self.feet_lineedit.textEdited.connect(self._update_metre)
        self.feet_lineedit.clicked.connect(self.feet_lineedit.clear)
        
        self.metre_lineedit.textEdited.connect(self._update_feet)
        self.metre_lineedit.clicked.connect(self.metre_lineedit.clear)

        self.setCentralWidget(widget)

    
    def open_colour_dialogue(self):
        colour = QColorDialog().getColor()

        if colour.isValid():
            pass

    
    def _update_feet(self, new_value: str):
        try:
            result = float(new_value) * 3.281
            self.feet_lineedit.setText(str(result))
        except ValueError:
            self.feet_lineedit.setText("Error")

    def _update_metre(self, new_value: str):
        try:
            result = float(new_value) / 3.281
            self.metre_lineedit.setText(str(result))
        except ValueError:
            self.metre_lineedit.setText("Error")


app = QApplication(sys.argv)


window = MainWindow()
window.show()

app.exec()
