#!/usr/bin/env python3
"""
Module PYSIDE2DISPLAY -- Python PySide2 Text Display Widgets
Sub-Package GUI.TOOLKITS.PYSIDE2 of Package PLIB3 -- Python GUI Toolkits
Copyright (C) 2008-2019 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the PySide GUI objects for text display widgets.
"""

from PySide2 import QtWidgets as qt

from plib.gui._widgets import display

from ._pyside2common import _PQtWidgetMeta, _PQtWidget


class PQtTextDisplay(_PQtWidget, qt.QTextEdit, display.PTextDisplayBase, metaclass=_PQtWidgetMeta):
    
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
