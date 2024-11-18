from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import Cursor
from matplotlib.figure import Figure
import numpy as np


# Main window
class windowPlot(QMainWindow):
    def __init__(self, parent=None):
        # Initialize QMainWindow
        super().__init__()
        # Get MplWidget
        self.mpl_widget = MplWidget()
        # Set MplWidget as central widget
        self.setCentralWidget(self.mpl_widget)
        # Create axes
        self.ax = self.mpl_widget.canvas.figure.add_subplot(111)
        # Reference Cursor
        self.cursor = Cursor(self.ax, useblit=True, linewidth=0.8, color='lightgray')
        # Plot some random stuff
#        x, y = np.random.rand(100), np.random.rand(100)
#        self.ax.scatter(x, y)
#        # Show app
#        self.show()


# MplCanvas
class MplWidget(QWidget):
    def __init__(self, parent=None):
        # Initialize QWidget
        super().__init__(parent)
        # Create canvas
        self.canvas = FigureCanvas(Figure())
        # Set constrained layout
        self.canvas.figure.set_constrained_layout(True)
        # Create layout
        layout = QVBoxLayout()
        # Add canvas
        layout.addWidget(self.canvas)
        # Set layout
        self.setLayout(layout)


## Initialize app
#app = QApplication([])
#UI = MainWindow()
#app.exec()
