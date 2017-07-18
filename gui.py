import numpy as np
from QSpectrum import Spectrum_generator

import gi
gi.require_version  ('Gtk', '3.0')
from gi.repository import Gtk

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

        if (self.entry_param_mee.get_text() != ""):
            self.c.params.me = float(self.entry_param_mee.get_text())
        print("gamma_schodek after change: " + str(self.c.params.me))
        if (self.entry_param_mehh.get_text() != ""):
            self.c.params.mehh = float(self.entry_param_mehh.get_text())
        print("gamma_schodek after change: " + str(self.c.params.mehh))
        if (self.entry_param_melh.get_text() != ""):
            self.c.params.melh = float(self.entry_param_melh.get_text())
        print("gamma_schodek after change: " + str(self.c.params.melh))

        if (self.c.params.A0) == 0 or self.c.params.g0  == 0 or \
           self.c.params.Eg == 0 or self.c.params.T == 0 or \
           self.c.params.gamma == 0 or self.c.params.gamma_schodek == 0:
              print("some values are set to 0!")
              dialog1 = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                  Gtk.ButtonsType.OK, "Values can't be zero!")
              dialog1.format_secondary_text(
                  "Some of your values appears to be empty. Please check it and type again")
              dialog1.run()
              dialog1.destroy()

        self.c.params.LAMBDA = (1.24 / self.c.params.E)
        print("LAMBDA after change: " + str(self.c.params.LAMBDA))
        self.spectrum_choice = self.spectrum_combobox.get_active()

        self.frame1.remove(self.currentGraph)
        self.c.calculate_all()

        if self.spectrum_choice == 1:
           self.c.plot_widmo_alfa()
           self.currentGraph = self.c.generated_alfa
        elif self.spectrum_choice == 2:
           self.c.plot_widmo_beta()
           self.currentGraph = self.c.generated_beta
        elif self.spectrum_choice == 3:
           self.c.plot_widmo_cbdos()
           self.currentGraph = self.c.generated_cbdos
        elif self.spectrum_choice == 4:
           self.c.plot_widmo_vbdos()
           self.currentGraph = self.c.generated_vbdos
        elif self.spectrum_choice == 5:
           self.c.plot_widmo_jdos()
           self.currentGraph = self.c.generated_jdos
        else:
           dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
               Gtk.ButtonsType.OK, "Wrong choice!")
           dialog.format_secondary_text(
               "You have not chosen any spectrum to generate. Please choose one and try again")
           dialog.run()
           dialog.destroy()

        self.frame1.add(self.currentGraph)
        self.window.show_all()

    def save_to_origin(self, widget, data=None):
        self.spectrum_choice = self.spectrum_combobox.get_active()
        dialog_origin = Gtk.FileChooserDialog("Please choose a file", None,
           Gtk.FileChooserAction.SAVE,
           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
           Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        if self.spectrum_choice == 1:
           dialog_origin.set_current_name('alfa_spectrum_origin_Untitled.txt')
           response = dialog_origin.run()
           if response == Gtk.ResponseType.OK:
               print("Save clicked")
               print("File selected: " + dialog_origin.get_filename())

               f = open(dialog_origin.get_filename(), 'wb')
               data = np.array([self.c.linex[0], self.c.linex[1], self.c.liney[1], self.c.linez[1]])
               data = data.T
               somestr = "X Y1 Y2 Y3\n"
               f.write(somestr.encode('ascii'))
               np.savetxt(f, data, fmt='%.7f %.7f %.7f %.7f')
               f.close()

           dialog_origin.destroy()

        elif self.spectrum_choice == 2:
           dialog_origin.set_current_name('beta_spectrum_origin_Untitled.txt')
           response = dialog_origin.run()
           if response == Gtk.ResponseType.OK:
               print("Save clicked")
               print("File selected: " + dialog_origin.get_filename())

               f = open(dialog_origin.get_filename(), 'wb')
               data = np.array([self.c.linex[0], self.c.linex[1], self.c.liney[1]])
               data = data.T
               somestr = "X Y1 Y2\n"
               f.write(somestr.encode('ascii'))
               np.savetxt(f, data, fmt='%.7f %.7f %.7f')
               f.close()

           dialog_origin.destroy()

        elif self.spectrum_choice == 3:
           dialog_origin.set_current_name('cbdos_spectrum_origin_Untitled.txt')
           response = dialog_origin.run()
           if response == Gtk.ResponseType.OK:
               print("Save clicked")
               print("File selected: " + dialog_origin.get_filename())

               f = open(dialog_origin.get_filename(), 'wb')
               data = np.array([self.c.linex[0], self.c.linex[1]])
               data = data.T
               somestr = "X Y1\n"
               f.write(somestr.encode('ascii'))
               np.savetxt(f, data, fmt='%.7f %.7f')
               f.close()

           dialog_origin.destroy()

        elif self.spectrum_choice == 4:
           dialog_origin.set_current_name('vbdos_spectrum_origin_Untitled.txt')
           response = dialog_origin.run()
           if response == Gtk.ResponseType.OK:
               print("Save clicked")
               print("File selected: " + dialog_origin.get_filename())

               f = open(dialog_origin.get_filename(), 'wb')
               data = np.array([self.c.linex[0], self.c.linex[1]])
               data = data.T
               somestr = "X Y1\n"
               f.write(somestr.encode('ascii'))
               np.savetxt(f, data, fmt='%.7f %.7f')
               f.close()

           dialog_origin.destroy()

        elif self.spectrum_choice == 5:
           dialog_origin.set_current_name('jdos_spectrum_origin_Untitled.txt')
           response = dialog_origin.run()
           if response == Gtk.ResponseType.OK:
               print("Save clicked")
               print("File selected: " + dialog_origin.get_filename())

               f = open(dialog_origin.get_filename(), 'wb')
               data = np.array([self.c.linex[0], self.c.linex[1], self.c.liney[1], self.c.linez[1]])
               data = data.T
               somestr = "X Y1 Y2 Y3\n"
               f.write(somestr.encode('ascii'))
               np.savetxt(f, data, fmt='%.7f %.7f %.7f %.7f')
               f.close()

           dialog_origin.destroy()

    def save_graph(self, widget, data=None):
        self.spectrum_choice = self.spectrum_combobox.get_active()

        dialog_graph = Gtk.FileChooserDialog("Please choose the name of a file to save", None,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        if self.spectrum_choice == 1:
            dialog_graph.set_current_name('alfa_spectrum_graph_Untitled.png')
        elif self.spectrum_choice == 2:
            dialog_graph.set_current_name('beta_spectrum_graph_Untitled.png')

        response = dialog_graph.run()
        if response == Gtk.ResponseType.OK:
            print("Save clicked")
            print("File selected: " + dialog_graph.get_filename())
            self.c.pb.savev(dialog_graph.get_filename(), "png", [], [])

        dialog_graph.destroy()

    def on_read_data_for_graph_toogled(self, widget, data=None):
        self.spectrum_choice = self.spectrum_combobox.get_active()

        dialog_own_graph_file = Gtk.FileChooserDialog("Please choose file to open", None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog_own_graph_file.run()
        if response == Gtk.ResponseType.OK:
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
        Gtk.main_quit()

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
        self.window = Gtk.Window()
        self.window.set_size_request(1200, 450)
        self.window.set_icon_from_file('icon.png')
        self.grid = Gtk.Grid()

        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(10)
        self.window.add(self.grid)

        self.initGraph = Gtk.Image.new_from_file('init_frame_image.png')
        self.currentGraph = self.initGraph

        # combobox for choosing spectrum
        spectrum_store = Gtk.ListStore(int, str)
        spectrum_store.append([1, "--- Choose spectrum ---"])
        spectrum_store.append([11, "Absorption"])
        spectrum_store.append([12, "Spectrum"])
        spectrum_store.append([21, "CB DOS"])
        spectrum_store.append([22, "VB DOS"])
        spectrum_store.append([3, "JDOS"])
        self.spectrum_combobox = Gtk.ComboBox.new_with_model_and_entry(spectrum_store)
        self.spectrum_combobox.connect("changed", self.on_spectrum_combo_changed)
        self.spectrum_combobox.set_entry_text_column(1)
        self.spectrum_combobox.set_active(0)

        # combobox for choosing compound
        compound_store = Gtk.ListStore(int, str)
        compound_store.append([1, "--- Custom ---"])
        compound_store.append([11, "GaAs"])
        compound_store.append([12, "InAs"])
        compound_store.append([2, "GaInAs"])
        self.compound_combobox = Gtk.ComboBox.new_with_model_and_entry(compound_store)
        self.compound_combobox.connect("changed", self.on_compound_combo_changed)
        self.compound_combobox.set_entry_text_column(1)
        self.compound_combobox.set_active(0)

        self.frame1 = Gtk.Frame(label="Graph")
        self.frame1.set_label_align(0.5, 0.5)
        self.frame1.add(self.currentGraph)

        self.label_param_a0 = Gtk.Label("A0")
        self.label_param_g0 = Gtk.Label("g0")
        self.label_param_eg = Gtk.Label("Eg")
        self.label_param_ef = Gtk.Label("Ef")
        self.label_param_en = Gtk.Label("En")
        self.label_param_emin = Gtk.Label("Emin")
        self.label_param_emax = Gtk.Label("Emax")
        self.label_param_edn = Gtk.Label("Edn")
        self.label_param_cp = Gtk.Label("CP")
        self.label_param_T = Gtk.Label("T")
        self.label_param_gamma = Gtk.Label("Gamma")
        self.label_param_gamma_schodek = Gtk.Label("Gamma schodek")
        self.label_param_mee = Gtk.Label("mee")
        self.label_param_mehh = Gtk.Label("mehh")
        self.label_param_melh = Gtk.Label("melh")
        self.label_emass_pick = Gtk.Label("Pick values for specific sc compound: ")
        self.label_energy_levels = Gtk.Label("Nb of energy states ")
        self.label_number_of_energy_levels = Gtk.Label("0")
        self.label_integrals = Gtk.Label("Nb of integrals ")
        self.label_number_of_integrals = Gtk.Label("0")

        self.label_param_a0.set_xalign(1)
        self.label_param_g0.set_xalign(1)
        self.label_param_eg.set_xalign(1)
        self.label_param_ef.set_xalign(1)
        self.label_param_en.set_xalign(1)
        self.label_param_emin.set_xalign(1)
        self.label_param_emax.set_xalign(1)
        self.label_param_edn.set_xalign(1)
        self.label_param_cp.set_xalign(1)
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

        self.entry_param_a0 = Gtk.Entry()
        self.entry_param_g0 = Gtk.Entry()
        self.entry_param_eg = Gtk.Entry()
        self.entry_param_ef = Gtk.Entry()
        self.entry_param_en = Gtk.Entry()
        self.entry_param_emin = Gtk.Entry()
        self.entry_param_emax = Gtk.Entry()
        self.entry_param_edn = Gtk.Entry()
        self.entry_param_cp = Gtk.Entry()
        self.entry_param_T = Gtk.Entry()
        self.entry_param_gamma = Gtk.Entry()
        self.entry_param_gamma_schodek = Gtk.Entry()
        self.entry_param_mee = Gtk.Entry()
        self.entry_param_mehh = Gtk.Entry()
        self.entry_param_melh = Gtk.Entry()

        # frame energy
        self.frame_energy = Gtk.Frame(label="Energies")
        self.frame_energy.set_label_align(0.5, 0.5)
        self.grid_energy = Gtk.Grid()
        self.grid_energy.set_row_spacing(10)
        self.grid_energy.set_column_spacing(30)
        self.frame_energy.add(self.grid_energy)

        # entries for energy frame
        self.entry_param_eg.set_width_chars(5)
        self.entry_param_en.connect("changed", self.changed_energy_levels, None)
        self.entry_param_cp.connect("changed", self.changed_integral_param, None)
        self.label_number_of_energy_levels.set_markup("<b>0</b>")
        self.label_number_of_integrals.set_markup("<b>0</b>")
        self.grid_energy.attach(self.label_energy_levels, 4, 0, 1, 1)
        self.grid_energy.attach(self.label_number_of_energy_levels, 4, 1, 1, 1)
        self.grid_energy.attach(self.label_param_en, 0, 1, 1, 1)
        self.grid_energy.attach(self.label_param_emin, 0, 2, 1, 1)
        self.grid_energy.attach(self.label_param_emax, 0, 3, 1, 1)
        self.grid_energy.attach(self.label_param_edn, 0, 4, 1, 1)
        self.grid_energy.attach(self.label_param_eg, 0, 5, 1, 1)
        self.grid_energy.attach(self.label_param_ef, 0, 6, 1, 1)
        self.grid_energy.attach(self.label_param_cp, 0, 7, 1, 1)
        self.grid_energy.attach(self.entry_param_en, 1, 1, 3, 1)
        self.grid_energy.attach(self.entry_param_emin, 1, 2, 1, 1)
        self.grid_energy.attach(self.entry_param_emax, 1, 3, 1, 1)
        self.grid_energy.attach(self.entry_param_edn, 1, 4, 1, 1)
        self.grid_energy.attach(self.entry_param_eg, 1, 5, 1, 1)
        self.grid_energy.attach(self.entry_param_ef, 1, 6, 1, 1)
        self.grid_energy.attach(self.entry_param_cp, 1, 7, 3, 1)
        self.grid_energy.attach(self.label_integrals, 4, 6, 1, 1)
        self.grid_energy.attach(self.label_number_of_integrals, 4, 7, 1, 1)

        # frame electron mass
        self.frame_emass = Gtk.Frame(label="Mass of electrons")
        self.frame_emass.set_label_align(0.5, 0.5)
        self.grid_emass = Gtk.Grid()
        self.grid_emass.set_row_spacing(10)
        self.grid_emass.set_column_spacing(20)
        self.frame_emass.add(self.grid_emass)

        self.grid_emass.attach(self.label_emass_pick, 0, 1, 2, 1)
        self.grid_emass.attach(self.compound_combobox, 2, 1, 1, 1)
        self.grid_emass.attach(self.label_param_mee, 0, 2, 1, 1)
        self.grid_emass.attach(self.label_param_mehh, 0, 3, 1, 1)
        self.grid_emass.attach(self.label_param_melh, 0, 4, 1, 1)
        self.grid_emass.attach(self.entry_param_mee, 1, 2, 1, 1)
        self.grid_emass.attach(self.entry_param_mehh, 1, 3, 1, 1)
        self.grid_emass.attach(self.entry_param_melh, 1, 4, 1, 1)

        # main buttons/entries
        self.button1 = Gtk.Button('Generate graph!')
        self.buttonExportToOrigin = Gtk.Button('Export data to txt')
        self.buttonExportToOrigin.connect("clicked", self.save_to_origin, None)
        self.buttonSaveImage = Gtk.Button('Save Graph')
        self.check_if_graph_your_data = Gtk.CheckButton("Draw own data on graph")
        self.entry_readOwnFileForGraph = Gtk.Entry()

        # events
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.button1.connect("clicked", self.generate_graph, None)
        self.buttonSaveImage.connect("clicked", self.save_graph, None)
        self.check_if_graph_your_data.connect("toggled", self.on_read_data_for_graph_toogled, None)

        # Other param entries
        self.grid.attach(self.label_param_gamma, 0, 2, 1, 1)
        self.grid.attach_next_to(self.label_param_gamma_schodek, self.label_param_gamma, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.label_param_T, self.label_param_gamma_schodek, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.label_param_a0, self.label_param_T, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.label_param_g0, self.label_param_a0, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach(self.entry_param_gamma, 1, 2, 1, 1)
        self.grid.attach_next_to(self.entry_param_gamma_schodek, self.entry_param_gamma, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_param_T, self.entry_param_gamma_schodek, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_param_a0,self.entry_param_T, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_param_g0,self.entry_param_a0, Gtk.PositionType.BOTTOM, 1, 1)

        # frames
        self.grid.attach(self.frame_energy, 2, 1, 5, 7)
        self.grid.attach(self.frame_emass, 2, 8, 5, 7)
        self.grid.attach(self.frame1, 7, 0, 4, 10)

        # main functionality
        self.grid.attach(self.button1, 8, 12, 3, 1)
        self.grid.attach_next_to(self.buttonExportToOrigin, self.button1, Gtk.PositionType.TOP, 1, 1)
        self.grid.attach_next_to(self.buttonSaveImage, self.buttonExportToOrigin, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(self.spectrum_combobox, self.button1, Gtk.PositionType.LEFT, 1, 1)
        self.grid.attach_next_to(self.entry_readOwnFileForGraph, self.buttonExportToOrigin, Gtk.PositionType.TOP, 1, 1)
        self.grid.attach_next_to(self.check_if_graph_your_data, self.entry_readOwnFileForGraph, Gtk.PositionType.LEFT, 1, 1)

        self.window.set_border_width(30)
        self.window.show_all()

    def main(self):
        Gtk.main()
