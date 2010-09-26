#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
#
__author__="atareao"
__date__ ="$26-septiembre-2010"
#
# <one line to give the program"s name and a brief idea of what it does.>
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
import httplib
import os
import gtk
from lxml import etree
from ACercaDe import ACercaDe

class MainWindow:
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file("zeta.glade")
		#
		self.window1 = self.builder.get_object("window1")
		self.button1 = self.builder.get_object("button1") # Seleccionar archivo origen
		self.button2 = self.builder.get_object("button2") # Seleccionar archivo salida
		self.button3 = self.builder.get_object("button3") # Aplicar
		self.button4 = self.builder.get_object("button4") # Salir
		self.entry1 = self.builder.get_object("entry1") # Archivo origen
		self.entry2 = self.builder.get_object("entry2") # Archivo salida
		#
		self.window1.show_all()
		# Magia :P
		self.builder.connect_signals(self)

	def on_window1_destroy(self,widget):
		exit()
		
	def on_button1_clicked(self,widget):
		dialog = gtk.FileChooserDialog("Selecciona archivo kml original",
										   None,
										   gtk.FILE_CHOOSER_ACTION_OPEN,
										   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
											gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		dialog.set_select_multiple(False)
		filter = gtk.FileFilter()
		filter.set_name("Kml")
		filter.add_pattern("*.kml")
		dialog.add_filter(filter)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			filename = dialog.get_filename()
			dialog.destroy()
			self.entry1.set_text(filename)
		else:
			dialog.destroy()
			
	def on_button2_clicked(self,widget):
		dialog = gtk.FileChooserDialog("Selecciona archivo kml para guardar",
										   None,
										   gtk.FILE_CHOOSER_ACTION_SAVE,
										   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
											gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		dialog.set_select_multiple(False)
		filter = gtk.FileFilter()
		filter.set_name("Kml")
		filter.add_pattern("*.kml")
		dialog.add_filter(filter)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			filename = dialog.get_filename()
			dialog.destroy()
			if filename.endswith(".kml")==False:
				filename+=".kml"
			self.entry2.set_text(filename)
		else:
			dialog.destroy()	
	
	def on_button3_clicked(self,widget):
		if (len(self.entry1.get_text())>0) & (os.path.exists(self.entry1.get_text())==True) & (len(self.entry2.get_text())>0):
			widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
			self.conn = httplib.HTTPConnection("www.geonames.org")
			tree = etree.parse(self.entry1.get_text())
			root = tree.getroot()
			for element in list(root):
				if element.tag.endswith("Document"):
					elements=[]
					for element2 in list(element):
						elements+=self.buscaplacemarks(element2)
			tree._setroot(root)
			tree.write(self.entry2.get_text())
			widget.window.set_cursor(None)
				
	def on_button4_clicked(self,widget):
		exit()

	def on_imagemenuitem5_activate(self,widget):
		exit()

	def on_imagemenuitem10_activate(self,widget):
		a=ACercaDe()
		
		
	def modcoordenadas(self,cadena):
		coordenadas=cadena.split(' ')
		newcoordenadas=""
		for coordenada in coordenadas:
			xyz=coordenada.split(',')
			if len(xyz)>1:
				z=self.calculaz(xyz[0],xyz[1])
				if z!="Error":
					newcoordenada=xyz[0]+","+xyz[1]+","+z
					newcoordenadas+=newcoordenada+" "
		return newcoordenadas	

	def calculaz(self,x,y):
		strt="/gtopo30?lat="+str(x)+"&lng="+str(y)
		self.conn.request("GET", strt)
		res = self.conn.getresponse()
		if res.reason=="OK":
			z=str(float(res.read()))
			return z
		else:
			return "Error"

	def buscaplacemarks(self,element):
		elements=[]
		if element.tag.endswith("Folder"):
			for inFolder in list(element):
				elements+=self.buscaplacemarks(inFolder)
		else:
			if element.tag.endswith("Placemark"):
				elements.append(element)
				for hijo in list(element):
					if hijo.tag.endswith("Point") | hijo.tag.endswith("LineString") | hijo.tag.endswith("LinearRing") | hijo.tag.endswith("Polygon") | hijo.tag.endswith("MultiGeometry"):
						for propiedad in list(hijo):
							if propiedad.tag.endswith("coordinates"):
								propiedad.text=self.modcoordenadas(propiedad.text)
		return elements	

if __name__ == "__main__":
	"""
	conn = httplib.HTTPConnection("www.geonames.org")
	tree = etree.parse('caca.kml')
	root = tree.getroot()
	for element in list(root):
		if element.tag.endswith("Document"):
			elements=[]
			for element2 in list(element):
				elements+=buscaplacemarks(conn,element2)
	tree._setroot(root)
	tree.write('salida.kml')
	"""
	v = MainWindow()
	gtk.main()

