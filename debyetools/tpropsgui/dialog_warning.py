from PySide6.QtWidgets import QDialog
from debyetools.tpropsgui.ui_warning import Ui_Dialog as Ui_Warning

class dialogWarning(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Warning()
        self.ui.setupUi(self)
