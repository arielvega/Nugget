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
import gtk
import gobject

from uadh import configurator
from uadh.gui import gtk2gui, base

from uadh.plugins import Plugin
import mobile


basepath = './'#'/usr/share/nugget-data/'


class Main(Plugin):
    def __init__(self, data):
        Plugin.__init__(self, data)
        self._view = data.view

    def run(self):
        s = base.Section('Prepago', PrepaidGui(self._data))
        self._view.add_section(s)
        pass

    def get_id(self):
        return 'prepaid-plugin'

class PrepaidGui(gtk.Table):
    def __init__(self, data):
        gtk.Table.__init__(self, rows = 5, columns = 1)
        self.conf = None
        self._mainView = data.view
        self.data = data
        self.attach(ChargeGui(self), 0, 1, 1, 2, xpadding = 10, ypadding = 10, xoptions = gtk.EXPAND | gtk.FILL, yoptions=False)
        self.attach(SelectPlanGui(self), 0, 1, 0, 1, xpadding = 10, ypadding = 10, xoptions = gtk.EXPAND | gtk.FILL, yoptions=False)
        self._lblStatus = gtk.Label()
        self.attach(self._lblStatus, 0, 1, 2, 3, xpadding = 10, ypadding = 10, xoptions = gtk.EXPAND | gtk.FILL, yoptions=False)

    def send_message(self, number, message):
        dev = self.data.device
        if (dev<>None) and (len(number)>0) and (len(message)>0):
            sms = dev.create_sms(message, number)
            if sms.send():
                self.show_message('Mensaje enviado a ' + number)
                pass
            else:
                self.show_message('No se pudo enviar mensaje a ' + number)
                pass
        else:
            if (dev == None):
                self.show_message('No se encontro dispositivo')
                return
            if (len(number) == 0):
                self.show_message('Debe introducir un telefono')
                return
            if (len(message) == 0):
                self.show_message('Debe escribir su mensaje')
                return

    def make_call(self, number):
        dev = self.data.device
        if (dev <> None) and (len(number)>0):
            if dev.call(number):
                self.show_message('Llamada exitosa a ' + number)
            else:
                self.show_message('No se pudo llamar a ' + number)
        else:
            if (dev == None):
                self.show_message('No se encontro dispositivo')
                return
            if (len(number) == 0):
                self.show_message('Debe introducir un telefono')
                return

    def get_config(self, obj):
        if self.conf <> None:
            return self.conf[obj]
        dev = self.data.device
        if (dev <> None):
            configmanager = configurator.ConfConfigurator(basepath + 'conf/countries')
            self.conf = configmanager.get_configuration('/' + dev.get_country_code() + '/' + dev.get_network_code() + '/prepaid.conf')
        if self.conf <> None:
            return self.conf[obj]
        else:
            return None

    def show_message(self, text):
        self._lblStatus.set_text(text)


class ChargeGui(gtk.Frame):
    def __init__(self, gui):
        gtk.Frame.__init__(self)
        self.gui = gui
        lbl = gtk.Label()
        lbl.set_markup('<b>Cargar crédito</b>')
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_label_widget(lbl)
        table = gtk.Table(rows = 2, columns = 3)
        table.attach(gtk.Label('Código secreto:'), 0, 1, 0, 1, xpadding = 10, ypadding = 10, xoptions=False, yoptions=False)
        self._txtSecretCode = gtk.Entry()
        table.attach(self._txtSecretCode, 1, 3, 0, 1, xpadding = 10, ypadding = 10, xoptions = gtk.EXPAND | gtk.FILL, yoptions=False)
        bbox = gtk.HButtonBox()
        self._btnCredit = gtk.Button('Ver saldo')
        self._btnData = gtk.Button('Ver consumo')
        self._btnOk = gtk.Button('Aceptar')
        bbox.pack_end(self._btnCredit)
        bbox.pack_end(self._btnData)
        bbox.pack_end(self._btnOk)
        self._btnCredit.connect('clicked', self.on_credit_click)
        self._btnData.connect('clicked', self.on_data_click)
        self._btnOk.connect('clicked', self.on_ok_click)
        bbox.set_spacing(10)
        table.attach(bbox,0,3,1,2, xpadding = 10, ypadding = 10, xoptions=False, yoptions=False)
        self.add(table)

    def credit_charge(self):
        self.gui.show_message('')
        secret_code = self._txtSecretCode.get_text()
        if len(secret_code) > 0:
            config = self.gui.get_config('charge')
            if (config <> None):
                number = config['NUMBER']
                method_string = config['METHOD_STRING']
                method_string = method_string.replace('SECRET_CODE', secret_code)
                method_string = method_string.replace('NUMBER', number)
                if config['METHOD'] <> 'sms':
                    self.gui.make_call(method_string)
                else:
                    self.gui.send_message(number, method_string)
                self._txtSecretCode.set_text('')
        else:
            self.gui.show_message('Debe introducir el codigo secreto de la tarjeta')

    def view_credit(self):
        self.gui.show_message('')
        config = self.gui.get_config('credit_query')
        if (config <> None):
            number = config['NUMBER']
            method_string = config['METHOD_STRING']
            method_string = method_string.replace('NUMBER', number)
            if config['METHOD'] <> 'sms':
                self.gui.make_call(method_string)
            else:
                self.gui.send_message(number, method_string)

    def view_data(self):
        self.gui.show_message('')
        config = self.gui.get_config('data_query')
        if (config <> None):
            number = config['NUMBER']
            method_string = config['METHOD_STRING']
            method_string = method_string.replace('NUMBER', number)
            if config['METHOD'] <> 'sms':
                self.gui.make_call(method_string)
            else:
                self.gui.send_message(number, method_string)

    def on_credit_click(self, *w):
        self.view_credit()

    def on_data_click(self, *w):
        self.view_data()

    def on_ok_click(self, *w):
        self.credit_charge()



class SelectPlanGui(gtk.Frame):
    def __init__(self, gui):
        gtk.Frame.__init__(self)
        self.gui = gui
        lbl = gtk.Label()
        lbl.set_markup('<b>Elegir plan</b>')
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_label_widget(lbl)
        table = gtk.Table(rows = 4, columns = 4)
        table.attach(gtk.Fixed(),0,2,0,1, ypadding = 5, xoptions=False)
        table.attach(gtk.Label('Plan:'),0,1,1,2, xpadding = 10, ypadding = 5, xoptions=False, yoptions=False)

        frmPlan = gtk.Frame()
        lbl = gtk.Label()
        lbl.set_markup('<b>Datos del plan:</b>')
        #frmPlan.set_shadow_type(gtk.SHADOW_NONE)
        frmPlan.set_label_widget(lbl)
        self._lblPlan = gtk.Label()
        self._lblPlan.set_line_wrap(True)
        self._lblPlan.set_padding(5,5)
        frmPlan.add(self._lblPlan)
        table.attach(frmPlan,2,4,0,4, xpadding = 10, ypadding = 10)

        self._cmbPlan = gtk2gui.ComboBoxObject(gtk2gui.SecuenceViewer())
        
        self.gui.data.controller.connect('added_device', self.on_added_device)
        self.gui.data.controller.connect('removed_device', self.on_removed_device)
        self._cmbPlan.connect('show', self.on_added_device)
        self._cmbPlan.connect('changed', self.on_plan_changed)

        table.attach(self._cmbPlan,1,2,1,2, xpadding = 10, ypadding = 5, xoptions=False, yoptions=False)
        bbox = gtk.HButtonBox()
        self._btnOk = gtk.Button('Aceptar')
        self._btnOk.connect('clicked', self.on_ok_click)
        bbox.pack_end(self._btnOk)
        table.attach(bbox,0,2,2,3, xpadding = 0, ypadding = 5, xoptions=False, yoptions=False)
        table.attach(gtk.Fixed(),0,2,3,4, ypadding = 5, xoptions=False)
        #table.attach(gtk.Fixed(),3,4,1,2)
        self.add(table)

    def on_added_device(self, *w):
        self.load_plans()

    def on_removed_device(self, *w):
        self.load_plans()

    def load_plans(self):
        config = self.gui.get_config('select_plan')
        self._cmbPlan.get_model().clear()
        if (config <> None):
            options = config['OPTIONS']
            union = ','.join(options)
            if union.count('(') > 0:
                options = union
                options = options.replace('( ', '(')
                options = options.replace(') ', ')')
                options = options.replace(' (', '(')
                options = options.replace(' )', ')')
                options = [z.split(',') for z in  [ y[0].split(')')[0] for y in [x.split('),') for x in options.split('(')] if len(y)>0 and len(y[0])>0 ]]
                for opt in options:
                    self._cmbPlan.get_model().append([opt])
            else:
                options = [x.strip() for x in options]
                tuples = []
                try:
                    for opt in options:
                        config = self.gui.get_config('select_plan.' + opt)
                        tuples.append((config['NAME'], config['OPTION']))
                    for tuple in tuples:
                        self._cmbPlan.get_model().append([tuple])
                except:
                    for opt in options:
                        self._cmbPlan.get_model().append([(opt,)])


    def select_plan(self):
        try:
            selected = self._cmbPlan.get_model().get(self._cmbPlan.get_active_iter(), 0)
            selected = selected[-1][-1]
            if selected <> None or len(selected) > 0:
                config = self.gui.get_config('select_plan')
                if (config <> None):
                    number = config['NUMBER']
                    method_string = config['METHOD_STRING']
                    method_string = method_string.replace('SELECTED', selected)
                    method_string = method_string.replace('NUMBER', number)
                    if config['METHOD'] <> 'sms':
                        self.gui.make_call(method_string)
                    else:
                        self.gui.send_message(number, method_string)
            else:
                self.gui.show_message('Debe seleccionar el plan')
        except:
            self.gui.show_message('Debe seleccionar el plan')

    def show_plan(self):
        try:
            selected = self._cmbPlan.get_model().get(self._cmbPlan.get_active_iter(), 0)
            selected = selected[-1][-1]
            if selected <> None or len(selected) > 0:
                config = self.gui.get_config('select_plan.' + selected)
                if (config <> None):
                    string = config['DESCRIPTION'] + '\n<b>Costo:</b> ' + config['COST'] + '\n<b>Duración:</b> ' + config['DURATION']
                    self._lblPlan.set_markup(string)
            else:
                self.gui.show_message('Debe seleccionar el plan')
        except:
            self.gui.show_message('Debe seleccionar el plan')

    def on_ok_click(self, *w):
        self.select_plan()

    def on_plan_changed(self, *w):
        self.show_plan()
