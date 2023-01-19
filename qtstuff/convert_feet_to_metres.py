import sys

from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QMainWindow, QGridLayout, QLabel
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

        feet_lineedit = ClickableLineEdit()
        metre_lineedit = ClickableLineEdit()

        layout.addWidget(feet_label, 0, 0)
        layout.addWidget(metre_label, 1, 0)
        layout.addWidget(feet_lineedit, 0, 1)
        layout.addWidget(metre_lineedit, 1, 1)

        def feet_changed(new_text: str):
            try:
                result = float(new_text) / 3.281
                metre_lineedit.setText(str(result))
            except ValueError:
                metre_lineedit.setText("Error")
            
        def metres_changed(new_text: str):
            try:
                result = float(new_text) * 3.281
                feet_lineedit.setText(str(result))
            except ValueError:
                feet_lineedit.setText("Error")

        feet_lineedit.textEdited.connect(feet_changed)
        feet_lineedit.clicked.connect(feet_lineedit.clear)
        
        metre_lineedit.textEdited.connect(metres_changed)
        metre_lineedit.clicked.connect(metre_lineedit.clear)


        self.setCentralWidget(widget)



app = QApplication(sys.argv)


window = MainWindow()
window.show()

app.exec()