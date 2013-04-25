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

from xml.dom.minidom import parse

#base = '/usr/share/nugget-data/'
base = './'

class Device:
    def __init__(self):
        self.name = None
        self.vendor = None
        self.product = None
        self.dev_props = None
        self.port = {}

    def get_port(self,str):
        return self.port[str]

class DevicesAvalaible:
    def __init__(self):
        midom=parse(base + "conf/modems.xml")
        self.vendors = midom.childNodes[1].childNodes
        self.__nProduct = None
        self.__nVendor = None

    def is_device_supported(self,idVendor,idProduct):
        for vendor in self.vendors:
            if(vendor.nodeType==1):
                if(vendor.attributes.get("id").value==idVendor):
                    products = vendor.childNodes
                    for product in products:
                        if(product.nodeType==1):
                            if(product.attributes.get("id").value==idProduct):
                                self.__nProduct = product
                                self.__nVendor = vendor
                                return True
                    break
        return False

    def get_Device(self):
        if(self.__nProduct != None):
            d = Device()
            d.name = self.__nVendor.attributes.get("name").value
            d.vendor = self.__nVendor.attributes.get("id").value
            d.product = self.__nProduct.attributes.get("id").value
            attribs = self.__nProduct.childNodes
            for attrib in attribs:
                if(attrib.nodeType == 1 and attrib.nodeName != "capabilities"):
                    d.port[attrib.nodeName] = attrib.childNodes[0].data
            return d
        return None