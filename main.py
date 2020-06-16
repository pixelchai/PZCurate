import sys

from qtpy import QtWidgets, QtGui, QtCore
from ui import windows

app = QtWidgets.QApplication(sys.argv)
main_window = windows.MainWindow()
main_window.show()
app.exec()