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
Created on 11/08/2012

@author: Uremix Team (http://uremix.org)

'''

import gobject
from Devices import *
import pyudev
from pyudev.glib import GUDevMonitorObserver

class DeviceController(gobject.GObject):

    __gsignals__ = {'added_device' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,(gobject.TYPE_STRING,)),
                    'removed_device' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,())}

    def __init__(self):
        gobject.GObject.__init__(self)
        
        self.context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(self.context)
        observer = GUDevMonitorObserver(monitor)
        observer.connect("device-added", self.__plug_device_cb)
        observer.connect("device-removed", self.__unplug_device_cb)
        
        self.devices_avalaible = DevicesAvalaible()
        self.device_active = None
        self.__first_time_hardware_detection()
        self.available_devices = []
        monitor.enable_receiving()
        
    def __first_time_hardware_detection(self):
        for device in self.context.list_devices(subsystem='usb-serial'):        
            attr = device.attributes
            try:
                if(attr['idVendor']!=None):
                    if self.devices_avalaible.is_device_supported(attr['idVendor'],attr['idProduct']):
                        self.device_active = self.devices_avalaible.get_Device()
                        self.emit('added_device',self.device_active.name)
                        break
            except Exception:
                pass
        if(self.device_active!=None):
            self.get_ports()
            print self.device_active
        else:
            print "Dispositivo no encontrado"
        self.devices = []
    
    def get_ports(self):
        ports=[]
        for device in self.context.list_devices(subsystem='usb-serial'):
            ports.append(device.sys_name)
        ports.sort()
        if(len(ports)<1):
            print "Dispositivo no reconocido por el sistema"
            self.device_active = None
        else:
            try:
                data = self.device_active.port['data']
                self.device_active.port['data'] = ports[int(data)]
            except:
                pass
            try:
                conf = self.device_active.port['conf']
                self.device_active.port['conf'] = ports[int(conf)]
            except:
                pass
            print "Dispositivo reconocido "
            self.emit('added_device',self.device_active.name)


    def __plug_device_cb(self, monitor, device):
        attr = device.attributes
        try:
            if(attr['idVendor'] != None):
                if self.devices_avalaible.is_device_supported(attr['idVendor'],attr['idProduct']):
                    self.device_active = self.devices_avalaible.get_Device()
                    self.emit('added_device',self.device_active.name)
        except Exception:
            pass
        

    def __unplug_device_cb(self, udi):
        if (self.device_active != None):
            if(self.device_active.dev_props['info.udi'] == udi):
                self.device_active = None
                self.emit('removed_device')
                print "unplug device"