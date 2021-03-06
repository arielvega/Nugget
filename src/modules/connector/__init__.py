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
import gtk, os, threading, gobject
from gtk import glade

from uadh.gui import gtk2gui, base
from uadh.plugins import Plugin
import mobile
from dialermonitor import Monitor 
from progress import ProgressDialog
from subprocess import Popen, PIPE
from status import *

basepath = './'#'/usr/share/nugget-data/'

class Main(Plugin):
    def __init__(self, data):
        Plugin.__init__(self, data)
        self._view = data.view

    def run(self):
        #s = base.Section('Conectar',ConnectorGui(self._data))
        #self._view.add_section(s)
        pass

    def get_id(self):
        return 'connector-plugin'

class ConnectorGui(gtk.Table):
    def __init__(self, data):
        gtk.Table.__init__(self, rows = 3, columns = 4)
        self._mainView = data.view
        self._data = data
        self.attach(gtk.Fixed(),0,4,0,1)
        self.attach(gtk.Fixed(),0,1,1,2, xpadding = 10, ypadding = 10)
        self._cmbOperators = gtk.ComboBox()
        self.attach(self._cmbOperators,1,2,1,2, xpadding = 10, ypadding = 10, xoptions = gtk.EXPAND | gtk.FILL, yoptions=False)
        self._btnConnect = gtk.ToggleButton('Conectar')
        self.attach(self._btnConnect,2,3,1,2, xpadding = 10, ypadding = 10, xoptions = gtk.EXPAND | gtk.FILL, yoptions=False)
        self.attach(gtk.Fixed(),3,4,1,2, xpadding = 10, ypadding = 10, xoptions = gtk.EXPAND | gtk.FILL, yoptions=False)
        self.attach(gtk.Fixed(),0,4,2,3)

        #Instances
        self.__dialog = ProgressDialog(self._mainView)
        self.controller = self._data.controller
        self.operators = []
        self.mon = Monitor()
        
        if(self.controller.device_active != None):
            self._mainView.set_status_message("Dispositivo activo: " + self.controller.device_active.name)
        
        self.build_list_operators()
        self.build_combo_operators()
        
        #signals
        self.__dialog.button.connect("clicked",self.cancel_connection,self.__dialog)
        self._btnConnect.connect("pressed",self.connect)
        self.controller.connect('added_device',self.__plug)
        self.controller.connect('removed_device',self.__unplug)
        self.mon.connect('connecting',self.__connecting_dialog)
        self.mon.connect('connected',self.__connected_dialog)
        self.mon.connect('disconnecting',self.__disconnecting_dialog)
        self.mon.connect('disconnected',self.__disconnected_dialog)
        self.mon.connect('connecting_state_change',self.__connecting_dialog)

    def __connecting_dialog(self,monitor,data = None):
        if(data == None):
            self._mainView.set_status_message("Conectando...")
        else:
            self._mainView.set_status_message(data)

    def __connected_dialog(self,monitor):
        self.__dialog.hide()
        self._btnConnect.set_label("Desconectar")
        self._btnConnect.set_active(True)

    def __disconnecting_dialog(self,monitor):
        self._mainView.set_status_message("Desconectando...")

    def __disconnected_dialog(self,monitor):
        self.__dialog.should_change = False
        self.__dialog.image.set_from_file(basepath + 'icons/network-error.png')
        self._mainView.set_status_message("Error")
        self.__dialog.button.set_label("Cerrar")

    def __plug(self,m_controller,dev):
        self._mainView.set_status_message("Dispositivo activo: "+dev)

    def __unplug(self,m_controller):
        self._mainView.set_status_message('No hay ningun dispositivo activo')

    def build_list_operators(self):
        from xml.dom.minidom import parse
        midom = parse(basepath + 'conf/operators.xml')
        m_operators = midom.childNodes[0].childNodes
        for m_operator in m_operators:
            if (m_operator.nodeType == 1):
                op = Operator()
                op.add("name",m_operator.attributes.get("name").value)
                attribs = m_operator.childNodes
                for attrib in attribs:
                    if(attrib.nodeType == 1):
                        op.add(attrib.nodeName,attrib.childNodes[0].data)
                self.operators.append(op)

    def connect(self,widget, data = None):
        if (self.mon.status() == PPP_STATUS_DISCONNECTED):
            active = self._cmbOperators.get_active()
            self.__dialog.show()
            self.mon.start(self.operators[active],self.controller.device_active.port['data'])
        else:
            widget.set_label("Conectar")
            self.mon.stop()

    def cancel_connection(self,widget,dialog,data = None):
        if(self.mon.status() == PPP_STATUS_CONNECTING):
            self.mon.stop()
            return
        if(self.mon.status() == PPP_STATUS_DISCONNECTED):
            dialog.hide()

    def build_combo_operators(self):
        liststore = gtk.ListStore(gtk.gdk.Pixbuf,str)
        px = gtk.CellRendererPixbuf() 
        cell = gtk.CellRendererText()
        self._cmbOperators.pack_start(px)
        self._cmbOperators.pack_start(cell)
        self._cmbOperators.add_attribute(px, 'pixbuf', 0)
        self._cmbOperators.add_attribute(cell, 'text', 1) 
        for i in self.operators:
            iter = liststore.append()
            liststore.set_value(iter, 1, i.get_attrib('name'))
            logo_path = basepath + "icons/"+i.get_attrib('logo')+ '.png'
            if os.path.exists(logo_path):
                liststore.set_value(iter, 0, gtk.gdk.pixbuf_new_from_file(logo_path))
        self._cmbOperators.set_model(liststore)
        self._cmbOperators.set_active(-1)


class Operator:
    
    def __init__(self):
        self.__attrib={}
        self.__attrib["name"]=""
        self.__attrib["phone"]=""
        self.__attrib["username"]=""
        self.__attrib["password"]=""
        self.__attrib["logo"]=""
        self.__attrib["stupid_mode"]=""
    
    def add(self,atr,data):
        self.__attrib[atr]=data
    
    def get_attrib(self,atr):
        return self.__attrib[atr]
