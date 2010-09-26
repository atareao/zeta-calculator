#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
#
__author__='atareao'
__date__ ='$06-jun-2010 12:34:44$'
#
# <one line to give the program's name and a brief idea of what it does.>
#
# Copyright (C) 2010 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
import gtk

class Licencia:
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file('licencia.glade')
		#
		self.window = self.builder.get_object('dialog')
		self.button1 = self.builder.get_object('button1')
		#
		self.window.show_all()
		# Magia :P
		self.builder.connect_signals(self)	
		#

	def on_button1_clicked(self,widget):
		self.window.hide()	
