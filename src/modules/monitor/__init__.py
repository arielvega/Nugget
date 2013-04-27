#coding:utf-8

#
#
# Copyright 2011,2013 Uremix (http://www.uremix.org) and contributors.
#
#
# This file is part of Nugget (The 3G dialer).
#
#    Nugget is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Nugget is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Nugget.  If not, see <http://www.gnu.org/licenses/>.
#
#


'''
Created on 02/10/2011

@author: Uremix Team (http://uremix.org)

'''

import pygtk
pygtk.require20()
import gtk

from uadh.gui import gtk2gui, base

from uadh.plugins import Plugin
import mobile

class Main(Plugin):
    def __init__(self, data):
        Plugin.__init__(self, data)
        self._view = data.view

    def run(self):
        #s = base.Section('Monitor',MonitorGui(self._view))
        #self._view.add_section(s)
        pass

    def get_id(self):
        return 'monitor-plugin'

class MonitorGui(gtk.Table):
    def __init__(self, view):
        gtk.Table.__init__(self, rows = 5, columns = 1)
        self._mainView = view
        self.attach(NetHistoryGui(),0,1,0,1, xpadding = 10, ypadding = 10, xoptions = gtk.EXPAND | gtk.FILL, yoptions=False)

class NetHistoryGui(gtk.Frame):
    def __init__(self):
        gtk.Frame.__init__(self)
        lbl = gtk.Label()
        lbl.set_markup('<b>Histórico de la red</b>')
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_label_widget(lbl)
        table = gtk.Table(rows = 3, columns = 3)
        self.add(table)