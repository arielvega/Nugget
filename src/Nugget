'''
Created on 02/10/2011

@author: ariel
'''
#!/usr/bin/python

import pygtk
pygtk.require20()
import gtk

from uadh import plugins
from uadh.gui import gtk2gui
from DevicesController import DeviceController

class VoidObject:
    pass

if __name__ == '__main__':
    gtk.gdk.threads_init()
    gtk.gdk.threads_enter()
    data = VoidObject()
    data.model = VoidObject()
    data.model.controller = DeviceController()
    data.view = gtk2gui.GtkWindow('Nugget')
    plugins.admin.load_plugins(data)
    data.view.show_all()
    gtk.main()
    gtk.gdk.threads_leave()
    pass