from PySide6.QtWidgets import QLineEdit, QPushButton
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QMouseEvent


class ClickableLineEdit(QLineEdit):
    # Define a custom signal named 'clicked'
    clicked = Signal()

    def __init__(self, parent=None):
        super(ClickableLineEdit, self).__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emit the clicked signal on mouse press
        super(ClickableLineEdit, self).mousePressEvent(event)

element_colors = {
    "H": "#00FF00", "He": "#EE82EE",
    "Li": "#FF6666", "Be": "#FFA500", "B": "#FFFF99", "C": "#00FF00", "N": "#00FF00", "O": "#00FF00", "F": "#FFFF00", "Ne": "#EE82EE",
    "Na": "#FF6666", "Mg": "#FFA500", "Al": "#FFDAB9", "Si": "#FFFF99", "P": "#00FF00", "S": "#00FF00", "Cl": "#FFFF00", "Ar": "#EE82EE",
    "K": "#FF6666", "Ca": "#FFA500", "Sc": "#ADD8E6", "Ti": "#ADD8E6", "V": "#ADD8E6", "Cr": "#ADD8E6", "Mn": "#ADD8E6", "Fe": "#ADD8E6",
    "Co": "#ADD8E6", "Ni": "#ADD8E6", "Cu": "#ADD8E6", "Zn": "#ADD8E6", "Ga": "#FFDAB9", "Ge": "#FFFF99", "As": "#FFFF99", "Se": "#00FF00",
    "Br": "#FFFF00", "Kr": "#EE82EE", "Rb": "#FF6666", "Sr": "#FFA500", "Y": "#ADD8E6", "Zr": "#ADD8E6", "Nb": "#ADD8E6", "Mo": "#ADD8E6",
    "Tc": "#ADD8E6", "Ru": "#ADD8E6", "Rh": "#ADD8E6", "Pd": "#ADD8E6", "Ag": "#ADD8E6", "Cd": "#ADD8E6", "In": "#FFDAB9", "Sn": "#FFDAB9",
    "Sb": "#FFFF99", "Te": "#FFFF99", "I": "#FFFF00", "Xe": "#EE82EE", "Cs": "#FF6666", "Ba": "#FFA500", "La": "#FFB6C1", "Ce": "#FFB6C1",
    "Pr": "#FFB6C1", "Nd": "#FFB6C1", "Pm": "#FFB6C1", "Sm": "#FFB6C1", "Eu": "#FFB6C1", "Gd": "#FFB6C1", "Tb": "#FFB6C1", "Dy": "#FFB6C1",
    "Ho": "#FFB6C1", "Er": "#FFB6C1", "Tm": "#FFB6C1", "Yb": "#FFB6C1", "Lu": "#FFB6C1", "Hf": "#ADD8E6", "Ta": "#ADD8E6", "W": "#ADD8E6",
    "Re": "#ADD8E6", "Os": "#ADD8E6", "Ir": "#ADD8E6", "Pt": "#ADD8E6", "Au": "#ADD8E6", "Hg": "#ADD8E6", "Tl": "#FFDAB9", "Pb": "#FFDAB9",
    "Bi": "#FFDAB9", "Po": "#FFDAB9", "At": "#FFFF00", "Rn": "#EE82EE", "Fr": "#FF6666", "Ra": "#FFA500", "Ac": "#D8BFD8", "Th": "#D8BFD8",
    "Pa": "#D8BFD8", "U": "#D8BFD8", "Np": "#D8BFD8", "Pu": "#D8BFD8", "Am": "#D8BFD8", "Cm": "#D8BFD8", "Bk": "#D8BFD8", "Cf": "#D8BFD8",
    "Es": "#D8BFD8", "Fm": "#D8BFD8", "Md": "#D8BFD8", "No": "#D8BFD8", "Lr": "#D8BFD8", "Rf": "#ADD8E6", "Db": "#ADD8E6", "Sg": "#ADD8E6",
    "Bh": "#ADD8E6", "Hs": "#ADD8E6", "Mt": "#ADD8E6", "Ds": "#ADD8E6", "Rg": "#ADD8E6", "Cn": "#ADD8E6", "Nh": "#FFDAB9", "Fl": "#FFDAB9",
    "Mc": "#FFDAB9", "Lv": "#FFDAB9", "Ts": "#FFFF00", "Og": "#EE82EE"
}

class CountingButton(QPushButton):
    counterChanged = Signal(int)  # Signal that indicates the counter has changed
    counterChanged2 = Signal(str, int)

    def __init__(self, label, parent=None):
        super(CountingButton, self).__init__(label, parent)
        self.counter = 0

    def set_style(self):
        bc = 'None' if self.counter==0 else 'purple'
        bw = 1 if self.counter==0 else 2
        # print(bc)
        self.setStyleSheet(
                'QPushButton {' + \
                f'background-color: {element_colors[self.text()]};' + \
                    'border-style: outset;' + \
                    f'border-width: {bw}px;' + \
                    'border-radius: 5px;' + \
                    'color: gray;' + \
                    # 'border-color: beige;' + \
                    'padding: 0px;' + \
                    f'border-color: {bc};' + \
                '}' + \
                'QPushButton:pressed {' + \
                    'background-color: navy;' + \
                    'border-style: inset;' + \
                    'border-color: purple;' + \
                '}' + \
                ''
            )

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.incrementCounter()
        elif event.button() == Qt.RightButton:
            self.decrementCounter()
        super(CountingButton, self).mousePressEvent(event)

    def incrementCounter(self):
        self.counter += 1
        self.counter = max(self.counter, 0)
        self.counterChanged2.emit(self.text(), self.counter) #WIP Emit Text+counter
        # self.updateText()

    def decrementCounter(self):
        self.counter -= 1
        self.counter = max(self.counter, 0)
        self.counterChanged2.emit(self.text(), self.counter)
        # self.updateText()

    # def updateText(self):
    #     self.setText(f"Count: {self.counter}")
