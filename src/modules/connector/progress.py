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
Created on 02/11/2011

@author: Uremix Team (http://uremix.org)

'''

try:
    import pygtk
    pygtk.require("2.0")
    import gtk
    import gobject
except Exception, detail:
    print detail

base = '/usr/share/nugget-data/'

class ProgressDialog(gtk.Dialog):
    
    def __init__(self, parentw):
        gtk.Dialog.__init__(self, title = 'Conectar...', parent = parentw, flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        self.hbox = gtk.HBox()
        self.vbox.pack_start(self.hbox)
        self.image = gtk.Image()
        self.image.set_from_file(base + 'icons/network-transmit.png')
        self.label = gtk.Label('...')
        self.hbox.pack_start(self.image)
        self.hbox.pack_start(self.label)
        self.button = gtk.Button('Cancelar')
        self.action_area.pack_end(self.button)
        self.should_change = True
        self.__switch = True
        self.set_size_request(250, 100)
        self.set_decorated(False)

    def show(self):
        def image_change():
            if(not self.should_change):
                return False
            if(self.__switch):
                self.image.set_from_file(base + 'icons/network-transmit.png')
                self.__switch = False
            else:
                self.image.set_from_file(base + 'icons/network-receive.png')
                self.__switch = True
            return self.should_change
        self.should_change = True
        self.show_all()
        gobject.timeout_add_seconds(1, image_change)

    def hide(self):
        self.__should_change = False
        super(ProgressDialog, self).hide()
        self.button.set_label('Cancelar')
        self.image.set_from_file(base + 'icons/network-transmit.png')