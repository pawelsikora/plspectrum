import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy as sp
from scipy import signal
import random
random.seed()
import linecache
#from sympy.mpmath import *

def Schodek(x):
	Y=np.zeros(len(x))
	for i in range(0,len(x)):
		if float(x[i]) < 0.0:
			Y[i]=0.0
		elif float(x[i]) >= 0.0:
			Y[i]=1.0
	return Y

def Delta(x):
	Y=np.zeros(len(x))
	for i in range(0,len(x)):
		if x[i]>=-0.0005 and x[i]<=0.0005:
			Y[i]=1.0
	return Y

#--------Funkcja liczaca calke:--------------------------------

def Calka(arg,fun):
	C=0
	for i in range(0,len(arg)-1):
		C=C+(0.5*(arg[i+1]-arg[i])*(fun[i+1]+fun[i]))
	return C

#--------------------------------------------------------------

def DOS_rozmyty_erf(Ene, E_prz, W): #Rozmyte schodki - funkcja bledu erf
	return 0.5*(sp.special.erf((Ene-E_prz)*W)+1.0)

def DOS_rozmyty_cauchy(Ene, E_prz, W): #Rozmyte schodki - funkcja dystrybuanty rozkladu Cauchyego
	return ((1.0/np.pi)*np.arctan((Ene-E_prz)*W)+0.5)

def Ogon_gestosci_stanow(Ene, E_prz, Amplituda0, w): #Rozmycie krawedzi absorpcji
	Y = 0.0
	if Ene<=E_prz:
		Y = Amplituda0*(np.exp((Ene-E_prz)*w))
	elif Ene>E_prz:
		Y = Amplituda0
	return Y

def Pik_Gaussowski(Ene, E_prz, w): #Pik Gaussa - rozklad normalny
	return ((1.0/(w*np.sqrt(2.0*np.pi)))*np.exp(-(((Ene-E_prz)**2)/(2.0*w**2))))

def Pik_Lorentza(Ene, E_prz, w): #Pik Lorentza - rozklad Cauchyego
	return 1.0/((np.pi*w)*(1.0+((Ene-E_prz)/w)**2))

def Rozklad_Boltzmanna(Ek, Ep, T):
	dEne = Ek-Ep
	return np.exp(dEne/(k*T))

def Rozklad_FD(Ene, EF, T):
	return (1.0/(np.exp((Ene-EF)/(k*T))+1.0))

def Rozklad_Plancka(Ene, T):
	return ((Ene**2)/(np.exp((Ene)/(k*T))-1.0))

A0=10.0
g0=1.0
k=8.617*10**(-5)
Eg=1.1828#1.45
T=300.0
gamma=0.001
gamma2=1.0
gamma_schodek=35.0
gamma_schodek2=5.0
Ef=0.5*Eg
E=np.arange(1.08,1.35,0.001)
En=np.array([0.49475+0.69223-Eg,0.54384+0.7062-Eg,0.60827+0.7275-Eg])
CP=np.array([0.98453,0.94166,0.79406])
a=np.zeros(len(E))
g_bulk=np.zeros(len(E))
DOS=np.zeros(len(E))
DOS2=np.zeros(len(E))
Pik=np.zeros(len(E))
Normal=np.zeros(len(E))
Pik_mieszany=np.zeros(len(E))
Hevisajd=np.zeros(len(E))
Delty=np.zeros(len(E))
Epocz=np.zeros(len(E))
Widmo=np.zeros(len(E))
Prawd=np.zeros(len(E))
Energia=0.0
LAMBDA=(1.24/E)
#LAMBDA=LAMBDA[::-1]

for i in range(0, len(En)):
	#Energia=Energia+En[i]
	DOS=DOS+g0*CP[i]*(DOS_rozmyty_erf(E, Eg+En[i], gamma_schodek))
	DOS2=DOS2+g0*CP[i]*(DOS_rozmyty_cauchy(E, Eg+En[i], gamma_schodek))
	Hevisajd=Hevisajd+g0*CP[i]*Schodek(E-Eg-En[i])
	Pik=Pik+A0*(Pik_Lorentza(E, Eg+En[i], gamma))
	Normal=Normal+A0*(Pik_Gaussowski(E, Eg+En[i], gamma))
	Pik_mieszany=Pik_mieszany+A0*(Pik_Lorentza(E, Eg+En[i], gamma) + Pik_Gaussowski(E, Eg+En[i], gamma))
	Delty=Delty+A0*Delta(E-Eg-En[i])

for i in range(0,len(E)):
	if E[i]<=(Eg+En[0]):
		Epocz[i]=0.0
	else:
		Epocz[i]=1.0

Widmo1=Pik*DOS*Rozklad_FD(E, Ef, T)
Widmo2=Pik*DOS*Rozklad_Boltzmanna(0.0, E, T)#*Epocz #Epocz to tak naprawde schodek, ucina energie!

Widmo5=(1.0/E)*DOS*Rozklad_Plancka(E, T)*E #Widmo PL QW ale obliczone sposobem jak dla Bulku (3D) - absorpcja jedynie zmieniona na dwuwymiarowa! Przypadek rownowagi termodynamicznej!

for j in range(0, len(En)):
	for i in range(0, len(E)):
         Prawd[i]=Prawd[i]+Calka(E, Pik_Gaussowski(E, E[i], gamma)*DOS*Rozklad_Boltzmanna(0.0, E, T))#*Ogon_gestosci_stanow(E[i], Eg, 0.001, 50.0))
         #Prawd[i]=Prawd[i]+Calka(E, Pik_Lorentza(E, E[i], gamma)*DOS*Rozklad_Boltzmanna(0.0, E, T)*Ogon_gestosci_stanow(E[i], Eg-En[0], gamma2, gamma_schodek2))

        #Prawd[i]=Prawd[i]+Calka(E, Delta(E-E[i])*Schodek(E-(Eg+En[j])))

print len(En), En
print len(E), En+Eg

Widmo=Prawd*E

#Pochodna=diff(E, DOS, 1)

#for i in range(0, len(E)):
	#Widmo[i]=Calka(E, Widmo1, i)

plik = open('widmo1', 'w')
for i in range(0,len(Widmo)):
    plik.write(str(LAMBDA[i]))
    plik.write(' ')
    plik.write(str(Widmo[i]/max(Widmo)))
    plik.write('\n')
plik.close()

plik2 = open('lambda', 'w')
for i in range(0,len(LAMBDA)):
    plik2.write(str(LAMBDA[i]))
    plik2.write('\n')
plik2.close()

count=len(open('LAMBDA_Zmierzona.txt', 'rU').readlines())
zmierzone_x = open('LAMBDA_Zmierzona.txt', 'rU').readlines()
zmierzone_y = open('Zmierzone1.txt', 'rU').readlines()

for i in range(0,count):
    zmierzone_x[i]=float(zmierzone_x[i].strip())
    zmierzone_y[i]=float(zmierzone_y[i].strip())
#Wiersz=[]
#for i in range(0, 4):
    #Wiersz[i] = linecache.getline('Zmierzone1.txt', i)
#Zmierzone = open('Zmierzone1.txt').read()
#print len(Zmierzone), Zmierzone[43]
#print zmierzone_x

BLAD=0.0

print len(LAMBDA), len(zmierzone_x)
print "Blad wynosi: "
print "kT wynosi (w [meV]): ", k*T*1000.0

#plt.xlim(E[0],E[len(E)-1])
#plt.xlim(LAMBDA[len(LAMBDA)-1],LAMBDA[0])

#plt.plot(E, DOS, 'r', E, DOS2, 'b', E, Hevisajd, 'g', lw=2)
#plt.plot(E, Pik, 'r', E, Normal, 'b', E, Delty, 'g', lw=2)
#plt.plot(E, Widmo2/max(Widmo2), 'r', E, Widmo5/max(Widmo5), 'b', lw=2)

#plt.plot(LAMBDA, Widmo/max(Widmo), 'r', LAMBDA, Widmo5/max(Widmo5), 'b', lw=2)

#-------- DOBRE WIDMA:--------------------------------------------------------------------------------------------
plt.plot(LAMBDA, Widmo5/max(Widmo5), 'r', LAMBDA, Widmo/max(Widmo), 'b', zmierzone_x, zmierzone_y, 'k.', lw=2)
#plt.plot(E, DOS/max(DOS), 'r', E, DOS2/max(DOS2), 'b', E, Hevisajd/max(Hevisajd), 'g', lw=2)
#-----------------------------------------------------------------------------------------------------------------

#plt.plot(LAMBDA, Widmo/max(Widmo), 'r', LAMBDA, Delta(LAMBDA-1.24/(Eg+En[2])), 'b', lw=2)
#plt.plot(zmierzone_x[::-1], zmierzone_y, 'r', lw=2)

#f, axarr = plt.subplots(2, sharex=True)
#axarr[0].plot(LAMBDA, Widmo5/max(Widmo5), 'r', zmierzone_x, zmierzone_y, 'b', lw=2)
#axarr[0].set_title('Sharing X axis')
#if len(LAMBDA) < len(zmierzone_x):
    #axarr[1].plot(LAMBDA, BLAD, 'ro', lw=2)
#else:
    #axarr[1].plot(zmierzone_x, BLAD, 'ro', lw=2)
#axarr[1].ylim(-1.0,1.0)

#plt.plot(E, Ogon_gestosci_stanow(E, Eg, 1.0, 100.0), 'r', lw=2)
#plt.plot(E, Rozklad_Boltzmanna(0.0, E, T), 'r', lw=2)
#plt.plot(E, DOS, 'r', E, DOS2, 'b', lw=2)
#plt.plot(E, Hevisajd, 'r', E, Delty, 'b', lw=2)
#plt.plot(E, Hevisajd*Delty, 'r', lw=2)
#plt.plot(E, Prawd/max(Prawd), 'r', E, DOS/max(DOS), 'b', lw=2)
#plt.plot(E, Widmo/max(Widmo), 'r', lw=2)
#plt.plot(E, Epocz, 'r', lw=2)
#plt.plot(E, DOS*Hevisajd, 'r', lw=2)
#plt.plot(E, Pik_Lorentza(E, Eg+En[0], gamma)/max(Pik_Lorentza(E, Eg+En[0], gamma)), 'r', E, Pik_Gaussowski(E, Eg+En[0], gamma)/max(Pik_Gaussowski(E, Eg+En[0], gamma)), 'b', lw=2)

#line_up, = plt.plot(E, Widmo3/max(Widmo3), 'r', label='Pik normalny, DOS normalny', lw=2)
#line_down, = plt.plot(E, Widmo4/max(Widmo4), 'b', label='Pik lorentza, DOS lorentza', lw=2)
#line_up2, = plt.plot(E, Widmo6/max(Widmo6), 'g', label='Pik normalny, DOS lorentza', lw=2)
#line_down2, = plt.plot(E, Widmo7/max(Widmo7), 'y', label='Pik lorentza, DOS normalny', lw=2)
#plt.legend([line_up, line_down, line_up2, line_down2], ['Line Up', 'Line Down', 'Line Up2', 'Line Down2'])

plt.savefig("pik1.png")
plt.show()