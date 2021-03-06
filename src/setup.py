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
Created on 26/10/2011
Updated on 24/04/2013

@author: Uremix Team (http://uremix.org)

'''

from setuptools import setup, find_packages  
  
setup(name='nugget',
      version='0.7.8',
      description='Un dialer para modems 3G/4G',
      author='Grupo Uremix',
      author_email='uremix@googlegroups.com',
      url='https://github.com/arielvega/Nugget',
      license='GPL V3',
      scripts=['nugget'],
      install_requires = ['python-mobile >= 0.2', 'uremix-app-developer-helper >= 0.1', 'python-configobj', 'python-dbus', 'python-gtk2', 'python-gobject','hal >=0.5']
)
