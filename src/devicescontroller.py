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

import time
import uadh
from devices import DevicesAvalaible
import pyudev
from pyudev.glib import GUDevMonitorObserver

class DeviceController(uadh.CommonThread):

    def __init__(self):
        uadh.CommonThread.__init__(self)
        self.add_event('added_device')
        self.add_event('removed_device')
        
        self.context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(self.context)
        monitor.filter_by(subsystem='usb-serial')
        observer = GUDevMonitorObserver(monitor)
        observer.connect("device-added", self.__on_device_added)
        observer.connect("device-removed", self.__on_device_removed)
        
        self.devices_avalaible = DevicesAvalaible()
        self.device_active = None
        #self.available_devices = []
        monitor.enable_receiving()
        self.start()

    def execute(self):
        self.__hardware_detection()
        time.sleep(1)

    def __hardware_detection(self):
        if self.device_active == None:
            self.device_active = self.devices_avalaible.get_device()
            if(self.device_active != None):
                print "Dispositivo reconocido "
                self.emit('added_device')
                print self.device_active
            else:
                print "Dispositivo no encontrado"

    def __on_device_added(self, monitor, device):
        pass

    def __on_device_removed(self, udi, device):
        if (self.device_active != None):
            port = device['DEVPATH']
            port = port[port.rfind('/')+1:]
            if(self.device_active.has_port(port)):
                self.device_active = None
                self.emit('removed_device')
                print "unplug device"
