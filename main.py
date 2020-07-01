import sys
from qtpy import QtWidgets, QtGui, QtCore
from ui import windows
from importers import FolderWatcher
from threading import Thread

app = QtWidgets.QApplication(sys.argv)
main_window = windows.MainWindow()

folder_watcher = FolderWatcher()

if __name__ == '__main__':
    watcher_thread = Thread(target=folder_watcher.run)
    try:
        # run watcher on new thread
        watcher_thread.start()

        # run UI on current thread
        main_window.show()
        app.exec()
    finally:
        folder_watcher.stop()
        watcher_thread.join()
