'''
Created on 26/10/2011

@author: ariel
'''

from setuptools import setup, find_packages  
  
setup(name='Nugget',
      version='0.6',
      description='Un dialer para modems 3G/4G',
      author='Grupo Uremix',
      author_email='uremix@googlegroups.com',
      url='https://github.com/arielvega/Nugget',
      license='GPL',
      scripts=['Nugget', 'simple-nugget.py'],
      py_modules=['Devices', 'DevicesController'],
      packages = find_packages(),
      install_requires = ['python-mobile >= 0.2', 'uremix-app-developer-helper >= 0.1', 'python-configobj', 'python-dbus', 'python-gtk2']
)