import numpy as np
from scipy.constants import codata
from scipy import special

k = codata.value('Boltzmann constant in eV/K')

class Parameters:	
	def __init__(self):
		self.A0 = 10.0
		self.g0 = 1.0
		self.Eg = 1.1828#
		self.T = 300#
		self.gamma = 0.001#
		self.gamma2 = 1.0#
		self.gamma_schodek=35.0
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

	def read_params_from_UI(self):
		return 0
	
	def update(self):
		return 0

def Schodek(x):
	Y = np.zeros(len(x))
	for i in range(0,len(x)):
		if float(x[i]) < 0.0:
			Y[i] = 0.0
		elif float(x[i]) >= 0.0:
			Y[i] = 1.0
	return Y

def Delta(x):
	Y = np.zeros(len(x))
	for i in range(0,len(x)):
		if x[i] >= -0.0005 and x[i]<=0.0005:
			Y[i] = 1.0
	return Y

def Calka(arg,fun):
	C = 0
	for i in range(0,len(arg)-1):
		C = C + (0.5 * (arg[i+1] - arg[i]) * (fun[i+1] + fun[i]))
	return C

def DOS_rozmyty_erf(Ene, E_prz, W): #Rozmyte schodki - funkcja bledu erf
	return 0.5 * ( special.erf( (Ene - E_prz) * W ) + 1.0 )

def DOS_rozmyty_cauchy(Ene, E_prz, W): #Rozmyte schodki - funkcja dystrybuanty rozkladu Cauchyego
	return ((1.0 / np.pi) * np.arctan((Ene - E_prz) * W) + 0.5)

def Ogon_gestosci_stanow(Ene, E_prz, Amplituda0, w): #Rozmycie krawedzi absorpcji
	Y = 0.0
	if Ene <= E_prz:
		Y = Amplituda0 * (np.exp((Ene - E_prz) * w ))
	elif Ene > E_prz:
		Y = Amplituda0
	return Y

def pik_Gaussowski(Ene, E_prz, w): #Pik Gaussa - rozklad normalny
	return ((1.0 / (w * np.sqrt(2.0 * np.pi))) * np.exp( - (((Ene - E_prz)**2)/(2.0 * w**2))))

def pik_Lorentza(Ene, E_prz, w): #Pik Lorentza - rozklad Cauchyego
	return 1.0 / ((np.pi * w)*(1.0 + ((Ene-  E_prz) / w)**2))

def distribution_Boltzmann(Ek, Ep, T):
	dEne = Ek - Ep
	return np.exp(dEne / (k * T))

def distribution_FD(Ene, EF, T):
	return (1.0/(np.exp((Ene - EF)/(k * T)) + 1.0))

def distribution_Planck(Ene, T):
	return ((Ene**2)/(np.exp((Ene) / (k * T)) - 1.0))
