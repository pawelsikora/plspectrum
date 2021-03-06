import numpy as np
from QSpectrum import Spectrum_generator

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

list_store = Gtk.ListStore(int, str, Gtk.Entry, str)


class GUI:
    def __init__(self):
        self.i = 0
        self.window = Gtk.Window()
        self.window.set_size_request(1100, 450)
        self.window.set_icon_from_file('icon.png')
        self.window.set_border_width(30)

        self.notebook = Gtk.Notebook()

        self.create_labels()
        self.set_labels_alignment()
        self.create_entries()
        self.set_width_chars_for_entries()
        self.store_entries_in_list()

        self.create_notebook_page_MAIN()
        self.create_notebook_page_HELP()
        self.create_notebook_page_ABOUT()

        self.fill_entries_for_debug()

        self.window.add(self.notebook)
        self.window.show_all()

    def main(self):
        Gtk.main()

    def generate_graph(self, widget, data=None):
        try:
            print("Try var with filename:" + self.read_own_graph_file_name)
        except AttributeError:
            print("File is NOT set")
            self.generator = Spectrum_generator()
        except TypeError:
            print("There is no variable for the file yet")
            self.generator = Spectrum_generator()
        else:
            print("File is set")
            self.generator = Spectrum_generator(self.read_own_graph_file_name)

        self.calculator = self.generator.calculator

        self.check_if_strings_in_entries_are_valid()

        self.get_strings_from_entries_and_update_params()

        self.frame1.remove(self.currentGraph)
        self.calculator.calculate_all()

        sc = self.spectrum_combobox.get_active()

        self.generate_plot_of_choice(sc)

        self.frame1.add(self.currentGraph)
        self.window.show_all()

    def write_params_to_file(self, filename):
        filename.write("\n--- Parameters used for generated graph ---\n")
        for row in list_store:
            entry = list_store.get_value(row.iter, 2)

            gt = entry.get_text()
            filename.write(
                list_store.get_value(row.iter, 3) + " = " + gt + "\n")

    def save_to_origin(self, widget, data=None):
        self.spectrum_choice = self.spectrum_combobox.get_active()
        dialog_origin = Gtk.FileChooserDialog(
            "Please choose a file", None, Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE,
             Gtk.ResponseType.OK))

        if self.spectrum_choice == 1:
            dialog_origin.set_current_name(
                'absorption_spectrum_origin_Untitled.txt')
            response = dialog_origin.run()
            if response == Gtk.ResponseType.OK:
                print("Save clicked")
                print("File selected: " + dialog_origin.get_filename())

                f = open(dialog_origin.get_filename(), 'wb')
                data = np.array([
                    self.generator.linex[0], self.generator.linex[1],
                    self.generator.liney[1], self.generator.linez[1]
                ])
                data = data.T
                somestr = "X Y1 Y2 Y3\n"
                f.write(somestr.encode('ascii'))
                np.savetxt(f, data, fmt='%.7f %.7f %.7f %.7f')
                self.write_params_to_file(f)
                f.close()

            dialog_origin.destroy()

        elif self.spectrum_choice == 2:
            dialog_origin.set_current_name(
                'pl_um_spectrum_origin_Untitled.txt')
            response = dialog_origin.run()
            if response == Gtk.ResponseType.OK:
                print("Save clicked")
                print("File selected: " + dialog_origin.get_filename())

                f = open(dialog_origin.get_filename(), 'wb')
                data = np.array([
                    self.generator.linex[0], self.generator.linex[1],
                    self.generator.liney[1]
                ])
                data = data.T
                somestr = "X Y1 Y2\n"
                f.write(somestr.encode('ascii'))
                np.savetxt(f, data, fmt='%.7f %.7f %.7f')
                self.write_params_to_file(f)
                f.close()

            dialog_origin.destroy()

        elif self.spectrum_choice == 3:
            dialog_origin.set_current_name(
                'pl_ev_spectrum_origin_Untitled.txt')
            response = dialog_origin.run()
            if response == Gtk.ResponseType.OK:
                print("Save clicked")
                print("File selected: " + dialog_origin.get_filename())

                f = open(dialog_origin.get_filename(), 'wb')
                data = np.array([
                    self.generator.linex[0], self.generator.linex[1],
                    self.generator.liney[1]
                ])
                data = data.T
                somestr = "X Y1 Y2\n"
                f.write(somestr.encode('ascii'))
                np.savetxt(f, data, fmt='%.7f %.7f %.7f')
                self.write_params_to_file(f)
                f.close()

            dialog_origin.destroy()

        elif self.spectrum_choice == 4:
            dialog_origin.set_current_name(
                'cbdos_spectrum_origin_Untitled.txt')
            response = dialog_origin.run()
            if response == Gtk.ResponseType.OK:
                print("Save clicked")
                print("File selected: " + dialog_origin.get_filename())

                f = open(dialog_origin.get_filename(), 'wb')
                data = np.array(
                    [self.generator.linex[0], self.generator.linex[1]])
                data = data.T
                somestr = "X Y1\n"
                f.write(somestr.encode('ascii'))
                np.savetxt(f, data, fmt='%.7f %.7f')
                self.write_params_to_file(f)
                f.close()

            dialog_origin.destroy()

        elif self.spectrum_choice == 5:
            dialog_origin.set_current_name(
                'vbdos_spectrum_origin_Untitled.txt')
            response = dialog_origin.run()
            if response == Gtk.ResponseType.OK:
                print("Save clicked")
                print("File selected: " + dialog_origin.get_filename())

                f = open(dialog_origin.get_filename(), 'wb')
                data = np.array(
                    [self.generator.linex[0], self.generator.linex[1]])
                data = data.T
                somestr = "X Y1\n"
                f.write(somestr.encode('ascii'))
                np.savetxt(f, data, fmt='%.7f %.7f')
                self.write_params_to_file(f)
                f.close()

            dialog_origin.destroy()

        elif self.spectrum_choice == 6:
            dialog_origin.set_current_name(
                'hh_lh_dos_spectrum_origin_Untitled.txt')
            response = dialog_origin.run()
            if response == Gtk.ResponseType.OK:
                print("Save clicked")
                print("File selected: " + dialog_origin.get_filename())

                f = open(dialog_origin.get_filename(), 'wb')
                data = np.array(
                    [self.generator.linex[0], self.generator.linex[1]])
                data = data.T
                somestr = "X Y1\n"
                f.write(somestr.encode('ascii'))
                np.savetxt(f, data, fmt='%.7f %.7f')
                self.write_params_to_file(f)
                f.close()

            dialog_origin.destroy()

        elif self.spectrum_choice == 7:
            dialog_origin.set_current_name('jdos_spectrum_origin_Untitled.txt')
            response = dialog_origin.run()
            if response == Gtk.ResponseType.OK:
                print("Save clicked")
                print("File selected: " + dialog_origin.get_filename())

                f = open(dialog_origin.get_filename(), 'wb')
                data = np.array([
                    self.generator.linex[0], self.generator.linex[1],
                    self.generator.liney[1], self.generator.linez[1]
                ])
                data = data.T
                somestr = "X Y1 Y2 Y3\n"
                f.write(somestr.encode('ascii'))
                np.savetxt(f, data, fmt='%.7f %.7f %.7f %.7f')
                self.write_params_to_file(f)
                f.close()

            dialog_origin.destroy()

    def save_graph(self, widget, data=None):
        self.spectrum_choice = self.spectrum_combobox.get_active()

        dialog_graph = Gtk.FileChooserDialog(
            "Please choose the name of a file to save", None,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE,
             Gtk.ResponseType.OK))

        if self.spectrum_choice == 1:
            dialog_graph.set_current_name(
                'absorption_spectrum_graph_Untitled.png')
        elif self.spectrum_choice == 2:
            dialog_graph.set_current_name('pl_um_spectrum_graph_Untitled.png')
        elif self.spectrum_choice == 3:
            dialog_graph.set_current_name('pl_ev_spectrum_graph_Untitled.png')
        elif self.spectrum_choice == 4:
            dialog_graph.set_current_name('cbdos_spectrum_graph_Untitled.png')
        elif self.spectrum_choice == 5:
            dialog_graph.set_current_name('vbdos_spectrum_graph_Untitled.png')
        elif self.spectrum_choice == 6:
            dialog_graph.set_current_name(
                'hh_lh_dos_spectrum_graph_Untitled.png')
        elif self.spectrum_choice == 7:
            dialog_graph.set_current_name('jdos_spectrum_graph_Untitled.png')

        response = dialog_graph.run()
        if response == Gtk.ResponseType.OK:
            print("Save clicked")
            print("File selected: " + dialog_graph.get_filename())
            self.generator.pb.savev(dialog_graph.get_filename(), "png", [], [])

        dialog_graph.destroy()

    def on_read_data_for_graph_toogled(self, widget, data=None):
        if (self.check_if_graph_your_data.get_active() == True):
            self.spectrum_choice = self.spectrum_combobox.get_active()

            dialog_own_graph_file = Gtk.FileChooserDialog(
                "Please choose file to open", None, Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN,
                 Gtk.ResponseType.OK))

            response = dialog_own_graph_file.run()
            if response == Gtk.ResponseType.OK:
                print("Open clicked")
                print("File selected: " + dialog_own_graph_file.get_filename())

            self.read_own_graph_file_name = dialog_own_graph_file.get_filename(
            )
            self.entry_readOwnFileForGraph.set_text(
                self.read_own_graph_file_name)

            dialog_own_graph_file.destroy()
        else:
            self.read_own_graph_file_name = None

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
            self.label_number_of_energy_levels.set_markup(
                "<b>" + str(txt_in_entry.count(',') + 1) + "</b>")

    def changed_cp_param(self, widget, data=None):
        txt_in_entry = self.entry_param_cp.get_text()

        if txt_in_entry == "":
            self.label_number_of_cp.set_markup("<b>0</b>")
        else:
            self.label_number_of_cp.set_markup(
                "<b>" + str(txt_in_entry.count(',') + 1) + "</b>")

    def changed_cb_param(self, widget, data=None):
        txt_in_entry = self.entry_param_cb.get_text()

        if txt_in_entry == "":
            self.label_number_of_cb.set_markup("<b>0</b>")
        else:
            self.label_number_of_cb.set_markup(
                "<b>" + str(txt_in_entry.count(',') + 1) + "</b>")

    def changed_hh_param(self, widget, data=None):
        txt_in_entry = self.entry_param_hh.get_text()

        if txt_in_entry == "":
            self.label_number_of_hh.set_markup("<b>0</b>")
        else:
            self.label_number_of_hh.set_markup(
                "<b>" + str(txt_in_entry.count(',') + 1) + "</b>")

    def changed_lh_param(self, widget, data=None):
        txt_in_entry = self.entry_param_lh.get_text()

        if txt_in_entry == "":
            self.label_number_of_lh.set_markup("<b>0</b>")
        else:
            self.label_number_of_lh.set_markup(
                "<b>" + str(txt_in_entry.count(',') + 1) + "</b>")

    def changed_wsk_param(self, widget, data=None):
        txt_in_entry = self.entry_param_wsk.get_text()

        if txt_in_entry == "":
            self.label_number_of_wsk.set_markup("<b>0</b>")
        else:
            self.label_number_of_wsk.set_markup(
                "<b>" + str(txt_in_entry.count(',') + 1) + "</b>")

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

    def create_labels(self):
        # SECTIONS:

        # Simulation parameters
        self.label_param_a0 = Gtk.Label("A0")
        self.label_param_g0 = Gtk.Label("g0")
        self.label_param_emin = Gtk.Label("E min [eV]")
        self.label_param_emax = Gtk.Label("E max [eV]")
        self.label_param_edn = Gtk.Label("E step [eV]")
        self.label_param_ecmin = Gtk.Label("Ec min [eV]")
        self.label_param_ecmax = Gtk.Label("Ec max [eV]")
        self.label_param_ecdn = Gtk.Label("Ec step [eV]")
        self.label_param_evmin = Gtk.Label("Ev min [eV]")
        self.label_param_evmax = Gtk.Label("Ev max [eV]")
        self.label_param_evdn = Gtk.Label("Ev step [eV]")
        self.label_param_T = Gtk.Label("T [K]")
        self.label_param_gamma = Gtk.Label("Gamma peak [eV]")
        self.label_param_step_func_gamma = Gtk.Label("Gamma Step [eV]")

        # Parameters of the structure
        self.label_param_cp = Gtk.Label("CP")
        self.label_param_cb = Gtk.Label("CB [eV]")
        self.label_param_hh = Gtk.Label("HH [eV]")
        self.label_param_lh = Gtk.Label("LH [eV]")
        self.label_param_wsk = Gtk.Label("wsk")
        self.label_param_eg = Gtk.Label("Eg [eV]")
        self.label_param_ef = Gtk.Label("Ef [eV]")
        self.label_param_en = Gtk.Label("En [eV]")

        # Effective masses section
        self.label_param_mee = Gtk.Label("mee")
        self.label_param_mehh = Gtk.Label("mehh")
        self.label_param_melh = Gtk.Label("melh")
        # Others
        self.label_energy_levels = Gtk.Label("Nb")
        self.label_number_of_energy_levels = Gtk.Label("0")
        self.label_number_of_cp = Gtk.Label("0")
        self.label_number_of_cb = Gtk.Label("0")
        self.label_number_of_hh = Gtk.Label("0")
        self.label_number_of_lh = Gtk.Label("0")
        self.label_number_of_wsk = Gtk.Label("0")
        self.label_emass_pick = Gtk.Label(
            "Pick values for specific sc compound: ")

    def set_width_chars_for_entries(self):
        self.entry_param_T.set_width_chars(6)
        self.entry_param_gamma.set_width_chars(6)
        self.entry_param_step_func_gamma.set_width_chars(6)
        self.entry_param_mee.set_width_chars(6)
        self.entry_param_mehh.set_width_chars(6)
        self.entry_param_melh.set_width_chars(6)
        self.entry_param_evmin.set_width_chars(4)
        self.entry_param_evmax.set_width_chars(4)
        self.entry_param_evdn.set_width_chars(4)
        self.entry_param_cp.set_width_chars(14)
        self.entry_param_hh.set_width_chars(14)
        self.entry_param_cb.set_width_chars(14)
        self.entry_param_wsk.set_width_chars(14)
        self.entry_param_lh.set_width_chars(14)
        self.entry_param_a0.set_width_chars(6)
        self.entry_param_g0.set_width_chars(6)
        self.entry_param_eg.set_width_chars(6)
        self.entry_param_ef.set_width_chars(6)
        self.entry_param_en.set_width_chars(6)
        self.entry_param_emin.set_width_chars(4)
        self.entry_param_emax.set_width_chars(4)
        self.entry_param_edn.set_width_chars(4)
        self.entry_param_ecmax.set_width_chars(4)
        self.entry_param_ecmin.set_width_chars(4)
        self.entry_param_ecdn.set_width_chars(4)

    def create_entries(self):
        # SECTIONS:

        # Simulation parameters
        self.entry_param_a0 = Gtk.Entry()
        self.entry_param_g0 = Gtk.Entry()
        self.entry_param_eg = Gtk.Entry()
        self.entry_param_ef = Gtk.Entry()
        self.entry_param_en = Gtk.Entry()
        self.entry_param_emin = Gtk.Entry()
        self.entry_param_emax = Gtk.Entry()
        self.entry_param_edn = Gtk.Entry()
        self.entry_param_ecmin = Gtk.Entry()
        self.entry_param_ecmax = Gtk.Entry()
        self.entry_param_ecdn = Gtk.Entry()
        self.entry_param_evmin = Gtk.Entry()
        self.entry_param_evmax = Gtk.Entry()
        self.entry_param_evdn = Gtk.Entry()

        # Parameters of the structure
        self.entry_param_cp = Gtk.Entry()
        self.entry_param_cb = Gtk.Entry()
        self.entry_param_hh = Gtk.Entry()
        self.entry_param_lh = Gtk.Entry()
        self.entry_param_wsk = Gtk.Entry()
        self.entry_param_T = Gtk.Entry()
        self.entry_param_gamma = Gtk.Entry()
        self.entry_param_step_func_gamma = Gtk.Entry()

        # Effective masses section
        self.entry_param_mee = Gtk.Entry()
        self.entry_param_mehh = Gtk.Entry()
        self.entry_param_melh = Gtk.Entry()

    def set_labels_alignment(self):
        # SECTIONS:

        # Simulation parameters
        self.label_param_a0.set_xalign(1)
        self.label_param_g0.set_xalign(1)
        self.label_param_T.set_xalign(1)
        self.label_param_gamma.set_xalign(1)
        self.label_param_step_func_gamma.set_xalign(1)
        self.label_param_emin.set_xalign(1)
        self.label_param_emax.set_xalign(1)
        self.label_param_edn.set_xalign(1)
        self.label_param_ecmin.set_xalign(1)
        self.label_param_ecmax.set_xalign(1)
        self.label_param_ecdn.set_xalign(1)
        self.label_param_evmin.set_xalign(1)
        self.label_param_evmax.set_xalign(1)
        self.label_param_evdn.set_xalign(1)

        # Parameters of the structure
        self.label_param_eg.set_xalign(1)
        self.label_param_ef.set_xalign(1)
        self.label_param_en.set_xalign(1)
        self.label_param_cp.set_xalign(1)
        self.label_param_cb.set_xalign(1)
        self.label_param_hh.set_xalign(1)
        self.label_param_lh.set_xalign(1)
        self.label_param_wsk.set_xalign(1)

        # Effective masses section
        self.label_param_mee.set_xalign(1)
        self.label_param_mehh.set_xalign(1)
        self.label_param_melh.set_xalign(1)

        # Others
        self.label_emass_pick.set_xalign(0.5)
        self.label_energy_levels.set_xalign(1)
        self.label_number_of_energy_levels.set_xalign(0.5)
        self.label_number_of_cp.set_xalign(0.5)
        self.label_number_of_cb.set_xalign(0.5)
        self.label_number_of_hh.set_xalign(0.5)
        self.label_number_of_lh.set_xalign(0.5)
        self.label_number_of_wsk.set_xalign(0.5)

    def create_notebook_page_ABOUT(self):
        self.box_page_about = Gtk.Grid()
        self.box_page_about.set_row_spacing(20)
        self.label_about = Gtk.Label('About')
        self.label_about.set_markup("<span font='30'><b>About</b></span>")
        self.label_about.set_margin_left(150)
        self.label_authors = Gtk.Label('Authors')
        self.label_authors.set_markup("<span font='26'><b>Authors</b></span>")
        self.label_authors.set_margin_left(150)
        self.label_authors_text = Gtk.Label(justify=Gtk.Justification.CENTER)
        self.label_authors_text.set_margin_left(240)
        self.label_authors_text.set_xalign(0)
        self.label_authors_text.set_markup(
            "<span font='12'> <b>Piotr Ruszala</b>, '204185@student.pwr.edu.pl', (Physics)           <b>Pawel Sikora</b> 'sikor6@gmail.com', (Interface, pyGtk) </span>"
        )
        self.label_about_text = Gtk.Label(justify=Gtk.Justification.CENTER)
        self.label_about_text.set_xalign(0)
        self.label_about_text.set_margin_left(150)
        self.label_about_text.set_markup(
            "<span font='12'>\n<b>'PLspectrum'</b> is a python script for calculating   \
and generating graphs of a photoluminescence \
spectrum. \n Script is able to generate the ideal \
characteristics and compare them with measured \
data when provided and draw it on single graph.\n\n \
All with pyGTK and using GTK3+.</span>")
        self.logo_about = Gtk.Image.new_from_file('logo_about.png')
        self.frame_logo = Gtk.Frame()
        self.frame_logo.set_margin_left(150)
        self.frame_logo.set_shadow_type(Gtk.ShadowType.NONE)
        self.frame_logo.add(self.logo_about)
        self.box_page_about.add(self.label_about)

        self.box_page_about.attach_next_to(self.frame_logo, self.label_about,
                                           Gtk.PositionType.BOTTOM, 1, 1)
        self.box_page_about.attach_next_to(self.label_about_text,
                                           self.frame_logo,
                                           Gtk.PositionType.BOTTOM, 1, 1)
        self.box_page_about.attach_next_to(self.label_authors,
                                           self.label_about_text,
                                           Gtk.PositionType.BOTTOM, 1, 1)
        self.box_page_about.attach_next_to(self.label_authors_text,
                                           self.label_authors,
                                           Gtk.PositionType.BOTTOM, 1, 1)

        self.notebook.append_page(self.box_page_about, Gtk.Label('About'))

    def create_notebook_page_HELP(self):
        self.box_page_help = Gtk.Grid()
        self.box_page_help.add(Gtk.Label('Help, TBD'))
        self.notebook.append_page(self.box_page_help, Gtk.Label('Help'))

    def store_entries_in_list(self):
        list_store.append([0, "Entry,a0", self.entry_param_a0, "a0"])
        list_store.append([1, "Entry,g0", self.entry_param_g0, "g0"])
        list_store.append([2, "Entry,eg", self.entry_param_eg, "Eg [eV]"])
        list_store.append([3, "Entry,ef", self.entry_param_ef, "Ef [eV]"])
        list_store.append([4, "Entry,en", self.entry_param_en, "En [eV]"])
        list_store.append(
            [5, "Entry,emin", self.entry_param_emin, "Emin [eV]"])
        list_store.append(
            [6, "Entry,emax", self.entry_param_emax, "Emax [eV]"])
        list_store.append([7, "Entry,edn", self.entry_param_edn, "Estep [eV]"])
        list_store.append(
            [8, "Entry,ecmin", self.entry_param_ecmin, "Ec min [eV]"])
        list_store.append(
            [9, "Entry,ecmax", self.entry_param_ecmax, "Ec max [eV]"])
        list_store.append(
            [10, "Entry,ecdn", self.entry_param_ecdn, "Ec step [eV]"])
        list_store.append(
            [11, "Entry,evmin", self.entry_param_evmin, "Ev min [eV]"])
        list_store.append(
            [12, "Entry,evmax", self.entry_param_evmax, "Ev max [eV]"])
        list_store.append(
            [13, "Entry,evdn", self.entry_param_evdn, "Ev step [eV]"])
        list_store.append([14, "Entry,cp", self.entry_param_cp, "CP"])
        list_store.append([15, "Entry,cb", self.entry_param_cb, "CB [eV]"])
        list_store.append([16, "Entry,hh", self.entry_param_hh, "HH [eV]"])
        list_store.append([17, "Entry,lh", self.entry_param_lh, "LH [eV]"])
        list_store.append([18, "Entry,wsk", self.entry_param_wsk, "WSK"])
        list_store.append([19, "Entry,T", self.entry_param_T, "T [K]"])
        list_store.append(
            [20, "Entry,gamma", self.entry_param_gamma, "Gamma Peak [eV]"])
        list_store.append([
            21, "Entry,step_func_gamma", self.entry_param_step_func_gamma,
            "Gamma step [eV]"
        ])
        list_store.append([22, "Entry,me", self.entry_param_mee, "Me"])
        list_store.append([23, "Entry,mehh", self.entry_param_mehh, "Mehh"])
        list_store.append([24, "Entry,melh", self.entry_param_melh, "Melh"])

    def create_notebook_page_MAIN(self):
        self.grid_page_main = Gtk.Grid()
        self.grid_page_main.set_column_spacing(30)
        self.grid_page_main.set_row_spacing(20)
        self.grid_page_main.set_margin_top(10)
        self.grid_page_main.set_margin_bottom(10)
        self.grid_page_main.set_margin_left(10)
        self.grid_page_main.set_margin_right(10)
        self.grid_page_main.set_column_spacing(10)

        self.notebook.append_page(self.grid_page_main,
                                  Gtk.Label('Graph generator'))

        # frame energy
        self.frame_energy = Gtk.Frame(
            label="Parameters of the electronic structure")
        self.frame_energy.set_label_align(0.5, 0.5)
        self.grid_energy = Gtk.Grid()
        self.grid_energy.set_margin_top(10)
        self.grid_energy.set_margin_left(10)
        self.grid_energy.set_margin_right(10)
        self.grid_energy.set_row_spacing(20)
        self.grid_energy.set_column_spacing(10)
        self.frame_energy.add(self.grid_energy)

        # entries for energy frame
        self.entry_param_eg.set_width_chars(5)
        self.entry_param_en.connect("changed", self.changed_energy_levels,
                                    None)
        self.entry_param_cp.connect("changed", self.changed_cp_param, None)
        self.entry_param_cb.connect("changed", self.changed_cb_param, None)
        self.entry_param_hh.connect("changed", self.changed_hh_param, None)
        self.entry_param_lh.connect("changed", self.changed_lh_param, None)
        self.entry_param_wsk.connect("changed", self.changed_wsk_param, None)
        self.label_number_of_energy_levels.set_markup("<b>0</b>")
        self.label_number_of_cp.set_markup("<b>0</b>")
        self.label_number_of_cb.set_markup("<b>0</b>")
        self.label_number_of_hh.set_markup("<b>0</b>")
        self.label_number_of_lh.set_markup("<b>0</b>")
        self.label_number_of_wsk.set_markup("<b>0</b>")
        self.grid_energy.attach(self.label_energy_levels, 4, 0, 1, 1)
        self.grid_energy.attach(self.label_number_of_energy_levels, 4, 1, 1, 1)
        self.grid_energy.attach(self.label_param_en, 0, 1, 1, 1)
        self.grid_energy.attach(self.label_param_eg, 0, 5, 1, 1)
        self.grid_energy.attach(self.label_param_ef, 0, 6, 1, 1)
        self.grid_energy.attach(self.label_param_cp, 0, 7, 1, 1)
        self.grid_energy.attach(self.label_param_cb, 0, 8, 1, 1)
        self.grid_energy.attach(self.label_param_hh, 0, 9, 1, 1)
        self.grid_energy.attach(self.label_param_lh, 0, 10, 1, 1)
        self.grid_energy.attach(self.label_param_wsk, 0, 11, 1, 1)
        self.grid_energy.attach(self.entry_param_en, 1, 1, 3, 1)
        self.grid_energy.attach(self.entry_param_eg, 1, 5, 1, 1)
        self.grid_energy.attach(self.entry_param_ef, 1, 6, 1, 1)
        self.grid_energy.attach(self.entry_param_cp, 1, 7, 3, 1)
        self.grid_energy.attach(self.entry_param_cb, 1, 8, 3, 1)
        self.grid_energy.attach(self.entry_param_hh, 1, 9, 3, 1)
        self.grid_energy.attach(self.entry_param_lh, 1, 10, 3, 1)
        self.grid_energy.attach(self.entry_param_wsk, 1, 11, 3, 1)
        self.grid_energy.attach(self.label_number_of_cp, 4, 7, 1, 1)
        self.grid_energy.attach(self.label_number_of_cb, 4, 8, 1, 1)
        self.grid_energy.attach(self.label_number_of_hh, 4, 9, 1, 1)
        self.grid_energy.attach(self.label_number_of_lh, 4, 10, 1, 1)
        self.grid_energy.attach(self.label_number_of_wsk, 4, 11, 1, 1)

        # frame electron mass
        self.frame_emass = Gtk.Frame(label="Effective masses")
        self.frame_emass.set_label_align(0.5, 0.5)
        self.grid_emass = Gtk.Grid()
        self.grid_emass.set_margin_left(10)
        self.grid_emass.set_margin_right(10)
        self.grid_emass.set_margin_top(10)
        self.grid_emass.set_margin_bottom(10)
        self.grid_energy.set_margin_top(10)
        self.grid_emass.set_row_spacing(20)
        self.grid_emass.set_column_spacing(10)
        self.frame_emass.add(self.grid_emass)

        self.grid_emass.attach(self.label_param_mee, 0, 0, 1, 1)
        self.grid_emass.attach(self.entry_param_mee, 1, 0, 1, 1)
        self.grid_emass.attach(self.label_param_mehh, 2, 0, 1, 1)
        self.grid_emass.attach(self.entry_param_mehh, 3, 0, 1, 1)
        self.grid_emass.attach(self.label_param_melh, 4, 0, 1, 1)
        self.grid_emass.attach(self.entry_param_melh, 5, 0, 1, 1)

        # main buttons/entries
        self.button1 = Gtk.Button('Generate graph!')
        self.buttonExportToOrigin = Gtk.Button('Export data to txt')
        self.buttonExportToOrigin.connect("clicked", self.save_to_origin, None)
        self.buttonSaveImage = Gtk.Button('Save Graph')

        self.buttonSaveParams = Gtk.Button()
        self.buttonSaveParams.set_always_show_image(True)
        self.image_save_stock = Gtk.Image()
        self.image_save_stock.set_from_stock(Gtk.STOCK_SAVE_AS,
                                             Gtk.IconSize.BUTTON)
        self.buttonSaveParams.set_image(self.image_save_stock)
        self.buttonSaveParams.set_image_position(Gtk.PositionType.RIGHT)
        self.buttonSaveParams.set_label("Save parameters       ")

        self.check_if_graph_your_data = Gtk.CheckButton(
            "Draw own data on graph")
        self.entry_readOwnFileForGraph = Gtk.Entry()

        # combobox for choosing spectrum
        spectrum_store = Gtk.ListStore(int, str)
        spectrum_store.append([1, "--- Choose spectrum ---"])
        spectrum_store.append([11, "Absorption"])
        spectrum_store.append([12, "Emission [um]"])
        spectrum_store.append([13, "Emission [eV]"])
        spectrum_store.append([21, "CB DOS"])
        spectrum_store.append([22, "VB DOS"])
        spectrum_store.append([23, "HH and LH DOS"])
        spectrum_store.append([3, "JDOS"])
        self.spectrum_combobox = Gtk.ComboBox.new_with_model_and_entry(
            spectrum_store)
        self.spectrum_combobox.connect("changed",
                                       self.on_spectrum_combo_changed)
        self.spectrum_combobox.set_entry_text_column(1)
        self.spectrum_combobox.set_active(0)

        # combobox for choosing compound
        compound_store = Gtk.ListStore(int, str)
        compound_store.append([1, "--- Custom ---"])
        compound_store.append([11, "GaAs"])
        compound_store.append([12, "InAs"])
        compound_store.append([2, "GaInAs"])
        self.compound_combobox = Gtk.ComboBox.new_with_model_and_entry(
            compound_store)
        self.compound_combobox.connect("changed",
                                       self.on_compound_combo_changed)
        self.compound_combobox.set_entry_text_column(1)
        self.compound_combobox.set_active(0)

        # add initial image for the graph frame
        self.frame1 = Gtk.Frame(label="Graph")
        self.frame1.set_label_align(0.5, 0.5)
        self.initGraph = Gtk.Image.new_from_file('init_frame_image.png')
        self.currentGraph = self.initGraph
        self.frame1.add(self.currentGraph)

        # events
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.button1.connect("clicked", self.generate_graph, None)
        self.buttonSaveImage.connect("clicked", self.save_graph, None)
        self.check_if_graph_your_data.connect(
            "toggled", self.on_read_data_for_graph_toogled, None)

        # Simulation parameters
        self.frame_simulation_params = Gtk.Frame(label="Simulation parameters")
        self.frame_simulation_params.set_label_align(0.5, 0.5)
        self.grid_simulation_params = Gtk.Grid()
        self.grid_simulation_params.set_margin_top(20)
        self.grid_simulation_params.set_margin_bottom(10)
        self.grid_simulation_params.set_margin_left(10)
        self.grid_simulation_params.set_margin_right(10)
        self.grid_simulation_params.set_row_spacing(40)
        self.grid_simulation_params.set_column_spacing(10)
        self.frame_simulation_params.add(self.grid_simulation_params)

        self.grid_simulation_params.attach(self.label_param_gamma, 0, 1, 1, 1)
        self.grid_simulation_params.attach(self.entry_param_gamma, 1, 1, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.label_param_step_func_gamma, self.entry_param_gamma,
            Gtk.PositionType.RIGHT, 2, 1)
        self.grid_simulation_params.attach_next_to(
            self.entry_param_step_func_gamma, self.label_param_step_func_gamma,
            Gtk.PositionType.RIGHT, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.label_param_T, self.label_param_gamma,
            Gtk.PositionType.BOTTOM, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.entry_param_T, self.label_param_T, Gtk.PositionType.RIGHT, 1,
            1)
        self.grid_simulation_params.attach_next_to(
            self.label_param_a0, self.label_param_step_func_gamma,
            Gtk.PositionType.BOTTOM, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.entry_param_a0, self.label_param_a0, Gtk.PositionType.RIGHT,
            1, 1)
        self.grid_simulation_params.attach_next_to(
            self.label_param_g0, self.entry_param_a0, Gtk.PositionType.RIGHT,
            1, 1)
        self.grid_simulation_params.attach_next_to(
            self.entry_param_g0, self.label_param_g0, Gtk.PositionType.RIGHT,
            1, 1)
        self.grid_simulation_params.attach_next_to(
            self.label_param_emin, self.label_param_T, Gtk.PositionType.BOTTOM,
            1, 1)
        self.grid_simulation_params.attach_next_to(
            self.label_param_emax, self.label_param_emin,
            Gtk.PositionType.BOTTOM, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.label_param_edn, self.label_param_emax,
            Gtk.PositionType.BOTTOM, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.entry_param_emin, self.label_param_emin,
            Gtk.PositionType.RIGHT, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.label_param_ecmin, self.entry_param_emin,
            Gtk.PositionType.RIGHT, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.entry_param_ecmin, self.label_param_ecmin,
            Gtk.PositionType.RIGHT, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.entry_param_emax, self.entry_param_emin,
            Gtk.PositionType.BOTTOM, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.label_param_ecmax, self.entry_param_emax,
            Gtk.PositionType.RIGHT, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.entry_param_ecmax, self.label_param_ecmax,
            Gtk.PositionType.RIGHT, 1, 1)

        self.grid_simulation_params.attach_next_to(
            self.entry_param_edn, self.entry_param_emax,
            Gtk.PositionType.BOTTOM, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.label_param_evmin, self.entry_param_ecmin,
            Gtk.PositionType.RIGHT, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.entry_param_evmin, self.label_param_evmin,
            Gtk.PositionType.RIGHT, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.label_param_evmax, self.entry_param_ecmax,
            Gtk.PositionType.RIGHT, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.entry_param_evmax, self.label_param_evmax,
            Gtk.PositionType.RIGHT, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.label_param_ecdn, self.entry_param_edn,
            Gtk.PositionType.RIGHT, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.entry_param_ecdn, self.label_param_ecdn,
            Gtk.PositionType.RIGHT, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.label_param_evdn, self.entry_param_ecdn,
            Gtk.PositionType.RIGHT, 1, 1)
        self.grid_simulation_params.attach_next_to(
            self.entry_param_evdn, self.label_param_evdn,
            Gtk.PositionType.RIGHT, 1, 1)

        # frames
        self.grid_page_main.attach(self.frame_simulation_params, 0, 0, 2, 8)
        self.grid_page_main.attach(self.frame_energy, 2, 0, 1, 8)
        self.grid_page_main.attach(self.frame_emass, 0, 8, 1, 3)
        self.grid_page_main.attach(self.frame1, 7, 0, 4, 7)

        # main functionality
        self.grid_page_main.attach(self.button1, 8, 9, 2, 1)
        self.grid_page_main.attach_next_to(self.buttonExportToOrigin,
                                           self.button1, Gtk.PositionType.TOP,
                                           1, 1)
        self.grid_page_main.attach_next_to(self.buttonSaveImage,
                                           self.buttonExportToOrigin,
                                           Gtk.PositionType.RIGHT, 1, 1)
        self.grid_page_main.attach_next_to(
            self.spectrum_combobox, self.button1, Gtk.PositionType.LEFT, 1, 1)
        self.grid_page_main.attach_next_to(self.entry_readOwnFileForGraph,
                                           self.buttonExportToOrigin,
                                           Gtk.PositionType.TOP, 1, 1)
        self.grid_page_main.attach_next_to(self.check_if_graph_your_data,
                                           self.entry_readOwnFileForGraph,
                                           Gtk.PositionType.LEFT, 1, 1)

    def check_if_strings_in_entries_are_valid(self):
        self.empty_cnt = 0
        self.not_a_number_cnt = 0

        for row in list_store:
            entry = list_store.get_value(row.iter, 2)

            gt = entry.get_text()

            if gt == "" or gt == "0":
                self.empty_cnt += 1

            es = list_store.get_value(row.iter, 1)

            if es != "Entry,en" and es != "Entry,cp" and es != "Entry,hh" and es != "Entry,lh" \
               and es != "Entry,wsk" and es != "Entry,cb":
                try:
                    tmp = float(gt)
                except ValueError:
                    self.not_a_number_cnt += 1
                    print("'" + list_store.get_value(row.iter, 1) + "'" +
                          " is not a number!")

        if self.empty_cnt != 0:
            dialog1 = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                                        Gtk.ButtonsType.OK,
                                        "Values can't be empty/zero!")
            dialog1.format_secondary_text(
                "Some of your entries for parameters appears to be empty/zero. Please check it and type again"
            )
            dialog1.run()
            dialog1.destroy()

            return -1

        if self.not_a_number_cnt != 0:
            dialog1 = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                                        Gtk.ButtonsType.OK,
                                        "Values can't be string!")
            dialog1.format_secondary_text(
                "Some of your entries are not a number. Please check it and type again"
            )
            dialog1.run()
            dialog1.destroy()

            return -1

    def fill_entries_for_debug(self):
        self.entry_param_en.set_text("1")
        self.entry_param_a0.set_text("4")
        self.entry_param_g0.set_text("5")
        self.entry_param_eg.set_text("4")
        self.entry_param_ef.set_text("2")
        self.entry_param_en.set_text("1,1,1,1")
        self.entry_param_emin.set_text("1")
        self.entry_param_emax.set_text("2")
        self.entry_param_edn.set_text("0.1")
        self.entry_param_ecmin.set_text("1")
        self.entry_param_ecmax.set_text("2")
        self.entry_param_ecdn.set_text("0.1")
        self.entry_param_evmin.set_text("1")
        self.entry_param_evmax.set_text("2")
        self.entry_param_evdn.set_text("0.1")

        # Parameters of the structure
        self.entry_param_cp.set_text("1,1,1,1")
        self.entry_param_cb.set_text("1,1,1,1")
        self.entry_param_hh.set_text("1,1,1,1")
        self.entry_param_lh.set_text("1,1,1,1")
        self.entry_param_wsk.set_text("h,h,h,h")
        self.entry_param_T.set_text("270")
        self.entry_param_gamma.set_text("5")
        self.entry_param_step_func_gamma.set_text("0.1")

        # Effective masses section
        self.entry_param_mee.set_text("4")
        self.entry_param_mehh.set_text("4")
        self.entry_param_melh.set_text("4")

    def get_strings_from_entries_and_update_params(self):
        self.calculator.params.En = np.fromstring(
            self.entry_param_en.get_text(), dtype=float, sep=',')
        self.calculator.params.CP = np.fromstring(
            self.entry_param_cp.get_text(), dtype=float, sep=',')
        self.calculator.params.CB = np.fromstring(
            self.entry_param_cb.get_text(), dtype=float, sep=',')
        self.calculator.params.HH = np.fromstring(
            self.entry_param_hh.get_text(), dtype=float, sep=',')
        self.calculator.params.LH = np.fromstring(
            self.entry_param_lh.get_text(), dtype=float, sep=',')
        self.calculator.params.wsk = np.array(
            list(self.entry_param_wsk.get_text().split(',')))

        self.calculator.params.A0 = float(self.entry_param_a0.get_text())
        self.calculator.params.g0 = float(self.entry_param_g0.get_text())
        self.calculator.params.Eg = float(self.entry_param_eg.get_text())
        self.calculator.params.Ef = float(self.entry_param_ef.get_text())
        self.calculator.params.E = np.arange(
            float(self.entry_param_emin.get_text()),
            float(self.entry_param_emax.get_text()),
            float(self.entry_param_edn.get_text()))
        self.calculator.params.Ec = np.arange(
            float(self.entry_param_ecmin.get_text()),
            float(self.entry_param_ecmax.get_text()),
            float(self.entry_param_ecdn.get_text()))
        self.calculator.params.Ev = np.arange(
            float(self.entry_param_evmin.get_text()),
            float(self.entry_param_evmax.get_text()),
            float(self.entry_param_evdn.get_text()))
        self.calculator.params.T = float(self.entry_param_T.get_text())
        self.calculator.params.gamma = float(self.entry_param_gamma.get_text())
        self.calculator.params.step_func_gamma = float(
            self.entry_param_step_func_gamma.get_text())
        self.calculator.params.me = float(self.entry_param_mee.get_text())
        self.calculator.params.mehh = float(self.entry_param_mehh.get_text())
        self.calculator.params.melh = float(self.entry_param_melh.get_text())

        self.calculator.params.LAMBDA = (1.24 / self.calculator.params.E)

    def generate_plot_of_choice(self, sc):
        if sc == 1:
            self.generator.plot_widmo_absorption(
                self.calculator.params.E,
                self.calculator.Abs1,
                self.calculator.Abs2,
                self.calculator.Abs3,
            )
            self.currentGraph = self.generator.generated_absorption
        elif sc == 2:
            self.generator.plot_widmo_pl_um(self.calculator.Widmo1,
                                            self.calculator.Widmo2,
                                            self.calculator.params.LAMBDA)
            self.currentGraph = self.generator.generated_pl_um
        elif sc == 3:
            self.generator.plot_widmo_pl_ev(
                self.calculator.Widmo1,
                self.calculator.Widmo2,
                self.calculator.params.LAMBDA,
            )
            self.currentGraph = self.generator.generated_pl_ev
        elif sc == 4:
            self.generator.plot_widmo_cbdos(self.calculator.params.Ec,
                                            self.calculator.params.Ev,
                                            self.calculator.dosCB)
            self.currentGraph = self.generator.generated_cbdos
        elif sc == 5:
            self.generator.plot_widmo_vbdos(self.calculator.params.Ev,
                                            self.calculator.dosVB)
            self.currentGraph = self.generator.generated_vbdos
        elif sc == 6:
            self.generator.plot_widmo_hh_lh_dos(
                self.calculator.params.Ev,
                self.calculator.dosHH,
                self.calculator.dosLH,
            )
            self.currentGraph = self.generator.generated_hh_lh_dos
        elif sc == 7:
            self.generator.plot_widmo_jdos(
                self.calculator.JDOS,
                self.calculator.JDOS2,
                self.calculator.Hevisajd,
            )
            self.currentGraph = self.generator.generated_jdos
        else:
            dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "Wrong choice!")
            dialog.format_secondary_text(
                "You have not chosen any spectrum to generate. Please choose one and try again"
            )
            dialog.run()
            dialog.destroy()
