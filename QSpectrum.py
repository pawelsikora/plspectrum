#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from common import *
from gui import *
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository.Gtk import Image
from helpers import *

__author__ = "Pawel Sikora, Piotr Ruszala"
__version__ = "0.1"


class Spectrum_generator:
    def __init__(self, file_with_measured_data=None):
        self.f_measured_data = file_with_measured_data
        self.calculator = Calculator()

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

    def plot_widmo_absorption(self, E, Abs1, Abs2, Abs3):
        plt.ylabel('A [j. w.]')
        plt.xlabel('Energy [eV]')
        one = plt.plot(E, Abs1 / max(Abs1), 'r', lw=2, label="one")
        two = plt.plot(E, Abs2 / max(Abs2), 'b', lw=2, label="two")
        three = plt.plot(E, Abs3 / max(Abs3), 'k', lw=2, label="three")

        self.linex = one[0].get_data()
        self.liney = two[0].get_data()
        self.linez = three[0].get_data()

        plt.savefig("plot_absorption_tmp.png", dpi=80)
        self.pb = Pixbuf.new_from_file("plot_absorption_tmp.png")
        self.generated_absorption = Image.new_from_file(
            "plot_absorption_tmp.png")
        plt.savefig("plot_absorption_tmp.png", dpi=200)
        plt.close()

    def plot_widmo_pl_um(self, Widmo1, Widmo2, LAMBDA):
        print("File with measured data name: " + str(self.f_measured_data))
        if (self.f_measured_data != None):
            self.x, self.y = np.loadtxt(self.f_measured_data, delimiter=' ', \
                                        usecols=(0,1), unpack=True)
            print(self.x)
            print(self.y)
            print(self.Widmo2)
            print("X and Y updated!")

            data_plt = plt.plot(LAMBDA, Widmo1/max(Widmo1), 'r', \
                 LAMBDA, Widmo2/max(Widmo2), \
                 'b', self.x, self.y, 'k.', lw=2)
            self.linex = data_plt[0].get_data()
            self.liney = data_plt[1].get_data()
            self.linez = data_plt[2].get_data()
        else:
            print("X/Y NOT updated!")
            data_plt = plt.plot(LAMBDA, Widmo1/max(Widmo1), 'r', \
                 LAMBDA, self.Widmo2/max(Widmo2), \
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

    def plot_widmo_pl_ev(self, Widmo1, Widmo2, E):
        print("File with measured data name: " + str(self.f_measured_data))
        if (self.f_measured_data != None):
            self.x, self.y = np.loadtxt(self.f_measured_data, delimiter=' ', \
                                        usecols=(0,1), unpack=True)
            print(self.x)
            print(self.y)
            print(self.Widmo2)
            print("X and Y updated!")

            data_plt = plt.plot(E, Widmo1/max(Widmo1), 'r', \
                 E, self.Widmo2/max(Widmo2), \
                 'b', self.x, self.y, 'k.', lw=2)
            self.linex = data_plt[0].get_data()
            self.liney = data_plt[1].get_data()
            self.linez = data_plt[2].get_data()
        else:
            print("X/Y NOT updated!")
            data_plt = plt.plot(E, Widmo1/max(Widmo1), 'r', \
                 E, Widmo2/max(Widmo2), \
                 'b', lw=2)
            self.linex = data_plt[0].get_data()
            self.liney = data_plt[1].get_data()

        plt.ylabel('PL [j. w.]')
        plt.xlabel('Energy [eV]')
        plt.savefig("plot_pl_ev_tmp.png", dpi=80)
        self.pb = Pixbuf.new_from_file("plot_pl_ev_tmp.png")
        self.generated_pl_ev = Image.new_from_file("plot_pl_ev_tmp.png")
        plt.savefig("plot_pl_ev_tmp.png", dpi=200)
        plt.close()

    def plot_widmo_cbdos(self, Ec, Ev, dosCB):
        plt.ylabel('CB DOS [j. w.]')
        plt.xlabel('Energy [eV]')
        data_plt_cb = plt.plot(Ec, dosCB, 'k', lw=2)

        self.linex = data_plt_cb[0].get_data()

        plt.savefig("plot_cbdos_tmp.png", dpi=80)
        self.pb = Pixbuf.new_from_file("plot_cbdos_tmp.png")
        self.generated_cbdos = Image.new_from_file("plot_cbdos_tmp.png")
        plt.savefig("plot_cbdos_tmp.png", dpi=200)
        plt.close()

    def plot_widmo_hh_lh_dos(self, Ev, dosHH, dosLH):
        plt.ylabel('HH and LH DOS [j. w.]')
        plt.xlabel('Energy [eV]')
        data_plt_vb = plt.plot(Ev, dosHH        \
                    + abs(min(dosHH)), 'r', Ev, \
      dosLH + abs(min(dosLH)), 'b', lw=2)

        self.linex = data_plt_vb[0].get_data()

        plt.savefig("plot_hh_lh_dos_tmp.png", dpi=80)
        self.pb = Pixbuf.new_from_file("plot_hh_lh_dos_tmp.png")
        self.generated_hh_lh_dos = Image.new_from_file(
            "plot_hh_lh_dos_tmp.png")
        plt.savefig("plot_hh_lh_dos_tmp.png", dpi=200)
        plt.close()

    def plot_widmo_vbdos(self, Ev, dosVB):
        plt.ylabel('VB DOS [j. w.]')
        plt.xlabel('Energy [eV]')
        data_plt_vb = plt.plot(Ev, dosVB + abs(min(dosVB)), 'k', lw=2)

        self.linex = data_plt_vb[0].get_data()

        plt.savefig("plot_vbdos_tmp.png", dpi=80)
        self.pb = Pixbuf.new_from_file("plot_vbdos_tmp.png")
        self.generated_vbdos = Image.new_from_file("plot_vbdos_tmp.png")
        plt.savefig("plot_vbdos_tmp.png", dpi=200)
        plt.close()

    def plot_widmo_jdos(self, E, JDOS, JDOS2, Hevisajd):
        plt.ylabel('JDOS [j. w.]')
        plt.xlabel('Energy [eV]')
        data_plt_j = plt.plot(E, JDOS/max(JDOS), 'r', \
                       E, JDOS2/max(JDOS2), 'b', \
                       E, Hevisajd/max(Hevisajd), 'k', lw=2)

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
