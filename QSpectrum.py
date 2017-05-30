#!/usr/bin/env python

from common import *
from gui import *

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

__author__ = "Piotr Ruszala"
__version__ = "0.1"

		
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
			self.DOS = self.DOS + self.params.g0 * self.params.CP[i] * \
				( DOS_rozmyty_erf(self.params.E, self.params.Eg + \
				 self.params.En[i], self.params.gamma_schodek) )
			
			self.DOS2 = self.DOS2 + self.params.g0 * self.params.CP[i] * \
				( DOS_rozmyty_cauchy(self.params.E, self.params.Eg + \
				 self.params.En[i], self.params.gamma_schodek) )
			
			self.Hevisajd = self.Hevisajd + self.params.g0 * \
				self.params.CP[i] * \
				Schodek(self.params.E-self.params.Eg - self.params.En[i])
			
			self.Pik = self.Pik + self.params.A0 * \
				( pik_Lorentza(self.params.E, self.params.Eg + \
				 self.params.En[i], self.params.gamma) )
			
			self.Normal = self.Normal + self.params.A0 * \
				pik_Gaussowski(self.params.E, self.params.Eg + \
				self.params.En[i], self.params.gamma)
			
			self.Pik_mieszany = self.Pik_mieszany + self.params.A0 * \
				( pik_Lorentza(self.params.E, self.params.Eg + \
				  self.params.En[i], self.params.gamma) + \
				  pik_Gaussowski(self.params.E, self.params.Eg + \
				  self.params.En[i], self.params.gamma) )
			
			self.Delty = self.Delty + \
				self.params.A0 * \
				Delta(self.params.E - self.params.Eg - self.params.En[i])


	def energia_pocz(self):
		#'Epocz' to tak naprawde schodek, ucina energie!
		for i in range(0,len(self.params.E)):
			if self.params.E[i] <= (self.params.Eg+self.params.En[0]):
				self.params.Epocz[i]=0.0
			else:
				self.params.Epocz[i]=1.0
	def widmo_fd(self):
		self.Widmo_fd = self.Pik * self.DOS * \
			distribution_FD(self.params.E, self.params.Ef, self.params.T)
	
	def widmo_boltzmann(self):
		self.Widmo_b = self.Pik * self.DOS * \
			distribution_Boltzmann(0.0, self.params.E, self.params.T)

	def widmo_planck(self):
		#Widmo PL QW ale obliczone sposobem jak dla Bulku (3D) - 
		#absorpcja jedynie zmieniona na dwuwymiarowa! Przypadek rownowagi termodynamicznej!
		self.Widmo5 = (1.0 / self.params.E) * self.DOS * \
		distribution_Planck(self.params.E, self.params.T) * self.params.E 

	def prawdopodobienstwo(self):
		for j in range(0, len(self.params.En)):
			for i in range(0, len(self.params.E)):
			 self.params.Prawd[i] = self.params.Prawd[i] + \
			 Calka( self.params.E, pik_Gaussowski(self.params.E, \
			 	self.params.E[i], self.params.gamma) * self.DOS * \
				distribution_Boltzmann(0.0, self.params.E, self.params.T) )
			 
	def generate(self, items):
		for i in range(items):
			yield i
	
	def widmo(self):
		self.params.Widmo = self.params.Prawd * self.params.E
	
	def save_to_files(self):
		plik = open('widmo1', 'w')
		plik2 = open('lambda', 'w')
		
		for i in self.generate(len(self.params.Widmo)):
		    plik.write(str(self.params.LAMBDA[i]) + ' ' \
		               + str(self.params.Widmo[i]/max(self.params.Widmo)) \
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
		plt.plot(self.params.E, self.DOS/max(self.DOS), 'r', self.params.E, \
			 self.DOS2/max(self.DOS2), 'b', self.params.E, \
			 self.Hevisajd/max(self.Hevisajd), 'g', lw=2)

		plt.savefig("plot_alfa.png")
		plt.show()
	
	def plot_widmo_beta(self):
		self.count = len(open('LAMBDA_Zmierzona.txt', 'rU').readlines())
		self.zmierzone_x = open('LAMBDA_Zmierzona.txt', 'rU').readlines()
		self.zmierzone_y = open('Zmierzone1.txt', 'rU').readlines()

		for i in range(0, self.count):
		    self.zmierzone_x[i] = float(self.zmierzone_x[i].strip())
		    self.zmierzone_y[i] = float(self.zmierzone_y[i].strip())
		
		plt.plot(self.params.LAMBDA, self.Widmo5/max(self.Widmo5), 'r', \
			 self.params.LAMBDA, self.params.Widmo/max(self.params.Widmo), \
			 'b', self.zmierzone_x, self.zmierzone_y, 'k.', lw=2)

		plt.savefig("plot_beta.png")
		plt.show()
		

if __name__ == "__main__":

	gui = GUI()
	gui.main()
