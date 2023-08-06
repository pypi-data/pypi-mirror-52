#!/usr/bin/env python3
"""
Module QT5STATUSBAR -- Python Qt 5 Status Bar Objects
Sub-Package GUI.TOOLKITS.QT5 of Package PLIB3 -- Python GUI Toolkits
Copyright (C) 2008-2019 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the Qt 4 GUI objects for the status bar.
"""

from PyQt5 import QtWidgets as qt

from plib.gui._base import statusbar

from ._qt5common import _PQtWidgetBase
from ._qt5label import PQtTextLabel


class PQtStatusBar(qt.QStatusBar, _PQtWidgetBase, statusbar.PStatusBarBase):
    
    textareaclass = PQtTextLabel
    
    def __init__(self, parent, widgets=None):
        qt.QStatusBar.__init__(self, parent)
        statusbar.PStatusBarBase.__init__(self, parent, widgets)
        parent.setStatusBar(self)
    
    def _add_widget(self, widget, expand=False, custom=True):
        if custom:
            self.addPermanentWidget(widget, int(expand))
        else:
            self.addWidget(widget, int(expand))
