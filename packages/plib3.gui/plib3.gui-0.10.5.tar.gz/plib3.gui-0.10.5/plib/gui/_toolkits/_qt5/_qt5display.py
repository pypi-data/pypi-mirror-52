#!/usr/bin/env python3
"""
Module QT5DISPLAY -- Python Qt 5 Text Display Widgets
Sub-Package GUI.TOOLKITS.QT5 of Package PLIB3 -- Python GUI Toolkits
Copyright (C) 2008-2019 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the Qt 4 GUI objects for text display widgets.
"""

from PyQt5 import QtWidgets as qt

from plib.gui._widgets import display

from ._qt5common import _PQtWidgetMeta, _PQtWidget


class PQtTextDisplay(qt.QTextEdit, _PQtWidget, display.PTextDisplayBase, metaclass=_PQtWidgetMeta):
    
    widget_class = qt.QTextEdit
    
    def __init__(self, parent, text=None, geometry=None, scrolling=False):
        qt.QTextEdit.__init__(self, parent)
        self.setReadOnly(True)
        if scrolling:
            self.setLineWrapMode(qt.QTextEdit.NoWrap)
        display.PTextDisplayBase.__init__(self, text, geometry)
    
    def get_text(self):
        return str(self.toPlainText())
    
    def set_text(self, value):
        self.setPlainText(value)
    
    def set_width(self, width):
        self.resize(width, self.height())
        # Qt text edits don't seem to fully respect
        # qt.QSizePolicy.MinimumExpanding
        self.setMinimumWidth(width)
    
    def set_height(self, height):
        self.resize(self.width(), height)
        # Qt text edits don't seem to fully respect
        # qt.QSizePolicy.MinimumExpanding
        self.setMinimumHeight(height)
