#!/usr/bin/env python
"""
Module QTAPP -- Python Qt Application Objects
Sub-Package GUI.TOOLKITS.QT of Package PLIB -- Python GUI Toolkits
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the Qt GUI application objects.
"""

import qt

from plib.gui.defs import *
from plib.gui._base import app

from ._qtcommon import _PQtCommunicator, _qtmessagefuncs


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
        
        return _qtmessagefuncs[type](self._parent, caption, text,
                                     _int(button1), _int(button2), _int(button3))


class PQtFileDialog(app.PFileDialogBase):
    
    def openfiledialog(self, path, filter):
        return qt.QFileDialog.getOpenFileName(path, filter)
    
    def savefiledialog(self, path, filter):
        return qt.QFileDialog.getSaveFileName(path, filter)


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


class _PQtBaseMixin(_PQtCommunicator, qt.QMainWindow):
    """Mixin class for Qt base windows.
    """
    
    def _get_w(self):
        return self.width()
    w = property(_get_w)
    
    def _show_window(self):
        qt.QMainWindow.show(self)
    
    def _hide_window(self):
        qt.QMainWindow.hide(self)
    
    def set_caption(self, caption):
        self.setCaption(caption)
    
    def _get_desktop_rect(self, primary=True):
        # Correctly handle virtual desktop across multiple screens
        desktop = self.app.desktop()
        l = desktop.x()
        t = desktop.y()
        w = desktop.width()
        h = desktop.height()
        if desktop.isVirtualDesktop() and primary:
            # Return the rect of the primary screen only
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
        g = self.frameGeometry()
        x, y = g.width(), g.height()
        self.move(l + (w - x) / 2, t + (h - y) / 2)
    
    def show_init(self):
        if hasattr(self, '_showMax'):
            self.showMaximized()
            del self._showMax
        else:
            qt.QMainWindow.show(self)
    
    def exit(self):
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


class PQtBaseWindow(_PQtBaseMixin, app.PBaseWindowBase):
    """Customized Qt base window class.
    """
    
    def __init__(self, parent, cls=None):
        _PQtBaseMixin.__init__(self)
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
        self.setIcon(qt.QPixmap(iconfile))
    
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
            qt.QString(curdir), self, 'select_folder', "Select Folder"))


class PQtTopWindow(_PQtMainMixin, app.PTopWindowBase):
    """Customized Qt top window class.
    """
    
    def __init__(self, parent, cls=None):
        _PQtMainMixin.__init__(self)
        app.PTopWindowBase.__init__(self, parent, cls)
        self.abouttoolkitfunc = self.app.aboutQt
        self.setCentralWidget(self.clientwidget)
    
    def show_init(self):
        app.PTopWindowBase.show_init(self)
        _PQtMainMixin.show_init(self)


class PQtApplication(_PQtCommunicator, qt.QApplication, app.PApplicationBase):
    """Customized Qt application class.
    """
    
    _in_local_loop = False
    
    def __init__(self, arglist=[], cls=None, use_mainwindow=False):
        qt.QApplication.__init__(self, arglist)
        app.PApplicationBase.__init__(self, arglist, cls, use_mainwindow)
        self.mainwin = self.createMainWidget()
        self.setMainWidget(self.mainwin)
        
        # 'automagic' signal connection
        self.setup_notify(SIGNAL_BEFOREQUIT, self.before_quit)
    
    def _eventloop(self):
        self.exec_loop()
    
    def process_events(self):
        self.processEvents()
    
    # For use when multiplexing with other event types (e.g.,
    # in a NotifierClient
    
    # FIXME: This only seems to work for Qt 3 when enterLoop() and
    # exitLoop() are called directy from NotifierClient ???
    
    #def enter_yield(self):
    #    if not self._in_local_loop:
    #        self.eventLoop().enterLoop()
    #        self._in_local_loop = True
    
    #def exit_yield(self):
    #    if self._in_local_loop:
    #        self._in_local_loop = False
    #        self.eventLoop().exitLoop()
