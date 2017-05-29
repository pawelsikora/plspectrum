#!/usr/bin/env python

import pygtk
import gtk
pygtk.require('2.0')
from common import *

import linecache
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

__author__ = "Piotr Ruszala"
__version__ = "0.1"

class Parameters:	
	def __init__(self):
		self.A0 = 10.0
		self.g0 = 1.0
		self.Eg = 1.1828#
		self.T = 300#
		self.gamma = 0.001#
		self.gamma2 = 1.0#
		self.gamma_schodek=35.0
		self.gamma_schodek2=5.0
		self.Ef = 0.5 * self.Eg
		self.E = np.arange(1.08,1.35,0.001)#
		self.En = np.array([0.49475 + 0.69223 - self.Eg, 0.54384+0.7062 - self.Eg, 0.60827 + 0.7275 - self.Eg])
		self.CP = np.array([0.98453, 0.94166, 0.79406])
			
		self.a=np.zeros(len(self.E))
		self.g_bulk=np.zeros(len(self.E))
		self.DOS=np.zeros(len(self.E))
		self.DOS2=np.zeros(len(self.E))
		self.Pik=np.zeros(len(self.E))
		self.Normal=np.zeros(len(self.E))
		self.Pik_mieszany=np.zeros(len(self.E))
		self.Hevisajd=np.zeros(len(self.E))
		self.Delty=np.zeros(len(self.E))
		self.Epocz=np.zeros(len(self.E))
		self.Widmo=np.zeros(len(self.E))
		self.Prawd=np.zeros(len(self.E))
		self.LAMBDA = (1.24 / self.E)
	
	def get_A0(self):
		return self.A0

	def get_g0(self):
		return self.g0

	def get_Eg(self):
		return self.Eg

	def get_T(self):
		return self.T

	def get_gamma(self):
		return self.gamma

	def get_gamma2(self):
		return self.gamma2
	
	def get_gamma_schodek(self):
		return self.gamma_schodek
	
	def get_gamma_schodek2(self):
		return self.gamma_schodek2
	
	def get_Ef(self):
		return self.Ef

	def set_g0(self, g0):
		self.g0 = g0

	def set_Eg(self, Eg):
		self.Eg = Eg
		self.Ef = 0.5 * Eg
	
	def set_T(self, T):
		self.T = T

	def set_gamma(self, gamma):
		self.gamma = gamma
	
	def set_gamma2(self, gamma2):
		self.gamma2 = gamma2

	def set_gamma_schodek(self, gamma_schodek):
		self.gamma_schodek = gamma_schodek

	def set_gamma_schodek2(self, gamma_schodek2):
		self.gamma_schodek_2 = gamma_schodek2

	def read_params_from_UI(self):
		return 0
	
	def update(self):
		return 0
		
class Spectrum_generator:

	def __init__(self):
		self.DOS = 0 
		self.DOS2 = 0
		self.Hevisajd = 0 
		self.Pik = 0
		self.Normal = 0
		self.Pik_mieszany = 0
		self.Delty= 0
		self.params = Parameters()
		self.params.update()
		
	def delta_cal(self):	
		for i in range(0, len(self.params.En)):
			self.DOS = self.DOS + self.params.g0 * self.params.CP[i] * (DOS_rozmyty_erf(self.params.E, self.params.Eg + self.params.En[i], self.params.gamma_schodek))
			self.DOS2 = self.DOS2 + self.params.g0 * self.params.CP[i] * (DOS_rozmyty_cauchy(self.params.E, self.params.Eg + self.params.En[i], self.params.gamma_schodek))
			self.Hevisajd = self.Hevisajd + self.params.g0 * self.params.CP[i] * Schodek(self.params.E-self.params.Eg-self.params.En[i])
			self.Pik = self.Pik + self.params.A0 * (pik_Lorentza(self.params.E, self.params.Eg + self.params.En[i], self.params.gamma))
			self.Normal = self.Normal + self.params.A0 * pik_Gaussowski(self.params.E, self.params.Eg + self.params.En[i], self.params.gamma)
			self.Pik_mieszany = self.Pik_mieszany + self.params.A0 * (pik_Lorentza(self.params.E, self.params.Eg + self.params.En[i], self.params.gamma) + pik_Gaussowski(self.params.E, self.params.Eg+self.params.En[i], self.params.gamma))
			self.Delty=self.Delty+self.params.A0*Delta(self.params.E-self.params.Eg-self.params.En[i])


	def energia_pocz(self):
		for i in range(0,len(self.params.E)):
			if self.params.E[i]<=(self.params.Eg+self.params.En[0]):
				self.params.Epocz[i]=0.0
			else:
				self.params.Epocz[i]=1.0
	def widmo_fd(self):
		self.Widmo_fd = self.Pik * self.DOS * distribution_FD(self.params.E, self.params.Ef, self.params.T)
	
	def widmo_boltzmann(self):
		self.Widmo_b = self.Pik*self.DOS*distribution_Boltzmann(0.0, self.params.E, self.params.T)#*Epocz #Epocz to tak naprawde schodek, ucina energie!

	def widmo_planck(self):
		self.Widmo5 = (1.0 / self.params.E) * self.DOS * distribution_Planck(self.params.E, self.params.T) * self.params.E #Widmo PL QW ale obliczone sposobem jak dla Bulku (3D) - absorpcja jedynie zmieniona na dwuwymiarowa! Przypadek rownowagi termodynamicznej!

	def prawdopodobienstwo(self):
		for j in range(0, len(self.params.En)):
			for i in range(0, len(self.params.E)):
			 #*Ogon_gestosci_stanow(E[i], Eg, 0.001, 50.0))
			 self.params.Prawd[i] = self.params.Prawd[i] + Calka(self.params.E, pik_Gaussowski(self.params.E, self.params.E[i], self.params.gamma)*self.DOS*distribution_Boltzmann(0.0, self.params.E, self.params.T))
			 
			 #Prawd[i]=Prawd[i]+Calka(E, Pik_Lorentza(E, E[i], gamma)*DOS*Rozklad_Boltzmanna(0.0, E, T)*Ogon_gestosci_stanow(E[i], Eg-En[0], gamma2, gamma_schodek2))

			#Prawd[i]=Prawd[i]+Calka(E, Delta(E-E[i])*Schodek(E-(Eg+En[j])))
	
	def generate(self, items):
		for i in range(items):
			yield i
	
	def widmo(self):
		self.params.Widmo = self.params.Prawd * self.params.E
	
	def save_to_files(self):
		plik = open('widmo1', 'w')
		plik2 = open('lambda', 'w')
		
		for i in self.generate(len(self.params.Widmo)):
		    plik.write(str(self.params.LAMBDA[i]) + ' '
		               + str(self.params.Widmo[i]/max(self.params.Widmo))
		               + '\n')
		
		for i in self.generate(len(self.params.LAMBDA)):
		    plik2.write(str(self.params.LAMBDA[i]) + '\n')
		
		plik2.close()
		plik.close()

	def calculate_all(self):
		self.delta_cal()
		self.energia_pocz()
		self.widmo_fd()
		self.widmo_boltzmann()
		self.widmo_planck()
		self.prawdopodobienstwo()
		self.widmo()
		self.save_to_files()

	def plot_widmo_alfa(self):
		plt.plot(self.params.E, self.DOS/max(self.DOS), 'r', self.params.E, self.DOS2/max(self.DOS2), 'b', self.params.E, self.Hevisajd/max(self.Hevisajd), 'g', lw=2)
		plt.savefig("plot_alfa.png")
		plt.show()
	
	def plot_widmo_beta(self):
		self.count = len(open('LAMBDA_Zmierzona.txt', 'rU').readlines())
		self.zmierzone_x = open('LAMBDA_Zmierzona.txt', 'rU').readlines()
		self.zmierzone_y = open('Zmierzone1.txt', 'rU').readlines()

		for i in range(0, self.count):
		    self.zmierzone_x[i] = float(self.zmierzone_x[i].strip())
		    self.zmierzone_y[i] = float(self.zmierzone_y[i].strip())
		
		plt.plot(self.params.LAMBDA, self.Widmo5/max(self.Widmo5), 'r', self.params.LAMBDA, self.params.Widmo/max(self.params.Widmo), 'b', self.zmierzone_x, self.zmierzone_y, 'k.', lw=2)
		plt.savefig("plot_beta.png")
		plt.show()
		
class GUI:

    # This is a callback function. The data arguments are ignored
    # in this example. More on callbacks below.
    def generate_graph(self, widget, data=None):
        c = Spectrum_generator()
	c.calculate_all()
	
	#print "Prawd"
	#print c.params.Prawd
	#print "LAMBDA"
	#print c.params.LAMBDA
	#print "Widmo"
	#print c.params.Widmo
	#print "Widmo5"
	#print c.Widmo5

	c.plot_widmo_beta()

    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    	self.window.set_size_request(500, 350)	
	self.entry = gtk.Entry()
        self.entry.set_text("Hello World")
	
	self.hbox = gtk.HButtonBox()
	self.hbox.set_layout(gtk.BUTTONBOX_SPREAD)
	self.hbox.set_border_width(5)
	
	self.bbox = gtk.VButtonBox()
	self.bbox.set_layout(gtk.BUTTONBOX_EDGE)
	self.bbox.set_border_width(5)
        self.bbox.pack_start(self.entry, True, True, 0)	
	
	self.button1 = gtk.Button('Generate graph!')
	self.bbox.add(self.button1)

	self.button2 = gtk.Button('Save graph')
	self.bbox.add(self.button2)

	self.button3 = gtk.Button('Compare two graphs')
	self.bbox.add(self.button3)

        self.window.connect("delete_event", self.delete_event)
    
        self.window.connect("destroy", self.destroy)
    
        self.window.set_border_width(30)
    
        #self.button = gtk.Button("Generate graph!")
    
        self.button1.connect("clicked", self.generate_graph, None)
    
        #self.window.add(self.button)
        self.window.add(self.bbox)
        #self.window.add(self.hbox)
        #self.window.add(self.entry)
    
        #self.button.show()
    	self.window.show_all()
        #self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
	
	gui = GUI()
	gui.main()
