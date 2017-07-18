#!/usr/bin/env python

from common import *
from gui import *
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pickle
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import FontProperties
from gi.repository.GdkPixbuf import Pixbuf

__author__ = "Piotr Ruszala"
__version__ = "0.1"


class Spectrum_generator:

    def __init__(self, file_with_measured_data="None"):
        self.DOS = 0
        self.DOS2 = 0
        self.JDOS = 0
        self.JDOS2 = 0
        self.dosC = 0
        self.dosV = 0
        self.Hevisajd = 0
        self.Pik = 0
        self.Normal = 0
        self.Pik_mieszany = 0
        self.Delty= 0
        self.params = Parameters()
        self.params.update()
        self.f_measured_data = file_with_measured_data

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

            self.dosC = self.dosC + self.params.g0 * self.params.me * \
                (Schodek(self.params.Ec - self.params.CB[i]))

            self.dosV = self.dosV + self.params.g0 * self.params.mehh * \
                (Schodek(self.params.Ev - self.params.VB[i]))

            self.JDOS = self.JDOS + self.params.g0 * \
                (DOS_rozmyty_erf(self.params.E, self.params.Eg + self.params.En[i], \
                                 self.params.gamma_schodek))

            self.JDOS2 = self.JDOS2 + self.params.g0 * \
                (DOS_rozmyty_cauchy(self.params.E, self.params.Eg + self.params.En[i], \
                                    self.params.gamma_schodek))

    def energia_pocz(self):
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
        self.Widmo5 = (1.0 / self.params.E) * self.DOS * \
        distribution_Planck(self.params.E, self.params.T) * self.params.E

    def prawdopodobienstwo(self):
        self.Prawd = np.zeros(len(self.params.E))
        for j in range(0, len(self.params.En)):
            for i in range(0, len(self.params.E)):
             self.Prawd[i] = self.Prawd[i] + \
             Calka( self.params.E, pik_Gaussowski(self.params.E, \
                 self.params.E[i], self.params.gamma) * self.DOS * \
                distribution_Boltzmann(0.0, self.params.E, self.params.T) )

    def generate(self, items):
        for i in range(items):
            yield i

    def widmo(self):
        self.Widmo = self.Prawd * self.params.E

    def save_to_files(self, plik, plik2):
        self.plik = open(plik, 'w')
        self.plik2 = open(plik2, 'w')

        for i in self.generate(len(self.Widmo)):
            self.plik.write(str(self.params.LAMBDA[i]) + ' ' \
                       + str(self.Widmo[i]/max(self.Widmo)) \
                       + '\n')

        for i in self.generate(len(self.params.LAMBDA)):
            self.plik2.write(str(self.params.LAMBDA[i]) + '\n')

        self.plik2.close()
        self.plik.close()

    def calculate_all(self):
        self.delta_cal()
        self.energia_pocz()
        self.widmo_fd()
        self.widmo_boltzmann()
        self.widmo_planck()
        self.prawdopodobienstwo()
        self.widmo()

    def plot_widmo_alfa(self):
        one = plt.plot(self.params.E, self.DOS/max(self.DOS), 'r', label="one")
        two = plt.plot(self.params.E, self.DOS2/max(self.DOS2), 'b', label="two")
        three = plt.plot(self.params.E, self.Hevisajd/max(self.Hevisajd), 'g', lw=2, label="three")

        self.linex = one[0].get_data()
        self.liney = two[0].get_data()
        self.linez = three[0].get_data()

        plt.savefig("plot_alfa_tmp.png")
        self.pb = Pixbuf.new_from_file("plot_alfa_tmp.png")
        self.generated_alfa = gtk.Image.new_from_file("plot_alfa_tmp.png")
        plt.close()

    def plot_widmo_beta(self):
        print("File with measured data name: " + self.f_measured_data)
        if (self.f_measured_data != "None"):
            self.x, self.y = np.loadtxt(self.f_measured_data, delimiter=' ', \
                                        usecols=(0,1), unpack=True)
            print(self.x)
            print(self.y)
            print(self.Widmo)
            print("X and Y updated!")
            data_plt = plt.plot(self.params.LAMBDA, self.Widmo5/max(self.Widmo5), 'r', \
                 self.params.LAMBDA, self.Widmo/max(self.Widmo), \
                 'b', self.x, self.y, 'k.', lw=2)
            self.linex = data_plt[0].get_data()
            self.liney = data_plt[1].get_data()
            self.linez = data_plt[2].get_data()
        else:
            print("X/Y NOT updated!")
            data_plt = plt.plot(self.params.LAMBDA, self.Widmo5/max(self.Widmo5), 'r', \
                 self.params.LAMBDA, self.Widmo/max(self.Widmo), \
                 'b', lw=2)    
            self.linex = data_plt[0].get_data()
            self.liney = data_plt[1].get_data()
        
        plt.savefig("plot_beta_tmp.png")
        self.pb = Pixbuf.new_from_file("plot_beta_tmp.png")
        self.generated_beta = gtk.Image.new_from_file("plot_beta_tmp.png")
        plt.close()

    def plot_widmo_cbdos(self):
        one = plt.plot(self.params.Ec, self.dosC, 'k', lw=2)

        self.linex = one[0].get_data()
        self.liney = one[0].get_data()

        plt.savefig("plot_cbdos_tmp.png")
        self.pb = Pixbuf.new_from_file("plot_cbdos_tmp.png")
        self.generated_cbdos = gtk.Image.new_from_file("plot_cbdos_tmp.png")
        plt.close()

    def plot_widmo_vbdos(self):
        one = plt.plot(self.params.Ev, self.dosV[::-1], 'g', lw=2)

        self.linex = one[0].get_data()
        self.liney = one[0].get_data()

        plt.savefig("plot_vbdos_tmp.png")
        self.pb = Pixbuf.new_from_file("plot_vbdos_tmp.png")
        self.generated_vbdos = gtk.Image.new_from_file("plot_vbdos_tmp.png")
        plt.close()

    def plot_widmo_jdos(self):
        one = plt.plot(self.params.E, self.JDOS/max(self.JDOS), 'r', \
                       self.params.E, self.JDOS2/max(self.JDOS2), 'b', \
                       self.params.E, self.Hevisajd/max(self.Hevisajd), lw=2)

        self.linex = one[0].get_data()
        self.liney = one[0].get_data()

        plt.savefig("plot_jdos_tmp.png")
        self.pb = Pixbuf.new_from_file("plot_jdos_tmp.png")
        self.generated_jdos = gtk.Image.new_from_file("plot_jdos_tmp.png")
        plt.close()

if __name__ == "__main__":

    gui = GUI()
    gui.main()
