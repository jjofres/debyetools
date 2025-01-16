# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from debyetools.tpropsgui.dialog_periodictable import dialogPeriodicTable
from debyetools.tpropsgui.dialog_crystal import dialogCrystal
# from main_window import dialogMainWindow
from debyetools.tpropsgui.main_window_small import dialogMainWindow

from debyetools.tpropsgui.atomtools import Molecule
from PySide6.QtCore import Qt, QTimer
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from debyetools.tpropsgui.ui_start_window import Ui_StartWindow
from PySide6.QtGui import QPixmap, QPalette

def highlight_line_edit(line_edit, color="purple", duration=100):
    # Set the background color
    line_edit.setStyleSheet(f"background-color: {color};")

    # Create a QTimer to reset the color after `duration` milliseconds
    timer = QTimer(line_edit)
    timer.setSingleShot(True)  # Only trigger once
    timer.timeout.connect(lambda: line_edit.setStyleSheet(""))  # Reset the color
    timer.start(duration)


class StartWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_StartWindow()
        self.ui.setupUi(self)

        self.dialogperiodictable = dialogPeriodicTable(self)
        self.ui.lineEdit_compoundname.clicked.connect(self.showDialogPeriodicTable)
        self.dialogperiodictable.external_lineEdit = self.ui.lineEdit_compoundname
        self.dialogperiodictable.external_lineEdit2 = self.ui.lineEdit_mass

        self.ui.pushButtonNext.clicked.connect(self.showDialogNext)

        self.dialogmainwindow = dialogMainWindow(self)
        self.dialogcrystal = dialogCrystal(self)

        self.molecule = Molecule()
        self.removed_items = {}

        # Connect the textChanged signals to a shared color change method
        self.ui.lineEdit_compoundname.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_compoundname))
        self.ui.lineEdit_mass.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_mass))
        self.ui.lineEdit_2.textChanged.connect(lambda: self.on_text_changed(self.ui.lineEdit_2))



    def showDialogPeriodicTable(self):
        self.dialogperiodictable.ui.lineEdit.setText(self.ui.lineEdit_compoundname.text())
        self.dialogperiodictable.show()  # Assuming dialogxx is initialized and ready to be displayed

    def showDialogNext(self):
        self.dialogmainwindow.app=self.app
        if self.ui.checkBox.isChecked():

            self.dialogcrystal.molecule = self.molecule
            self.dialogcrystal.eos_str = 'MP'

            self.dialogcrystal.dialogmainwindow = self.dialogmainwindow

            self.dialogcrystal.copied_mass = self.ui.lineEdit_mass.text()
            self.dialogcrystal.copied_name = self.ui.lineEdit_compoundname.text()

            self.show_hidden_comboboxitems()
            self.removed_items = {i:self.dialogmainwindow.ui.comboBox.itemText(i) for i in range(6)}
            print('removed_items', self.removed_items)
            for i in range(self.dialogmainwindow.ui.comboBox.count()-1, -1, -1):
                print(self.dialogmainwindow.ui.comboBox.itemText(i))
                if self.dialogmainwindow.ui.comboBox.itemText(i) in self.removed_items.values():
                    print(i, self.dialogmainwindow.ui.comboBox.itemText(i))

                    self.dialogmainwindow.ui.comboBox.removeItem(i)


            self.dialogcrystal.show()
        else:
            self.dialogmainwindow.ui.lineEdit.setText(self.ui.lineEdit_mass.text())
            self.dialogmainwindow.ui.lineEdit_11.setText(self.ui.lineEdit_compoundname.text())

            self.show_hidden_comboboxitems()
            self.removed_items = { 6: self.dialogmainwindow.ui.comboBox.itemText(6)}
            self.dialogmainwindow.ui.comboBox.removeItem(6)
            self.dialogmainwindow.show()


    def show_hidden_comboboxitems(self):
            for ix,value in self.removed_items.items():

                self.dialogmainwindow.ui.comboBox.insertItem(ix,value)

    def is_dark_mode(self):
        # Detect if the application is in dark mode using the palette
        palette = self.palette()
        return palette.color(QPalette.ColorRole.Window).value() < 128  # Lightness threshold for dark mode

    def on_text_changed(self, line_edit):
        # Call the reusable highlight function
        dark_mode = self.is_dark_mode()
        color_p = "purple" if dark_mode else "#94a2c9"

        highlight_line_edit(line_edit, color=color_p, duration=500)
        # Update label with the current content of the edited line edit





