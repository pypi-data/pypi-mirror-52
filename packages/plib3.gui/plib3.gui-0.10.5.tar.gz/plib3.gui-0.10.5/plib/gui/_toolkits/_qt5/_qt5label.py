#!/usr/bin/env python3
"""
Module QT5LABEL -- Python Qt 5 Text Label Widgets
Sub-Package GUI.TOOLKITS.QT5 of Package PLIB3 -- Python GUI Toolkits
Copyright (C) 2008-2019 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the Qt 4 GUI objects for text label widgets.
"""

from PyQt5 import QtWidgets as qt

from plib.gui._widgets import label

from ._qt5common import _PQtWidgetMeta, _PQtWidget


class PQtTextLabel(qt.QLabel, _PQtWidget, label.PTextLabelBase, metaclass=_PQtWidgetMeta):
    
    widget_class = qt.QLabel
    
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
