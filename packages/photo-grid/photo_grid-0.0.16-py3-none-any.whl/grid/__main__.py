import sys, qdarkstyle
from PyQt5.QtWidgets import QApplication
from .GRID import GRID

app = QApplication(sys.argv)
if '--light' not in sys.argv:
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
GRID()
app.exec_()
