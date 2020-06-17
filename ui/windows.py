from qtpy import QtWidgets, QtGui, QtCore
from qtpy.QtCore import Qt
from ui import views

def center(window):
    """
    Centres the window on the active screen
    """
    # https://stackoverflow.com/a/55172738/5013267
    frame_gm = window.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    frame_gm.moveCenter(QtWidgets.QApplication.desktop().screenGeometry(screen).center())
    window.move(frame_gm.topLeft())

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QtWidgets.QWidget(self)
        self.setWindowTitle("PZCurate")
        self.setCentralWidget(self.central_widget)

        # child dialog (if any)
        # -- kept as a class variable so that dialog doesn't get GC'd
        self.__dialog = None

        # containing widgets
        self._init_menu_bar()

        self.resize(1200, 700)
        center(self)

    def _init_menu_bar(self):
        menu_bar = self.menuBar()

        help_menu = menu_bar.addMenu("&Help")
        about_action = QtWidgets.QAction("&About", self)
        about_action.triggered.connect(self._menu_action_about)
        help_menu.addAction(about_action)

    def _menu_action_about(self):
        self.show_dialog(OkDialogWindow(self, "By PixelZerg", "About"))

    def show_dialog(self, dialog: "DialogWindow"):
        self.__dialog = dialog
        self.__dialog.close_signal.connect(self.__cleanup_dialog)
        self.__dialog.show()

    def __cleanup_dialog(self):
        # free up dialog memory
        del self.__dialog

class DialogWindow(QtWidgets.QMainWindow):
    close_signal = QtCore.Signal() # https://stackoverflow.com/a/37640029/5013267

    def __init__(self, parent, message=None, title=None):
        super().__init__(parent)

        central_widget = QtWidgets.QWidget(self)

        layout = QtWidgets.QVBoxLayout()

        if message is not None:
            label = QtWidgets.QLabel()
            label.setText(message)
            layout.addWidget(label)

        if title is not None:
            self.setWindowTitle(title)

        self.top_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(self.top_layout)

        # horizontal line
        line = QtWidgets.QFrame(self)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(line)

        self.bottom_layout = QtWidgets.QHBoxLayout()

        # horizontal spacer for the buttons
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.bottom_layout.addItem(spacer)

        layout.addLayout(self.bottom_layout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # window setup
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setWindowModality(Qt.ApplicationModal)

    def resize_wide(self):
        size_hint = self.sizeHint()
        self.setFixedSize(int(size_hint.width() * 1.5), size_hint.height())

    def add_button(self, button_text):
        button = QtWidgets.QPushButton()
        button.setText(button_text)
        self.bottom_layout.addWidget(button)
        return button

    def closeEvent(self, event):
        self.close_signal.emit()

class OkDialogWindow(DialogWindow):
    def __init__(self, parent, message=None, title=None):
        super().__init__(parent, message=message, title=title)

        self.btn_ok = self.add_button("Ok")
        self.btn_ok.clicked.connect(self._btn_ok_clicked)

    def _btn_ok_clicked(self):
        self.close()