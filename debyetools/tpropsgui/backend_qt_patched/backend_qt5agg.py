"""
Render to qt from agg
"""
import matplotlib
from matplotlib import backends

backends._QT_FORCE_QT5_BINDING = True
from debyetools.tpropsgui.backend_qt_patched.backend_qtagg import (    # noqa: F401, E402 # pylint: disable=W0611
    _BackendQTAgg, FigureCanvasQTAgg, FigureManagerQT, NavigationToolbar2QT,
    backend_version,  FigureCanvasAgg,  FigureCanvasQT
)


@_BackendQTAgg.export
class _BackendQT5Agg(_BackendQTAgg):
    pass
