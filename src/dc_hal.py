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
Created on 04/11/2011

@author: Uremix Team (http://uremix.org)

'''

import dbus
import os
import gobject
from devices import *
if getattr(dbus, "version", (0,0,0)) >= (0,41,0):
    import dbus.glib

class DeviceController(gobject.GObject):

    __gsignals__ = {'added_device' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,(gobject.TYPE_STRING,)),
                    'removed_device' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,()),
                    'support_device_detected' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,())}

    def __init__(self):
        gobject.GObject.__init__(self)
        self.dbus = dbus.SystemBus()
        self.hal_manager_obj = self.dbus.get_object("org.freedesktop.Hal", "/org/freedesktop/Hal/Manager")
        self.hal_manager = dbus.Interface(self.hal_manager_obj, "org.freedesktop.Hal.Manager")
        
        #Signals
        self.hal_manager.connect_to_signal("DeviceAdded", self.__plug_device_cb)
        self.hal_manager.connect_to_signal("DeviceRemoved", self.__unplug_device_cb)
        
        self.devices_avalaible = DevicesAvalaible()
        self.device_active = None
        self.__first_time_hardware_detection()
        self.available_devices = []

    def __first_time_hardware_detection(self):
        self.devices = self.hal_manager.GetAllDevices()
        for dev in self.devices:
            device_dbus_obj = self.dbus.get_object("org.freedesktop.Hal", dev)
            try:
                props = device_dbus_obj.GetAllProperties(dbus_interface="org.freedesktop.Hal.Device")
            except:
                return False
            if props.has_key("info.subsystem"):
                if props["info.subsystem"] ==  "usb_device":
                    if props.has_key("usb_device.product_id") and props.has_key("usb_device.product_id"):
                        if  self.devices_avalaible.is_device_supported(str(props["usb_device.vendor_id"]),
                                                                        str(props["usb_device.product_id"])):
                            self.device_active = self.devices_avalaible.get_Device()
                            self.device_active.dev_props = props
                            print props["info.udi"]
                            self.emit('added_device',self.device_active.name)
                            break
        if(self.device_active!=None):
            self.get_ports()
            print self.device_active.name+" "+self.device_active.port['data']
        else:
            print "Dispositivo no encontrado"
        self.devices = []

    def get_ports(self):
        ports = []
        self.devices = self.hal_manager.GetAllDevices()
        for dev in self.devices:
            device_dbus_obj = self.dbus.get_object("org.freedesktop.Hal", dev)
            try:
                props = device_dbus_obj.GetAllProperties(dbus_interface="org.freedesktop.Hal.Device")
            except:
                return False
            if props.has_key("info.parent") and props["info.parent"] == self.device_active.dev_props["info.udi"]:
                    if props.has_key("usb.linux.sysfs_path") :
                        files = os.listdir(props["usb.linux.sysfs_path"])
                        for f in files:
                            if f.startswith("ttyUSB") :
                                ports.append(f)
        ports.sort()
        if(len(ports)<1):
            print "Dispositivo no reconocido por el sistema"
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

    def __real_plug_device_cb(self, udi):
        self.devices.append(udi)
        device_dbus_obj = self.dbus.get_object("org.freedesktop.Hal", udi)
        try:
            dev_props = device_dbus_obj.GetAllProperties(dbus_interface="org.freedesktop.Hal.Device")
        except:
            return False
        if dev_props.has_key("info.subsystem"):
            if dev_props["info.subsystem"] ==  "usb_device":
                if dev_props.has_key("usb_device.product_id") and dev_props.has_key("usb_device.product_id"):
                    print str(dev_props["usb_device.vendor_id"]), str(dev_props["usb_device.product_id"])
                    if  self.devices_avalaible.is_device_supported(str(dev_props["usb_device.vendor_id"]),
                                                                    str(dev_props["usb_device.product_id"])):
                        self.device_active = self.devices_avalaible.get_Device()
                        self.device_active.dev_props = dev_props
                        self.get_ports()
                        self.emit('added_device',self.device_active.name)
                        print udi
                        print "Dispositivo encontrado"
        return False

    def __plug_device_cb(self, udi):
        gobject.timeout_add(3000, self.__real_plug_device_cb, udi)

    def __unplug_device_cb(self, udi):
        if (self.device_active != None):
            if(self.device_active.dev_props['info.udi'] == udi):
                self.device_active = None
                self.emit('removed_device')
                print "unplug device"