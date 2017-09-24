#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from common import *
from gui import *
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository.Gtk import Image

__author__ = "Piotr Ruszala"
__version__ = "0.1"

class Spectrum_generator:

    def __init__(self, file_with_measured_data = None):
        self.DOS = 0
        self.DOS2 = 0
        self.JDOS = 0
        self.JDOS2 = 0
        self.Abs1 = 0
        self.Abs2 = 0
        self.Abs3 = 0
        self.dosCB = 0
        self.dosVB = 0
        self.dosLH = 0
        self.dosHH = 0
        self.dosHH_probability = 0
        self.Hevisajd = 0
        self.Pik = 0
        self.Normal = 0
        self.Pik_mieszany = 0
        self.Delty = 0
        self.OGS = 0
        self.u_rehh = 0
        self.u_relh = 0

        self.params = Parameters()
        self.params.update()
        self.f_measured_data = file_with_measured_data

    def delta_cal(self):
        self.u_rehh = (self.params.me * self.params.mehh) \
                    / (self.params.me + self.params.mehh)
        self.u_relh = (self.params.me * self.params.melh) \
                    / (self.params.me + self.params.melh)

        self.masy_r = np.zeros(len(self.params.En))

        for i in range(0, len(self.params.CB)):
			self.dosCB = self.dosCB + self.params.g0 \
				* self.params.me \
				* (Schodek(self.params.Ec - self.params.CB[i]))

        for i in range(0, len(self.params.HH)):
            self.dosHH = self.dosHH - self.params.g0 \
                 * self.params.mehh \
                 * (Schodek(self.params.Ev - self.params.HH[i]))

            self.dosHH_probability = self.dosHH_probability \
                 - self.params.g0 * self.params.mehh \
                 * (Schodek(self.params.Ev - self.params.HH[i]))

        for i in range(0, len(self.params.LH)):
            self.dosLH = self.dosLH - self.params.g0 * self.params.melh \
                 * (Schodek(self.params.Ev - self.params.LH[i]))

        for i in range(0, len(self.params.En)):
            if (self.params.wsk[i]=='h' or self.params.wsk[i]=='H'):
                self.masy_r[i]=self.u_rehh
            elif (self.params.wsk[i]=='l' or self.params.wsk[i]=='L'):
                self.masy_r[i]=self.u_relh

        for i in range(0, len(self.params.En)):
            self.DOS = self.DOS + self.params.g0 * self.params.CP[i] * \
                (DOS_rozmyty_erf(self.params.E, \
                 self.params.En[i], self.params.step_func_gamma) )

            self.DOS2 = self.DOS2 + self.params.g0 * self.params.CP[i] * \
                ( DOS_rozmyty_cauchy(self.params.E, \
                 self.params.En[i], self.params.step_func_gamma) )

            self.Hevisajd = self.Hevisajd + self.params.g0 * \
                self.masy_r[i] * \
                Schodek(self.params.E - self.params.En[i]) # Hevisajd to jest idealny JDOS!

            self.Pik = self.Pik + self.params.A0 * \
                ( pik_Lorentza(self.params.E, \
                 self.params.En[i], self.params.gamma) )

            self.Normal = self.Normal + self.params.A0 * \
                pik_Gaussowski(self.params.E, \
                self.params.En[i], self.params.gamma)

            self.Pik_mieszany = self.Pik_mieszany + self.params.A0 * \
                ( pik_Lorentza(self.params.E, \
                  self.params.En[i], self.params.gamma) + \
                  pik_Gaussowski(self.params.E, \
                  self.params.En[i], self.params.gamma) )

            self.Delty = self.Delty + \
                self.params.A0 * \
                Delta(self.params.E - self.params.En[i])

            self.dosVB = self.dosHH + self.dosLH

            self.JDOS = self.JDOS + self.params.g0 * self.masy_r[i] * \
                (DOS_rozmyty_erf(self.params.E, self.params.En[i], \
                                 self.params.step_func_gamma))

            self.JDOS2 = self.JDOS2 + self.params.g0 * self.masy_r[i] * \
                (DOS_rozmyty_cauchy(self.params.E, self.params.En[i], \
                                    self.params.step_func_gamma))

            self.Abs1 = self.Abs1 + self.params.g0 * self.params.CP[i] * self.masy_r[i] * \
                (DOS_rozmyty_erf(self.params.E, self.params.En[i], \
                                 self.params.step_func_gamma))

            self.Abs2 = self.Abs2 + self.params.g0 * self.params.CP[i] * self.masy_r[i] * \
                (DOS_rozmyty_cauchy(self.params.E, self.params.En[i], \
                                 self.params.step_func_gamma))

            self.Abs3 = self.Abs3 + self.params.g0 * self.params.CP[i] * self.masy_r[i] * \
                Schodek(self.params.E - self.params.En[i])

    def widmo_fd(self):
        self.Widmo_fd = self.Pik * self.DOS * \
            distribution_FD(self.params.E, self.params.Ef, self.params.T)

    def widmo_boltzmann(self):
        self.Widmo_b = self.Pik * self.DOS * \
            distribution_Boltzmann(0.0, self.params.E, self.params.T)

    def widmo_planck(self):
        self.Widmo1 = (1.0 / self.params.E) * self.Abs1 * \
        distribution_Planck(self.params.E, self.params.T) * self.params.E

    def prawdopodobienstwo(self):
        self.Prawd = np.zeros(len(self.params.E))
        for i in range(0, len(self.params.E)):
             self.Prawd[i] = Calka( self.params.E, pik_Gaussowski(self.params.E, \
                             self.params.E[i], self.params.gamma) * self.Abs1 * \
                             distribution_Boltzmann(0.0, self.params.E, self.params.T) )

    def generate(self, items):
        for i in range(items):
            yield i

    def widmo(self):
        self.Widmo2 = self.Prawd * self.params.E

    def save_to_files(self, plik, plik2):
        self.plik = open(plik, 'w')
        self.plik2 = open(plik2, 'w')

        for i in self.generate(len(self.Widmo2)):
            self.plik.write(str(self.params.LAMBDA[i]) + ' ' \
                       + str(self.Widmo2[i]/max(self.Widmo2)) \
                       + '\n')

        for i in self.generate(len(self.params.LAMBDA)):
            self.plik2.write(str(self.params.LAMBDA[i]) + '\n')

        self.plik2.close()
        self.plik.close()

    def calculate_all(self):
        self.delta_cal()
        #self.energia_pocz()
        self.widmo_fd()
        self.widmo_boltzmann()
        self.widmo_planck()
        self.prawdopodobienstwo()
        self.widmo()

    def plot_widmo_absorption(self):
        plt.ylabel('A [j. w.]')
        plt.xlabel('Energy [eV]')
        one = plt.plot(self.params.E, self.Abs1/max(self.Abs1), 'r', lw=2, label="one")
        two = plt.plot(self.params.E, self.Abs2/max(self.Abs2), 'b', lw=2, label="two")
        three = plt.plot(self.params.E, self.Abs3/max(self.Abs3), 'k', lw=2, label="three")

        self.linex = one[0].get_data()
        self.liney = two[0].get_data()
        self.linez = three[0].get_data()

        plt.savefig("plot_absorption_tmp.png", dpi=80)
        self.pb = Pixbuf.new_from_file("plot_absorption_tmp.png")
        self.generated_absorption = Image.new_from_file("plot_absorption_tmp.png")
        plt.savefig("plot_absorption_tmp.png", dpi=200)
        plt.close()

    def plot_widmo_pl_um(self):
        print("File with measured data name: " + str(self.f_measured_data))
        if (self.f_measured_data != None):
            self.x, self.y = np.loadtxt(self.f_measured_data, delimiter=' ', \
                                        usecols=(0,1), unpack=True)
            print(self.x)
            print(self.y)
            print(self.Widmo2)
            print("X and Y updated!")

            data_plt = plt.plot(self.params.LAMBDA, self.Widmo1/max(self.Widmo1), 'r', \
                 self.params.LAMBDA, self.Widmo2/max(self.Widmo2), \
                 'b', self.x, self.y, 'k.', lw=2)
            self.linex = data_plt[0].get_data()
            self.liney = data_plt[1].get_data()
            self.linez = data_plt[2].get_data()
        else:
            print("X/Y NOT updated!")
            data_plt = plt.plot(self.params.LAMBDA, self.Widmo1/max(self.Widmo1), 'r', \
                 self.params.LAMBDA, self.Widmo2/max(self.Widmo2), \
                 'b', lw=2)
            self.linex = data_plt[0].get_data()
            self.liney = data_plt[1].get_data()

        plt.ylabel('PL [j. w.]')
        plt.xlabel('lambda [um]')
        plt.savefig("plot_pl_um_tmp.png", dpi=80)
        self.pb = Pixbuf.new_from_file("plot_pl_um_tmp.png")
        self.generated_pl_um = Image.new_from_file("plot_pl_um_tmp.png")
        plt.savefig("plot_pl_um_tmp.png", dpi=200)
        plt.close()

    def plot_widmo_pl_ev(self):
        print("File with measured data name: " + str(self.f_measured_data))
        if (self.f_measured_data != None):
            self.x, self.y = np.loadtxt(self.f_measured_data, delimiter=' ', \
                                        usecols=(0,1), unpack=True)
            print(self.x)
            print(self.y)
            print(self.Widmo2)
            print("X and Y updated!")

            data_plt = plt.plot(self.params.E, self.Widmo1/max(self.Widmo1), 'r', \
                 self.params.E, self.Widmo2/max(self.Widmo2), \
                 'b', self.x, self.y, 'k.', lw=2)
            self.linex = data_plt[0].get_data()
            self.liney = data_plt[1].get_data()
            self.linez = data_plt[2].get_data()
        else:
            print("X/Y NOT updated!")
            data_plt = plt.plot(self.params.E, self.Widmo1/max(self.Widmo1), 'r', \
                 self.params.E, self.Widmo2/max(self.Widmo2), \
                 'b', lw=2)
            self.linex = data_plt[0].get_data()
            self.liney = data_plt[1].get_data()

        plt.ylabel('PL [j. w.]')
        plt.xlabel('lambda [eV]')
        plt.savefig("plot_pl_ev_tmp.png", dpi=80)
        self.pb = Pixbuf.new_from_file("plot_pl_ev_tmp.png")
        self.generated_pl_ev = Image.new_from_file("plot_pl_ev_tmp.png")
        plt.savefig("plot_pl_ev_tmp.png", dpi=200)
        plt.close()

    def plot_widmo_cbdos(self):
        plt.ylabel('CB DOS [j. w.]')
        plt.xlabel('Energy [eV]')
        data_plt_cb = plt.plot(self.params.Ec, self.dosCB, 'k', lw=2)

        self.linex = data_plt_cb[0].get_data()

        plt.savefig("plot_cbdos_tmp.png", dpi=80)
        self.pb = Pixbuf.new_from_file("plot_cbdos_tmp.png")
        self.generated_cbdos = Image.new_from_file("plot_cbdos_tmp.png")
        plt.savefig("plot_cbdos_tmp.png", dpi=200)
        plt.close()

    def plot_widmo_hh_lh_dos(self):
        plt.ylabel('HH and LH DOS [j. w.]')
        plt.xlabel('Energy [eV]')
        data_plt_vb = plt.plot(self.params.Ev, self.dosHH        \
                    + abs(min(self.dosHH)), 'r', self.params.Ev, \
		    self.dosLH + abs(min(self.dosLH)), 'b', lw=2)

        self.linex = data_plt_vb[0].get_data()

        plt.savefig("plot_hh_lh_dos_tmp.png", dpi=80)
        self.pb = Pixbuf.new_from_file("plot_hh_lh_dos_tmp.png")
        self.generated_hh_lh_dos = Image.new_from_file("plot_hh_lh_dos_tmp.png")
        plt.savefig("plot_hh_lh_dos_tmp.png", dpi=200)
        plt.close()

    def plot_widmo_vbdos(self):
        plt.ylabel('VB DOS [j. w.]')
        plt.xlabel('Energy [eV]')
        data_plt_vb = plt.plot(self.params.Ev, self.dosVB + abs(min(self.dosVB)), 'k', lw=2)

        self.linex = data_plt_vb[0].get_data()

        plt.savefig("plot_vbdos_tmp.png", dpi=80)
        self.pb = Pixbuf.new_from_file("plot_vbdos_tmp.png")
        self.generated_vbdos = Image.new_from_file("plot_vbdos_tmp.png")
        plt.savefig("plot_vbdos_tmp.png", dpi=200)
        plt.close()

    def plot_widmo_jdos(self):
        plt.ylabel('JDOS [j. w.]')
        plt.xlabel('Energy [eV]')
        data_plt_j = plt.plot(self.params.E, self.JDOS/max(self.JDOS), 'r', \
                       self.params.E, self.JDOS2/max(self.JDOS2), 'b', \
                       self.params.E, self.Hevisajd/max(self.Hevisajd), 'k', lw=2)

        self.linex = data_plt_j[0].get_data()
        self.liney = data_plt_j[1].get_data()
        self.linez = data_plt_j[2].get_data()

        plt.savefig("plot_jdos_tmp.png", dpi=80)
        self.pb = Pixbuf.new_from_file("plot_jdos_tmp.png")
        self.generated_jdos = Image.new_from_file("plot_jdos_tmp.png")
        plt.savefig("plot_jdos_tmp.png", dpi=200)
        plt.close()

if __name__ == "__main__":

    gui = GUI()
    gui.main()
