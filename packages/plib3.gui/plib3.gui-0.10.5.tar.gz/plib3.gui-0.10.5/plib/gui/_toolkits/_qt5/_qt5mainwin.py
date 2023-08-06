#!/usr/bin/env python3
"""
Module QT5MAINWIN -- Python Qt 5 Main Window Objects
Sub-Package GUI.TOOLKITS.QT5 of Package PLIB3 -- Python GUI Toolkits
Copyright (C) 2008-2019 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the Qt 4 GUI main window objects.
"""

from plib.gui.defs import *
from plib.gui._base import mainwin

from ._qt5common import _PQtWidgetMeta
from ._qt5app import _PQtMainMixin
from ._qt5action import PQtMenu, PQtToolBar, PQtAction
from ._qt5statusbar import PQtStatusBar


class PQtMainWindow(_PQtMainMixin, mainwin.PMainWindowBase, metaclass=_PQtWidgetMeta):
    """Customized Qt main window class.
    """
    
    menuclass = PQtMenu
    toolbarclass = PQtToolBar
    statusbarclass = PQtStatusBar
    actionclass = PQtAction
    
    def __init__(self, parent, cls=None):
        _PQtMainMixin.__init__(self)
        mainwin.PMainWindowBase.__init__(self, parent, cls)
        self.abouttoolkitfunc = self.app.aboutQt
        self.setCentralWidget(self.clientwidget)
    
    def show_init(self):
        mainwin.PMainWindowBase.show_init(self)
        _PQtMainMixin.show_init(self)
