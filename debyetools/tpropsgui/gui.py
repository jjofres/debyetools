import sys
from PySide6.QtWidgets import QApplication

from debyetools.tpropsgui.start_window import StartWindow


def dtgui():
    """
    Function that calls the mainWindow class from  debyetools.tpropsgui.startwindow.
    """
    app = QApplication(sys.argv)
    widget = StartWindow()
    widget.app = app
    widget.show()
    sys.exit(app.exec())




