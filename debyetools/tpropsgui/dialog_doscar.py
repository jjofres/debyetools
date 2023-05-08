from PySide6.QtWidgets import  QDialog, QFileDialog
from debyetools.tpropsgui.ui_dialog_doscar import Ui_Dialog as Ui_DOSCAR


class dialogDOSCAR(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DOSCAR()
        self.ui.setupUi(self)

        self.ui.browse.clicked.connect(self.getfiles)
        self.ui.ok.clicked.connect(self.on_pushButton_OK)
        self.filepath='.'

    def getfiles(self):
            filepath = QFileDialog.getExistingDirectory(self, caption='Select a folder')
            self.ui.filepath.setText(filepath)

    def on_pushButton_OK(self):
        self.filepath = self.ui.filepath.text()
        self.close()
