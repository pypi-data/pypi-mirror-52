#!/usr/bin/env python3
"""
Module PYSIDE2LABEL -- Python PySide2 Text Label Widgets
Sub-Package GUI.TOOLKITS.PYSIDE2 of Package PLIB3 -- Python GUI Toolkits
Copyright (C) 2008-2019 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the PySide GUI objects for text label widgets.
"""

from PySide2 import QtWidgets as qt

from plib.gui._widgets import label

from ._pyside2common import _PQtWidgetMeta, _PQtWidget


class PQtTextLabel(_PQtWidget, qt.QLabel, label.PTextLabelBase, metaclass=_PQtWidgetMeta):
    
    def __init__(self, parent, text=None, geometry=None):
        qt.QLabel.__init__(self, parent)
        label.PTextLabelBase.__init__(self, text, geometry)
    
    def get_text(self):
        return str(self.text())
    
    def set_text(self, value):
        self.setText(value)
    
    def set_width(self, width):
        self.resize(width, self.height())
        # Qt text labels don't seem to fully respect
        # qt.QSizePolicy.MinimumExpanding
        self.setMinimumWidth(width)
