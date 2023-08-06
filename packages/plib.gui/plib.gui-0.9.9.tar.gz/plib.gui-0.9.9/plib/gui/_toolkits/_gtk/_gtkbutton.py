#!/usr/bin/env python
"""
Module GTKBUTTON -- Python GTK Button Widgets
Sub-Package GUI.TOOLKITS.GTK of Package PLIB -- Python GUI Toolkits
Copyright (C) 2008-2015 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains the GTK GUI objects for button widgets.
"""

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from plib.gui.defs import *
from plib.gui._widgets import button

from ._gtkcommon import _PGtkWidget, _gtkstockids, _gtksignals


class _PGtkButtonMixin(object):
    
    def set_caption(self, caption):
        label = caption.replace("&", "_")
        self.set_label(label)
    
    def set_icon(self, pxname):
        # No way currently to set custom icons in Gtk without major gymnastics
        pass


class PGtkButton(_PGtkButtonMixin, _PGtkWidget, gtk.Button,
                 button.PButtonBase):
    
    #_adjust = True
    
    def __init__(self, parent, caption=None, pxname=None,
                 target=None, geometry=None):
        
        stockid = None
        # We can't wait until PButtonBase.__init__ to do this in Gtk
        if isinstance(caption, int):
            if caption in _gtkstockids:
                stockid = _gtkstockids[caption]
                caption = None
        gtk.Button.__init__(self, None, stockid)
        if caption is not None:
            self.set_use_underline(True)
        _PGtkWidget.__init__(self, parent)
        button.PButtonBase.__init__(self, caption, pxname, target, geometry)
    
    def _font_widget(self):
        if self.get_use_stock():
            return self.child.get_children()[1]  # FIXME: is this right?
        elif isinstance(self.child, gtk.Label):
            return self.child
        raise ValueError("Gtk Button does not have a label.")


class PGtkCheckBox(_PGtkButtonMixin, _PGtkWidget, gtk.CheckButton,
                   button.PCheckBoxBase):
    
    fn_get_checked = 'get_active'
    fn_set_checked = 'set_active'
    
    __gsignals__ = {
        _gtksignals[SIGNAL_TOGGLED]: (
            gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_BOOLEAN,))
    }
    
    def __init__(self, parent, caption=None, pxname=None, tristate=False,
                 target=None, geometry=None):
        
        gtk.CheckButton.__init__(self)
        _PGtkWidget.__init__(self, parent)
        button.PCheckBoxBase.__init__(self, caption, pxname, tristate,
                                      target, geometry)
        
        # Pass our current checked state in the visible SIGNAL_TOGGLED signal
        self.connect(_gtksignals[SIGNAL_CHECKTOGGLED], self._check_toggled)
    
    def _check_toggled(self, obj):
        self.do_notify(SIGNAL_TOGGLED, self.checked)
    
    def make_tristate(self):
        # FIXME: No such thing in GTK?
        pass
