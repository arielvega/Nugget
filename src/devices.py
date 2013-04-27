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
Created on 26/04/2013

@author: Uremix Team (http://uremix.org)

'''

import mobile

class Device:
    def __init__(self):
        self.name = None
        self.vendor = None
        self.product = None
        self.dev_props = None
        self.IMEI = None
        self.port = {}

    def get_port(self,name):
        return self.port[name]

    def has_port(self,port):
        port = port[port.rfind('/')+1:]
        for localport in self.port.values():
            if localport == port:
                return True
        return False

class DevicesAvalaible:
    def __init__(self):
        pass

    def is_device_supported(self,idVendor,idProduct):
        return True

    def get_device(self):
        l = mobile.list_at_terminals()
        if len(l)>0:
            mydevice = Device()
            (mydevice.IMEI,ports) = l.items()[0]
            mobiledevice = mobile.MobileDevice(ports[-1])
            mydevice.vendor = mobiledevice.get_manufacturer()
            mydevice.product = mobiledevice.get_model()
            mydevice.name = mydevice.vendor + ' ' + mydevice.product
            ports.sort()
            mobiledevice.power_off()
            portname = ports[0].get_port_name()
            mydevice.port['data'] = portname[portname.rfind('/')+1:]
            if len(ports)>1:
                portname = ports[-1].get_port_name()
                mydevice.port['conf'] = portname[portname.rfind('/')+1:]
            else:
                mydevice.port['conf'] = None
            return mydevice
        else:
            return None
