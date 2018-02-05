#!/usr/bin/env python

from common import *

class Calculator:

        def __init__(self):
            self.a = 0
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
            self.urehh = 0
            self.urelh = 0
            self.masy_r = 0

            self.params = Parameters()
            self.params.update()

        def calculate_u_relh(self, me, melh):
            self.urelh = (me * melh) \
                        / (me + melh)

        def calculate_u_rehh(self, me, mehh):
            self.urehh = (me * mehh) \
                        / (me + mehh)

        def calculate_dosCB(self, g0, me, Ec, CB):
            for i in range(0, len(CB)):
		self.dosCB = self.dosCB + g0 * me \
		        * (Schodek(Ec - CB[i]))

        def calculate_dosHH(self, g0, HH, mehh, Ev):
            for i in range(0, len(HH)):
                self.dosHH = self.dosHH - g0 \
                    * mehh \
                    * (Schodek(Ev - HH[i]))

        def calculate_dosHH_probability(self, HH, Ev, g0, mehh):
            for i in range(0, len(HH)):
                self.dosHH_probability = self.dosHH_probability \
                    - g0 * mehh \
                    * (Schodek(Ev - HH[i]))

        def calculate_dosLH(self, g0, LH, Ev, melh):
            for i in range(0, len(LH)):
                self.dosLH = self.dosLH - g0 * melh \
                     * (Schodek(Ev - LH[i]))

        def calculate_masy_r(self, En, wsk, urehh, urelh):
            self.masy_r = np.zeros(len(En))
            for i in range(0, len(En)):
                if (wsk[i]=='h' or wsk[i]=='H'):
                    self.masy_r[i]=urehh
                elif (wsk[i]=='l' or wsk[i]=='L'):
                    self.masy_r[i]=urelh

        def calculate_dos(self, En, E, g0, CP, step_func_gamma):
            for i in range(0, len(En)):
                self.DOS = self.DOS + g0 * CP[i] * \
                    (DOS_rozmyty_erf(E, \
                     En[i], step_func_gamma) )

        def calculate_dos2(self, En, E, g0, CP, step_func_gamma):
            for i in range(0, len(En)):
                self.DOS2 = self.DOS2 + g0 * CP[i] * \
                    ( DOS_rozmyty_cauchy(E, \
                     En[i], step_func_gamma) )

        def calculate_hevisajd(self, En, E, g0, masy_r):
            for i in range(0, len(En)):
                self.Hevisajd = self.Hevisajd + g0 * masy_r[i] * \
                    Schodek(E - En[i]) # Hevisajd to jest idealny JDOS!

        def calculate_pik(self, En, A0, E, gamma):
            for i in range(0, len(En)):
                self.Pik = self.Pik + A0 * \
                    ( pik_Lorentza(E, \
                     En[i], gamma) )

        def calculate_Normal(self, En, E, A0, gamma):
            for i in range(0, len(En)):
                self.Normal = self.Normal + A0 * \
                    pik_Gaussowski(E, \
                    En[i], gamma)

        def calculate_pik_mieszany(self, En, E, A0, gamma):
            for i in range(0, len(En)):
                self.Pik_mieszany = self.Pik_mieszany + A0 * \
                    ( pik_Lorentza(E, \
                      En[i], gamma) + \
                      pik_Gaussowski(E, \
                      En[i], gamma) )

        def calculate_delty(self, En, E, A0):
            for i in range(0, len(En)):
                self.Delty = self.Delty + A0 * \
                    Delta(E - En[i])

        def calculate_dosVB(self, En, dosHH, dosLH):
            for i in range(0, len(En)):
                self.dosVB = dosHH + dosLH

        def calculate_jdos(self, En, E, g0, masy_r, step_func_gamma):
            for i in range(0, len(En)):
                self.JDOS = self.JDOS + g0 * masy_r[i] * \
                    (DOS_rozmyty_erf(E, En[i], \
                                     step_func_gamma))

        def calculate_jdos2(self, En, E, g0, masy_r, step_func_gamma):
            for i in range(0, len(En)):
                self.JDOS2 = self.JDOS2 + g0 * masy_r[i] * \
                    (DOS_rozmyty_cauchy(E, En[i], \
                                        step_func_gamma))

        def calculate_abs1(self, En, E, g0, CP, masy_r, step_func_gamma):
            for i in range(0, len(En)):
                self.Abs1 = self.Abs1 + g0 * CP[i] * masy_r[i] * \
                    (DOS_rozmyty_erf(E, En[i], \
                                     step_func_gamma))

        def calculate_abs2(self, En, E, g0, CP, masy_r, step_func_gamma):
            for i in range(0, len(En)):
                self.Abs2 = self.Abs2 + g0 * CP[i] * masy_r[i] * \
                    (DOS_rozmyty_cauchy(E, En[i], \
                                     step_func_gamma))

        def calculate_abs3(self, En, E, g0, CP, masy_r):
            for i in range(0, len(En)):
                self.Abs3 = self.Abs3 + g0 * CP[i] * masy_r[i] * \
                    Schodek(E - En[i])

        def calculate_all_parameters(self):
            self.calculate_u_relh(self.params.me, self.params.melh)
            self.calculate_u_rehh(self.params.me, self.params.mehh)
            self.calculate_dosCB(self.params.g0,
                            self.params.me,
                            self.params.Ec,
                            self.params.CB)

            self.calculate_dosHH(self.params.g0,
                            self.params.HH,
                            self.params.mehh,
                            self.params.Ev)

            self.calculate_dosHH_probability(self.params.HH,
                                        self.params.Ev,
                                        self.params.g0,
                                        self.params.mehh)

            self.calculate_masy_r(self.params.En,
                             self.params.wsk,
                             self.urehh, self.urelh)


            self.calculate_dos(self.params.En,
                          self.params.E,
                          self.params.g0,
                          self.params.CP,
                          self.params.step_func_gamma)

            self.calculate_dos2(self.params.En,
                           self.params.E,
                           self.params.g0,
                           self.params.CP,
                           self.params.step_func_gamma)

            self.calculate_hevisajd(self.params.En,
                               self.params.E,
                               self.params.g0,
                               self.masy_r)

            self.calculate_pik(self.params.En,
                          self.params.A0,
                          self.params.E,
                          self.params.gamma)

            self.calculate_Normal(self.params.En,
                             self.params.E,
                             self.params.A0,
                             self.params.gamma)

            self.calculate_pik_mieszany(self.params.En,
                                   self.params.E,
                                   self.params.A0,
                                   self.params.gamma)


            self.calculate_delty(self.params.En,
                            self.params.E,
                            self.params.A0)

            self.calculate_dosVB(self.params.En,
                           self.dosHH,
                           self.dosLH)

            self.calculate_jdos(self.params.En,
                           self.params.E,
                           self.params.g0,
                           self.masy_r,
                           self.params.step_func_gamma)

            self.calculate_jdos2(self.params.En,
                           self.params.E,
                           self.params.g0,
                           self.masy_r,
                           self.params.step_func_gamma)

            self.calculate_abs1(self.params.En,
                           self.params.E,
                           self.params.g0,
                           self.params.CP,
                           self.masy_r,
                           self.params.step_func_gamma)

            self.calculate_abs2(self.params.En,
                           self.params.E,
                           self.params.g0,
                           self.params.CP,
                           self.masy_r,
                           self.params.step_func_gamma)

            self.calculate_abs3(self.params.En,
                           self.params.E,
                           self.params.g0,
                           self.params.CP,
                           self.masy_r)

        def calculate_widmo_fd(self):
            self.Widmo_fd = self.Pik * self.DOS * \
                distribution_FD(self.params.E, self.params.Ef, self.params.T)

        def calculate_widmo_boltzmann(self):
            self.Widmo_b = self.Pik * self.DOS * \
                distribution_Boltzmann(0.0, self.params.E, self.params.T)

        def calculate_widmo_planck(self):
            self.Widmo1 = (1.0 / self.params.E) * self.Abs1 * \
            distribution_Planck(self.params.E, self.params.T) * self.params.E

        def calculate_prawdopodobienstwo(self):
            self.Prawd = np.zeros(len(self.params.E))
            for i in range(0, len(self.params.E)):
                 self.Prawd[i] = Calka( self.params.E, pik_Gaussowski(self.params.E, \
                                 self.params.E[i], self.params.gamma) * self.Abs1 * \
                                 distribution_Boltzmann(0.0, self.params.E, self.params.T) )

        def calculate_widmo(self):
            self.Widmo2 = self.Prawd * self.params.E

        def generate(self, items):
            for i in range(items):
                yield i

        def calculate_all(self):
            self.calculate_all_parameters()
            self.calculate_widmo_fd()
            self.calculate_widmo_boltzmann()
            self.calculate_widmo_planck()
            self.calculate_prawdopodobienstwo()
            self.calculate_widmo()
