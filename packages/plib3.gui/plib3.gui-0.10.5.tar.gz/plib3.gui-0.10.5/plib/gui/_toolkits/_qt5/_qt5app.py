#!/usr/bin/env python3
"""
Module QT5APP -- Python Qt 5 Application Objects
Sub-Package GUI.TOOLKITS.QT5 of Package PLIB3 -- Python GUI Toolkits
Copyright (C) 2008-2019 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the Qt 4 GUI application objects.
"""

from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qt

from plib.gui.defs import *
from plib.gui._base import app

from ._qt5common import _PQtCommunicator, _PQtWidgetMeta, _qtmessagefuncs


def _int(button):
    if button is not None:
        return button
    else:
        return 0


class PQtMessageBox(app.PMessageBoxBase):
    """Customized Qt message box.
    """
    
    questionmap = {
        answerYes: qt.QMessageBox.Yes,
        answerNo: qt.QMessageBox.No,
        answerCancel: qt.QMessageBox.Cancel,
        answerOK: qt.QMessageBox.Ok
    }
    
    def _messagebox(self, type, caption, text,
                    button1, button2=None, button3=None):
        
        buttons = default = button1
        if button2 is not None:
            buttons |= button2
            if button3 is not None:
                buttons |= button3
                default = button3
            else:
                default = button2
        
        return _qtmessagefuncs[type](self._parent, caption, text,
                                     buttons, default)


class PQtFileDialog(app.PFileDialogBase):
    
    def openfiledialog(self, path, filter):
        return qt.QFileDialog.getOpenFileName(None, "Open",
                                              path, filter)[0]
    
    def savefiledialog(self, path, filter):
        return qt.QFileDialog.getSaveFileName(None, "Save",
                                              path, filter)[0]


class PQtAboutDialog(app.PAboutDialogBase):
    
    attrnames = [
        'name',
        'version',
        'copyright',
        'license',
        'description',
        'developers',
        'website',
        'icon'
    ]
    
    formatstr = "{aname} {aversion}\n{adescription}\n{acopyright}\n{adevelopers}\n{awebsite}"
    
    def __getattribute__(self, name):
        # Here we have to modify the hack somewhat
        attrnames = object.__getattribute__(self, 'attrnames')
        if name in attrnames:
            object.__getattribute__(self, '__dict__')['temp'] = name
            name = 'store'
        return object.__getattribute__(self, name)
    
    def store(self, data):
        name = self.temp
        del self.temp
        if name == 'developers':
            data = ", ".join(data)
        setattr(self, "a{}".format(name), data)
    
    def display(self):
        caption = "About {}".format(self.aname)
        # Leave out icon here (setting it in set_iconfile below is enough, and
        # including it here will raise an exception if there is no icon)
        body = self.formatstr.format(**dict(
            ("a{}".format(name), getattr(self, "a{}".format(name)))
            for name in self.attrnames if name != 'icon'))
        qt.QMessageBox.about(self.mainwidget, caption, body)


# NOTE: For some reason, PyQt5 insists on having the Qt classes first in the MRO,
# so all MROs have been switched around to do that. PySide2 does not require this.
# Note sure why the difference between the two, possibly different wrapper generation
# tools.

class _PQtBaseMixin(qt.QMainWindow, _PQtCommunicator):
    """Mixin class for Qt base windows.
    """
    
    event_signals = (SIGNAL_CLOSING, SIGNAL_SHOWN, SIGNAL_HIDDEN)
    
    def _get_w(self):
        return self.width()
    w = property(_get_w)
    
    def _show_window(self):
        qt.QMainWindow.show(self)
    
    def _hide_window(self):
        qt.QMainWindow.hide(self)
    
    def set_caption(self, caption):
        self.setWindowTitle(caption)
    
    def _get_desktop_rect(self, primary=True):
        # Correctly handle virtual desktop across multiple screens
        desktop = self.app.desktop()
        l = desktop.x()
        t = desktop.y()
        w = desktop.width()
        h = desktop.height()
        if desktop.isVirtualDesktop() and primary:
            # Default to centering on the primary screen
            i = desktop.primaryScreen()
            n = desktop.numScreens()
            w = w / n
            # NOTE: We have to check for i > 0 here because in some
            # cases (e.g., when running in a VirtualBox), Qt thinks
            # the desktop is "virtual" but there's only one screen and
            # desktop.primaryScreen returns 0 instead of 1.
            if i > 0:
                l += w * (i - 1)
        else:
            i = 0
            n = 1
        return i, n, l, t, w, h
    
    def sizetoscreen(self, maximized):
        if maximized:
            if self.shown:
                self.showMaximized()
            else:
                self._showMax = True
        else:
            i, n, l, t, w, h = self._get_desktop_rect()
            self.resize(
                w - self.sizeoffset,
                h - self.sizeoffset)
            self.move(l, t)
    
    def sizetoclient(self, clientwidth, clientheight):
        self.resize(clientwidth, clientheight)
    
    def center(self):
        i, n, l, t, w, h = self._get_desktop_rect()
        s = self.frameSize()  # FIXME: this appears to give wrong values!
        x, y = s.width(), s.height()
        self.move(l + (w - x) / 2, t + (h - y) / 2)
    
    def show_init(self):
        if hasattr(self, '_showMax'):
            self.showMaximized()
            del self._showMax
        else:
            qt.QMainWindow.show(self)
    
    def do_exit(self):
        self.close()
    
    def closeEvent(self, event):
        # 'automagic' code for SIGNAL_QUERYCLOSE
        if self._canclose():
            self._emit_event(SIGNAL_CLOSING)
            event.accept()
        else:
            event.ignore()
    
    def showEvent(self, event):
        self._emit_event(SIGNAL_SHOWN)
    
    def hideEvent(self, event):
        self._emit_event(SIGNAL_HIDDEN)


class PQtBaseWindow(_PQtBaseMixin, app.PBaseWindowBase, metaclass=_PQtWidgetMeta):
    """Customized Qt base window class.
    """
    
    def __init__(self, parent, cls=None):
        p = parent if isinstance(parent, qt.QWidget) else None
        _PQtBaseMixin.__init__(self, p)
        app.PBaseWindowBase.__init__(self, parent, cls)
        self.setCentralWidget(self.clientwidget)
    
    def show_init(self):
        app.PBaseWindowBase.show_init(self)
        _PQtBaseMixin.show_init(self)


class _PQtMainMixin(_PQtBaseMixin):
    """Mixin class for Qt top windows and main windows.
    """
    
    messageboxclass = PQtMessageBox
    filedialogclass = PQtFileDialog
    aboutdialogclass = PQtAboutDialog
    
    def set_iconfile(self, iconfile):
        self.setWindowIcon(qtg.QIcon(qtg.QPixmap(iconfile)))
    
    def _size_to_settings(self, width, height):
        self.resize(width, height)
    
    def _move_to_settings(self, left, top):
        self.move(left, top)
    
    def _get_current_geometry(self):
        p = self.pos()
        s = self.size()
        return p.x(), p.y(), s.width(), s.height()
    
    def choose_directory(self, curdir):
        return str(qt.QFileDialog.getExistingDirectory(
            self, "Select Folder", qt.QString(curdir)))


class PQtTopWindow(_PQtMainMixin, app.PTopWindowBase, metaclass=_PQtWidgetMeta):
    """Customized Qt top window class.
    """
    
    def __init__(self, parent, cls=None):
        p = parent if isinstance(parent, qt.QWidget) else None
        _PQtMainMixin.__init__(self, p)
        app.PTopWindowBase.__init__(self, parent, cls)
        self.abouttoolkitfunc = self.app.aboutQt
        self.setCentralWidget(self.clientwidget)
    
    def show_init(self):
        app.PTopWindowBase.show_init(self)
        _PQtMainMixin.show_init(self)


class PQtApplication(qt.QApplication, _PQtCommunicator, app.PApplicationBase):
    """Customized Qt application class.
    """
    
    _local_loop = None
    
    def __init__(self, arglist=[], cls=None, use_mainwindow=False):
        qt.QApplication.__init__(self, arglist)
        app.PApplicationBase.__init__(self, arglist, cls, use_mainwindow)
        self.mainwin = self.createMainWidget()
        #self.setMainWidget(self.mainwin)
        
        # 'automagic' signal connection
        self.setup_notify(SIGNAL_BEFOREQUIT, self.before_quit)
    
    def _eventloop(self):
        self.exec_()
    
    def process_events(self):
        self.processEvents()
    
    # For use when multiplexing with other event types (e.g.,
    # in a NotifierClient
    
    def enter_yield(self):
        if self._local_loop is None:
            self._local_loop = qtc.QEventLoop()
            self._local_loop.exec_()
    
    def exit_yield(self):
        if self._local_loop is not None:
            self._local_loop.exit()
            del self._local_loop
