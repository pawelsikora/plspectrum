from gi import pygtkcompat
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
import numpy as np
import itertools as it
import csv

pygtkcompat.enable()
pygtkcompat.enable_gtk(version='3.0')

import gtk

from QSpectrum import Spectrum_generator

class GUI:

    def generate_graph(self, widget, data=None):
        try:
            print("Try var with filename:" + self.read_own_graph_file_name)
        except AttributeError:
            print("File is NOT set")
            self.c = Spectrum_generator()
        else:
            print("File is set")
            self.c = Spectrum_generator(self.read_own_graph_file_name)

        if(self.entry_param_en.get_text() != ""):
            self.c.params.En = np.fromstring(self.entry_param_en.get_text(), dtype=float, sep=',')

        if(self.entry_param_cp.get_text() != ""):
            self.c.params.CP = np.fromstring(self.entry_param_cp.get_text(), dtype=float, sep=',')

        self.c.params.A0 = float(self.entry_param_a0.get_text())
        print("A0 after change: " + str(self.c.params.A0))
        self.c.params.g0 = float(self.entry_param_g0.get_text())
        print("g0 after change: " + str(self.c.params.g0))
        self.c.params.Eg = float(self.entry_param_eg.get_text())
        print("Eg after change: " + str(self.c.params.Eg))
        self.c.params.Ef = float(self.entry_param_ef.get_text())
        print("Eg after change: " + str(self.c.params.Ef))
        self.c.params.E = np.arange(float(self.entry_param_emin.get_text()),
                                    float(self.entry_param_emax.get_text()),
                                    float(self.entry_param_edn.get_text()))
        print("E after change: " + str(self.c.params.E))
        self.c.params.T = float(self.entry_param_T.get_text())
        print("T after change: " + str(self.c.params.T))
        self.c.params.gamma = float(self.entry_param_gamma.get_text())
        print("gamma after change: " + str(self.c.params.gamma))
        self.c.params.gamma_schodek = float(self.entry_param_gamma_schodek.get_text())
        print("gamma_schodek after change: " + str(self.c.params.gamma_schodek))

        if (self.c.params.A0) == 0 or self.c.params.g0  == 0 or \
           self.c.params.Eg == 0 or self.c.params.T == 0 or \
           self.c.params.gamma == 0 or self.c.params.gamma_schodek == 0:
              print("some values are set to 0!")
              dialog1 = gtk.MessageDialog(None, 0, gtk.MessageType.INFO,
                  gtk.ButtonsType.OK, "Values can't be zero!")
              dialog1.format_secondary_text(
                  "Some of your values appears to be empty. Please check it and type again")
              dialog1.run()
              dialog1.destroy()

        self.c.params.LAMBDA = (1.24 / self.c.params.E)
        print("LAMBDA after change: " + str(self.c.params.LAMBDA))
        self.spectrum_choice = self.spectrum_combobox.get_active()

        if self.spectrum_choice == 1:
           self.frame1.remove(self.currentGraph)
           self.c.calculate_all()
           self.c.plot_widmo_alfa()
           self.currentGraph = self.c.generated_alfa
        elif self.spectrum_choice == 2:
           self.frame1.remove(self.currentGraph)
           self.c.calculate_all()
           self.c.plot_widmo_beta()
           self.currentGraph = self.c.generated_beta
        else:
           dialog = gtk.MessageDialog(None, 0, gtk.MessageType.INFO,
               gtk.ButtonsType.OK, "Wrong choice!")
           dialog.format_secondary_text(
               "You have not chosen any spectrum to generate. Please choose one and try again")
           dialog.run()
           dialog.destroy()

        self.frame1.add(self.currentGraph)
        self.window.show_all()

    def save_to_origin(self, widget, data=None):
        self.spectrum_choice = self.spectrum_combobox.get_active()
        if self.spectrum_choice == 1:
           dialog_alfa = gtk.FileChooserDialog("Please choose a file", None,
               gtk.FileChooserAction.SAVE,
               (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
                gtk.STOCK_SAVE, gtk.ResponseType.OK))

           dialog_alfa.set_current_name('alfa_spectrum_origin_Untitled.txt')
           response = dialog_alfa.run()
           if response == gtk.ResponseType.OK:
               print("Save clicked")
               print("File selected: " + dialog_alfa.get_filename())

               f = open(dialog_alfa.get_filename(), 'wb')
               data = np.array([self.c.linex[0], self.c.linex[1], self.c.liney[1], self.c.linez[1]])
               data = data.T
               somestr = "X Y1 Y2 Y3\n"
               f.write(somestr.encode('ascii'))
               np.savetxt(f, data, fmt='%.7f %.7f %.7f %.7f')
               f.close()

           dialog_alfa.destroy()
        elif self.spectrum_choice == 2:
           dialog_beta = gtk.FileChooserDialog("Please choose a file", None,
               gtk.FileChooserAction.SAVE,
               (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
                gtk.STOCK_SAVE, gtk.ResponseType.OK))

           dialog_beta.set_current_name('beta_spectrum_origin_Untitled.txt')
           response = dialog_beta.run()
           if response == gtk.ResponseType.OK:
               print("Save clicked")
               print("File selected: " + dialog_beta.get_filename())

               f = open(dialog_beta.get_filename(), 'wb')
               data = np.array([self.c.linex[0], self.c.linex[1], self.c.liney[1]])
               data = data.T
               somestr = "X Y1 Y2\n"
               f.write(somestr.encode('ascii'))
               np.savetxt(f, data, fmt='%.7f %.7f %.7f')
               f.close()

           dialog_beta.destroy()

    def save_graph(self, widget, data=None):
        self.spectrum_choice = self.spectrum_combobox.get_active()

        dialog_graph = gtk.FileChooserDialog("Please choose the name of a file to save", None,
            gtk.FileChooserAction.SAVE,
            (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
             gtk.STOCK_SAVE, gtk.ResponseType.OK))

        if self.spectrum_choice == 1:
            dialog_graph.set_current_name('alfa_spectrum_graph_Untitled.png')
        elif self.spectrum_choice == 2:
            dialog_graph.set_current_name('beta_spectrum_graph_Untitled.png')

        response = dialog_graph.run()
        if response == gtk.ResponseType.OK:
            print("Save clicked")
            print("File selected: " + dialog_graph.get_filename())
            self.c.pb.savev(dialog_graph.get_filename(), "png", [], [])

        dialog_graph.destroy()

    def on_read_data_for_graph_toogled(self, widget, data=None):
        self.spectrum_choice = self.spectrum_combobox.get_active()

        dialog_own_graph_file = gtk.FileChooserDialog("Please choose file to open", None,
            gtk.FileChooserAction.OPEN,
            (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
             gtk.STOCK_OPEN, gtk.ResponseType.OK))

        response = dialog_own_graph_file.run()
        if response == gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog_own_graph_file.get_filename())

        self.read_own_graph_file_name = dialog_own_graph_file.get_filename()
        self.entry_readOwnFileForGraph.set_text(self.read_own_graph_file_name)

        dialog_own_graph_file.destroy()

    def delete_event(self, widget, event, data=None):
        print("delete event occurred")
        return False

    def destroy(self, widget, data=None):
        print("destroy signal occurred")
        gtk.main_quit()

    def changed_energy_levels(self, widget, data=None):
        txt_in_entry = self.entry_param_en.get_text()

        if txt_in_entry == "":
            self.label_number_of_energy_levels.set_markup("<b>0</b>")
        else:
            self.label_number_of_energy_levels.set_markup("<b>"+str(txt_in_entry.count(',') + 1)+"</b>")

    def changed_integral_param(self, widget, data=None):
        txt_in_entry = self.entry_param_cp.get_text()

        if txt_in_entry == "":
            self.label_number_of_integrals.set_markup("<b>0</b>")
        else:
            self.label_number_of_integrals.set_markup("<b>"+str(txt_in_entry.count(',') + 1)+"</b>")

    def on_spectrum_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            print("Selected: ID=%d, name=%s" % (row_id, name))
        else:
            entry = combo.get_child()
            print("Entered: %s" % entry.get_text())


    def on_compound_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            print("Selected: ID=%d, name=%s" % (row_id, name))
        else:
            entry = combo.get_child()
            print("Entered: %s" % entry.get_text())

        compound = combo.get_active()

        if compound == 1:
            self.entry_param_mee.set_text("0")
            self.entry_param_mee.set_sensitive(False)
            self.entry_param_mehh.set_text("0")
            self.entry_param_mehh.set_sensitive(False)
            self.entry_param_melh.set_text("0")
            self.entry_param_melh.set_sensitive(False)
        elif compound == 2:
            self.entry_param_mee.set_text("1")
            self.entry_param_mee.set_sensitive(False)
            self.entry_param_mehh.set_text("1")
            self.entry_param_mehh.set_sensitive(False)
            self.entry_param_melh.set_text("1")
            self.entry_param_melh.set_sensitive(False)
        elif compound == 3:
            self.entry_param_mee.set_text("2")
            self.entry_param_mee.set_sensitive(False)
            self.entry_param_mehh.set_text("2")
            self.entry_param_mehh.set_sensitive(False)
            self.entry_param_melh.set_text("2")
            self.entry_param_melh.set_sensitive(False)
        elif compound == 0:
            self.entry_param_mee.set_text("")
            self.entry_param_mee.set_sensitive(True)
            self.entry_param_mehh.set_text("")
            self.entry_param_mehh.set_sensitive(True)
            self.entry_param_melh.set_text("")
            self.entry_param_melh.set_sensitive(True)

    def __init__(self):
        self.i = 0
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(1400, 450)
        self.window.set_icon_from_file('icon.png')
        self.grid = gtk.Grid()

        self.grid.set_column_spacing(20)
        self.grid.set_row_spacing(20)
        self.window.add(self.grid)

        self.initGraph = gtk.Image.new_from_file('init_frame_image.png')
        self.currentGraph = self.initGraph

        # combobox for choosing spectrum
        spectrum_store = gtk.ListStore(int, str)
        spectrum_store.append([1, "--- Choose spectrum ---"])
        spectrum_store.append([11, "Widmo alfa"])
        spectrum_store.append([12, "Widmo beta"])
        spectrum_store.append([2, "Widmo gamma"])
        self.spectrum_combobox = gtk.ComboBox.new_with_model_and_entry(spectrum_store)
        self.spectrum_combobox.connect("changed", self.on_spectrum_combo_changed)
        self.spectrum_combobox.set_entry_text_column(1)
        self.spectrum_combobox.set_active(0)

        # combobox for choosing compound
        compound_store = gtk.ListStore(int, str)
        compound_store.append([1, "--- Custom ---"])
        compound_store.append([11, "GaAs"])
        compound_store.append([12, "InAs"])
        compound_store.append([2, "GaInAs"])
        self.compound_combobox = gtk.ComboBox.new_with_model_and_entry(compound_store)
        self.compound_combobox.connect("changed", self.on_compound_combo_changed)
        self.compound_combobox.set_entry_text_column(1)
        self.compound_combobox.set_active(0)

        self.frame1 = gtk.Frame(label="Graph")
        self.frame1.set_label_align(0.5, 0.5)
        self.frame1.add(self.currentGraph)

        self.label_param_a0 = gtk.Label("A0")
        self.label_param_g0 = gtk.Label("g0")
        self.label_param_eg = gtk.Label("Eg")
        self.label_param_ef = gtk.Label("Ef")
        self.label_param_en = gtk.Label("En")
        self.label_param_emin = gtk.Label("Emin")
        self.label_param_emax = gtk.Label("Emax")
        self.label_param_edn = gtk.Label("Edn")
        self.label_param_cp = gtk.Label("CP")
        self.label_param_T = gtk.Label("T")
        self.label_param_gamma = gtk.Label("Gamma")
        self.label_param_gamma_schodek = gtk.Label("Gamma schodek")
        self.label_param_mee = gtk.Label("mee")
        self.label_param_mehh = gtk.Label("mehh")
        self.label_param_melh = gtk.Label("melh")
        self.label_emass_pick = gtk.Label("Pick values for specific sc compound: ")
        self.label_energy_levels = gtk.Label("Nb of energy states ")
        self.label_number_of_energy_levels = gtk.Label("0")
        self.label_integrals = gtk.Label("Nb of integrals ")
        self.label_number_of_integrals = gtk.Label("0")

        self.label_param_a0.set_xalign(1)
        self.label_param_g0.set_xalign(1)
        self.label_param_eg.set_xalign(0.5)
        self.label_param_ef.set_xalign(0.5)
        self.label_param_en.set_xalign(0.5)
        self.label_param_emin.set_xalign(0.5)
        self.label_param_emax.set_xalign(0.5)
        self.label_param_edn.set_xalign(0.5)
        self.label_param_cp.set_xalign(0.5)
        self.label_param_T.set_xalign(1)
        self.label_param_gamma.set_xalign(1)
        self.label_param_gamma_schodek.set_xalign(1)
        self.label_energy_levels.set_xalign(1)
        self.label_number_of_energy_levels.set_xalign(0.5)
        self.label_number_of_integrals.set_xalign(0.5)
        self.label_integrals.set_xalign(0.5)
        self.label_param_mee.set_xalign(1)
        self.label_param_mehh.set_xalign(1)
        self.label_param_melh.set_xalign(1)
        self.label_emass_pick.set_xalign(0.5)

        self.entry_param_a0 = gtk.Entry()
        self.entry_param_g0 = gtk.Entry()
        self.entry_param_eg = gtk.Entry()
        self.entry_param_ef = gtk.Entry()
        self.entry_param_en = gtk.Entry()
        self.entry_param_emin = gtk.Entry()
        self.entry_param_emax = gtk.Entry()
        self.entry_param_edn = gtk.Entry()
        self.entry_param_cp = gtk.Entry()
        self.entry_param_T = gtk.Entry()
        self.entry_param_gamma = gtk.Entry()
        self.entry_param_gamma_schodek = gtk.Entry()
        self.entry_param_mee = gtk.Entry()
        self.entry_param_mehh = gtk.Entry()
        self.entry_param_melh = gtk.Entry()

        # frame energy
        self.frame_energy = gtk.Frame(label="Energies")
        self.frame_energy.set_label_align(0.5, 0.5)
        self.grid_energy = gtk.Grid()
        self.grid_energy.set_row_spacing(10)
        self.grid_energy.set_column_spacing(60)
        self.frame_energy.add(self.grid_energy)

        # entries for energy frame
        self.entry_param_eg.set_width_chars(5)
        self.entry_param_en.connect("changed", self.changed_energy_levels, None)
        self.entry_param_cp.connect("changed", self.changed_integral_param, None)
        self.label_number_of_energy_levels.set_markup("<b>0</b>")
        self.label_number_of_integrals.set_markup("<b>0</b>")
        self.grid_energy.attach(self.label_energy_levels, 5, 0, 1, 1)
        self.grid_energy.attach(self.label_number_of_energy_levels, 5, 1, 1, 1)
        self.grid_energy.attach(self.label_param_en, 0, 1, 1, 1)
        self.grid_energy.attach(self.label_param_emin, 0, 3, 1, 1)
        self.grid_energy.attach(self.label_param_emax, 0, 4, 1, 1)
        self.grid_energy.attach(self.label_param_edn, 0, 5, 1, 1)
        self.grid_energy.attach(self.label_param_eg, 0, 6, 1, 1)
        self.grid_energy.attach(self.label_param_ef, 0, 7, 1, 1)
        self.grid_energy.attach(self.label_param_cp, 0, 8, 1, 1)
        self.grid_energy.attach(self.entry_param_en, 1, 1, 4, 1)
        self.grid_energy.attach(self.entry_param_emin, 1, 3, 1, 1)
        self.grid_energy.attach(self.entry_param_emax, 1, 4, 1, 1)
        self.grid_energy.attach(self.entry_param_edn, 1, 5, 1, 1)
        self.grid_energy.attach(self.entry_param_eg, 1, 6, 1, 1)
        self.grid_energy.attach(self.entry_param_ef, 1, 7, 1, 1)
        self.grid_energy.attach(self.entry_param_cp, 1, 8, 4, 1)
        self.grid_energy.attach(self.label_integrals, 5, 7, 1, 1)
        self.grid_energy.attach(self.label_number_of_integrals, 5, 8, 1, 1)

        # frame electron mass
        self.frame_emass = gtk.Frame(label="Mass of electrons")
        self.frame_emass.set_label_align(0.5, 0.5)
        self.grid_emass = gtk.Grid()
        self.grid_emass.set_row_spacing(20)
        self.grid_emass.set_column_spacing(70)
        self.frame_emass.add(self.grid_emass)

        self.grid_emass.attach(self.label_emass_pick, 0, 1, 3, 1)
        self.grid_emass.attach(self.compound_combobox, 3, 1, 1, 1)
        self.grid_emass.attach(self.label_param_mee, 0, 2, 2, 1)
        self.grid_emass.attach(self.label_param_mehh, 0, 3, 2, 1)
        self.grid_emass.attach(self.label_param_melh, 0, 4, 2, 1)
        self.grid_emass.attach(self.entry_param_mee, 2, 2, 1, 1)
        self.grid_emass.attach(self.entry_param_mehh, 2, 3, 1, 1)
        self.grid_emass.attach(self.entry_param_melh, 2, 4, 1, 1)

        # main buttons/entries
        self.button1 = gtk.Button('Generate graph!')
        self.buttonExportToOrigin = gtk.Button('Export data to txt')
        self.buttonExportToOrigin.connect("clicked", self.save_to_origin, None)
        self.buttonSaveImage = gtk.Button('Save Graph')
        self.check_if_graph_your_data = gtk.CheckButton("Draw own data on graph")
        self.entry_readOwnFileForGraph = gtk.Entry()

        # events
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.button1.connect("clicked", self.generate_graph, None)
        self.buttonSaveImage.connect("clicked", self.save_graph, None)
        self.check_if_graph_your_data.connect("toggled", self.on_read_data_for_graph_toogled, None)

        # Other param entries
        self.grid.attach(self.label_param_gamma, 0, 2, 1, 1)
        self.grid.attach_next_to(self.label_param_gamma_schodek, self.label_param_gamma, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.label_param_T, self.label_param_gamma_schodek, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.label_param_a0, self.label_param_T, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.label_param_g0, self.label_param_a0, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach(self.entry_param_gamma, 1, 2, 1, 1)
        self.grid.attach_next_to(self.entry_param_gamma_schodek, self.entry_param_gamma, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_param_T, self.entry_param_gamma_schodek, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_param_a0,self.entry_param_T, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_param_g0,self.entry_param_a0, gtk.PositionType.BOTTOM, 1, 1)

        # frames
        self.grid.attach(self.frame_energy, 2, 1, 4, 7)
        self.grid.attach(self.frame_emass, 2, 8, 4, 7)
        self.grid.attach(self.frame1, 6, 0, 6, 14)

        # main functionality
        self.grid.attach(self.button1, 10, 15, 3, 1)
        self.grid.attach_next_to(self.buttonExportToOrigin, self.button1, gtk.PositionType.TOP, 1, 1)
        self.grid.attach_next_to(self.buttonSaveImage, self.buttonExportToOrigin, gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(self.spectrum_combobox, self.button1, gtk.PositionType.LEFT, 1, 1)
        self.grid.attach_next_to(self.entry_readOwnFileForGraph, self.buttonExportToOrigin, gtk.PositionType.LEFT, 1, 1)
        self.grid.attach_next_to(self.check_if_graph_your_data, self.entry_readOwnFileForGraph, gtk.PositionType.LEFT, 3, 1)

        self.window.set_border_width(30)
        self.window.show_all()

    def main(self):
        gtk.main()
