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
		self.Eg = 1.1828
		self.T = 300
		self.gamma = 0.001
		self.gamma2 = 1.0
		self.gamma_schodek=35.0
		self.gamma_schodek2=5.0
		self.Ef = 0.5 * self.Eg
		self.E = np.arange(1.08,1.35,0.001)
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
		
#Pochodna=diff(E, DOS, 1)

#for i in range(0, len(E)):
	#Widmo[i]=Calka(E, Widmo1, i)

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
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    
        # When the window is given the "delete_event" signal (this is given
        # by the window manager, usually by the "close" option, or on the
        # titlebar), we ask it to call the delete_event () function
        # as defined above. The data passed to the callback
        # function is NULL and is ignored in the callback function.
        self.window.connect("delete_event", self.delete_event)
    
        # Here we connect the "destroy" event to a signal handler.  
        # This event occurs when we call gtk_widget_destroy() on the window,
        # or if we return FALSE in the "delete_event" callback.
        self.window.connect("destroy", self.destroy)
    
        # Sets the border width of the window.
        self.window.set_border_width(30)
    
        # Creates a new button with the label "Hello World".
        self.button = gtk.Button("Generate graph!")
    
        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.
        self.button.connect("clicked", self.generate_graph, None)
    
        # This will cause the window to be destroyed by calling
        # gtk_widget_destroy(window) when "clicked".  Again, the destroy
        # signal could come from here, or the window manager.
        #self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
    
        # This packs the button into the window (a GTK container).
        self.window.add(self.button)
    
        # The final step is to display this newly created widget.
        self.button.show()
    
        # and the window
        self.window.show()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

if __name__ == "__main__":
	
	gui = GUI()
	gui.main()
        
	#count=len(open('LAMBDA_Zmierzona.txt', 'rU').readlines())
	#zmierzone_x = open('LAMBDA_Zmierzona.txt', 'rU').readlines()
	#zmierzone_y = open('Zmierzone1.txt', 'rU').readlines()

	#for i in range(0,count):
	#    zmierzone_x[i]=float(zmierzone_x[i].strip())
	#    zmierzone_y[i]=float(zmierzone_y[i].strip())
	##Wiersz=[]
	##for i in range(0, 4):
	#    #Wiersz[i] = linecache.getline('Zmierzone1.txt', i)
	##Zmierzone = open('Zmierzone1.txt').read()
	##print len(Zmierzone), Zmierzone[43]
	##print zmierzone_x

	#BLAD=0.0

	#print len(c.LAMBDA), len(zmierzone_x)
	#print "Blad wynosi: "
	#print "kT wynosi (w [meV]): ", k*T*1000.0

	##plt.xlim(E[0],E[len(E)-1])
	##plt.xlim(LAMBDA[len(LAMBDA)-1],LAMBDA[0])

	##plt.plot(E, DOS, 'r', E, DOS2, 'b', E, Hevisajd, 'g', lw=2)
	##plt.plot(E, Pik, 'r', E, Normal, 'b', E, Delty, 'g', lw=2)
	##plt.plot(E, Widmo2/max(Widmo2), 'r', E, Widmo5/max(Widmo5), 'b', lw=2)

	##plt.plot(LAMBDA, Widmo/max(Widmo), 'r', LAMBDA, Widmo5/max(Widmo5), 'b', lw=2)

	##-------- DOBRE WIDMA:--------------------------------------------------------------------------------------------
	##plt.plot(c.LAMBDA, c.Widmo5/max(c.Widmo5), 'r', c.LAMBDA, c.Widmo/max(c.Widmo), 'b', zmierzone_x, zmierzone_y, 'k.', lw=2)
	#plt.plot(c.E, c.DOS/max(c.DOS), 'r', c.E, c.DOS2/max(c.DOS2), 'b', c.E, c.Hevisajd/max(c.Hevisajd), 'g', lw=2)
	##-----------------------------------------------------------------------------------------------------------------

	##plt.plot(LAMBDA, Widmo/max(Widmo), 'r', LAMBDA, Delta(LAMBDA-1.24/(Eg+En[2])), 'b', lw=2)
	##plt.plot(zmierzone_x[::-1], zmierzone_y, 'r', lw=2)

	##f, axarr = plt.subplots(2, sharex=True)
	##axarr[0].plot(LAMBDA, Widmo5/max(Widmo5), 'r', zmierzone_x, zmierzone_y, 'b', lw=2)
	##axarr[0].set_title('Sharing X axis')
	##if len(LAMBDA) < len(zmierzone_x):
	#    #axarr[1].plot(LAMBDA, BLAD, 'ro', lw=2)
	##else:
	#    #axarr[1].plot(zmierzone_x, BLAD, 'ro', lw=2)
	##axarr[1].ylim(-1.0,1.0)

	##plt.plot(c.E, co.Ogon_gestosci_stanow(c.E, c.Eg, 1.0, 100.0), 'r', lw=2)
	##plt.plot(E, Rozklad_Boltzmanna(0.0, E, T), 'r', lw=2)
	##plt.plot(E, DOS, 'r', E, DOS2, 'b', lw=2)
	##plt.plot(E, Hevisajd, 'r', E, Delty, 'b', lw=2)
	##plt.plot(E, Hevisajd*Delty, 'r', lw=2)
	##plt.plot(E, Prawd/max(Prawd), 'r', E, DOS/max(DOS), 'b', lw=2)
	##plt.plot(E, Widmo/max(Widmo), 'r', lw=2)
	##plt.plot(E, Epocz, 'r', lw=2)
	##plt.plot(E, DOS*Hevisajd, 'r', lw=2)
	##plt.plot(E, Pik_Lorentza(E, Eg+En[0], gamma)/max(Pik_Lorentza(E, Eg+En[0], gamma)), 'r', E, Pik_Gaussowski(E, Eg+En[0], gamma)/max(Pik_Gaussowski(E, Eg+En[0], gamma)), 'b', lw=2)

	##line_up, = plt.plot(E, Widmo3/max(Widmo3), 'r', label='Pik normalny, DOS normalny', lw=2)
	##line_down, = plt.plot(E, Widmo4/max(Widmo4), 'b', label='Pik lorentza, DOS lorentza', lw=2)
	##line_up2, = plt.plot(E, Widmo6/max(Widmo6), 'g', label='Pik normalny, DOS lorentza', lw=2)
	##line_down2, = plt.plot(E, Widmo7/max(Widmo7), 'y', label='Pik lorentza, DOS normalny', lw=2)
	##plt.legend([line_up, line_down, line_up2, line_down2], ['Line Up', 'Line Down', 'Line Up2', 'Line Down2'])

	#plt.savefig("pik1.png")
	#plt.show()
