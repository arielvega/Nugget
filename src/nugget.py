#!/usr/bin/python

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
import time
pygtk.require20()
import gtk

import uadh
from uadh import plugins
from uadh.gui import gtk2gui
from devicescontroller import DeviceController
import mobile

class Nugget(uadh.UObject):
    def __init__(self, datapath = './', pluginspath = './'):
        uadh.UObject.__init__(self)
        self._added = False
        self.device = None
        self.add_event('added_device')
        self.add_event('removed_device')
        gtk.gdk.threads_init()
        gtk.gdk.threads_enter()
        self.model = uadh.VoidObject()
        #self.data.model.datapath = '/usr/share/nugget-data/'
        self.model.datapath = datapath
        self.view = gtk2gui.GtkWindow('Nugget 0.7.8')
        self.view.connect('destroy',self.on_exit)
        self.controller = DeviceController()
        self.controller.connect('added_device', self.on_added_device)
        self.controller.connect('removed_device', self.on_removed_device)
        if self.controller.device_active <> None:
            self.on_added_device()
        #plugins.admin.load_plugins(self, '/usr/lib/nugget/')
        plugins.admin.load_plugins(self, pluginspath)
        self.view.show_all()
        gtk.main()
        gtk.gdk.threads_leave()
    
    def on_added_device(self, *a):
        print 'dispositivo detectado'
        if not self._added:
            self._added = True
            self.device = mobile.MobilePhone(self.controller.device_active.port['conf'])
            self.emit('added_device')
            time.sleep(3)

    def on_removed_device(self,*a):
        print 'dispositivo removido'
        self.emit('removed_device')
        if self.device <> None:
            self.device.power_off()
        self.device = None

    def on_exit(self, *a):
        print 'cerrando Nugget'
        self.controller.stop()
        if self.device <> None:
            self.device.power_off()

if __name__ == '__main__':
    nugget3g = Nugget()
    pass