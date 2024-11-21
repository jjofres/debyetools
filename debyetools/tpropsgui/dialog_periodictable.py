from PySide6.QtWidgets import QDialog

from debyetools.tpropsgui.atomtools import atomic_mass
from debyetools.tpropsgui.ui_dialog_periodictable import Ui_Dialog as Ui_Dialog


def create_formula_from_dict(d):
    result = ""
    for key, value in d.items():
        if value > 0:
            if value == 1:
                result += key  # Add just the key if the value is 1
            else:
                result += f"{key}{value}"  # Add key and value if value is greater than 1
    return result

class dialogPeriodicTable(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.formula = ''
        self.mass = 0  # 0.02698
        self.dict_formula = {k:0 for k in [getattr(self.ui, 'pushB'+str(i)).text() for i in range(118)]}
        # self.dict_formula['Al']=0#4
        # Example setup with multiple counting buttons
        self.buttons = [getattr(self.ui, 'pushB'+str(i)) for i in range(118)]
        self.buttons[12].counter = 0  #4
        for btn in self.buttons:
            btn.counterChanged2.connect(self.updateFormula)
            # self.layout.addWidget(btn)
            btn.set_style()

        self.ui.pushButton_3.clicked.connect(self.on_pushButton_OK)





    def updateFormula(self, str, counter):
        self.dict_formula[str] = counter
        self.formula = create_formula_from_dict(self.dict_formula)

        # print('formula', self.formula)
        for btn in self.buttons:
            btn.set_style()
        self.ui.lineEdit.setText(self.formula)

        mass = 0
        total_count = 0
        for k,v in self.dict_formula.items():
            total_count += int(v)
            mass += atomic_mass[k]*int(v)

        self.mass = mass/total_count/1000


        # self.ui.browse.clicked.connect(self.getfiles)
        # self.ui.ok.clicked.connect(self.on_pushButton_OK)
        # self.filepath='.'

    # def getfiles(self):
    #         filepath = QFileDialog.getExistingDirectory(self, caption='Select a folder')
    #         self.ui.filepath.setText(filepath)

    def on_pushButton_OK(self):
        # self.filepath = self.ui.filepath.text()
        self.close()

    def closeEvent(self, event):
        # print('something')
        self.external_lineEdit.setText(self.formula)
        self.external_lineEdit2.setText(f'{self.mass}')
        event.accept()

