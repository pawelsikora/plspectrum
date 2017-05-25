import scipy as sp
import numpy as np

k = 8.617*10**(-5)
T = 300.0

def Schodek( x):
	Y = np.zeros(len(x))
	for i in range(0,len(x)):
		if float(x[i]) < 0.0:
			Y[i] = 0.0
		elif float(x[i]) >= 0.0:
			Y[i] = 1.0
	return Y

def Delta( x):
	Y = np.zeros(len(x))
	for i in range(0,len(x)):
		if x[i] >= -0.0005 and x[i]<=0.0005:
			Y[i] = 1.0
	return Y

def Calka( arg,fun):
	C = 0
	for i in range(0,len(arg)-1):
		C = C + (0.5 * (arg[i+1] - arg[i]) * (fun[i+1] + fun[i]))
	return C

def DOS_rozmyty_erf( Ene, E_prz, W): #Rozmyte schodki - funkcja bledu erf
	return 0.5 * (sp.special.erf((Ene-E_prz)*W)+1.0)

def DOS_rozmyty_cauchy( Ene, E_prz, W): #Rozmyte schodki - funkcja dystrybuanty rozkladu Cauchyego
	return ((1.0 / np.pi) * np.arctan((Ene - E_prz) * W) + 0.5)

def Ogon_gestosci_stanow( Ene, E_prz, Amplituda0, w): #Rozmycie krawedzi absorpcji
	Y = 0.0
	if Ene <= E_prz:
		Y = Amplituda0 * (np.exp((Ene - E_prz) * w ))
	elif Ene > E_prz:
		Y = Amplituda0
	return Y

def pik_Gaussowski( Ene, E_prz, w): #Pik Gaussa - rozklad normalny
	return ((1.0 / (w * np.sqrt(2.0 * np.pi))) * np.exp( - (((Ene - E_prz)**2)/(2.0 * w**2))))

def pik_Lorentza( Ene, E_prz, w): #Pik Lorentza - rozklad Cauchyego
	return 1.0 / ((np.pi * w)*(1.0 + ((Ene-  E_prz) / w)**2))

def distribution_Boltzmann( Ek, Ep, T, k):
	dEne = Ek - Ep
	return np.exp(dEne / (k * T))

def distribution_FD( Ene, EF, T, k):
	return (1.0/(np.exp((Ene - EF)/(k * T)) + 1.0))

def distribution_Planck( Ene, T, k):
	return ((Ene**2)/(np.exp((Ene) / (k * T)) - 1.0))
