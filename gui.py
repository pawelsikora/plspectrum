from gi import pygtkcompat
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

pygtkcompat.enable()
pygtkcompat.enable_gtk(version='3.0')

import gtk

from QSpectrum import Spectrum_generator
class DialogExample(gtk.Dialog):

    def __init__(self, parent):
        gtk.Dialog.__init__(self, "My Dialog", parent, 0,
            (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
             gtk.STOCK_OK, gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = gtk.Label("This is a dialog to display additional information")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class GUI:

    def generate_graph(self, widget, data=None):

        self.c = Spectrum_generator()
        self.c.params.A0 = float(self.entry_param_a0.get_text())
        self.c.params.g0 = float(self.entry_param_g0.get_text())
        self.c.params.Eg = float(self.entry_param_eg.get_text())
        self.c.params.T = float(self.entry_param_T.get_text())
        self.c.params.gamma = float(self.entry_param_gamma.get_text())
        self.c.params.gamma_schodek = float(self.entry_param_gamma_schodek.get_text())
        if (self.c.params.A0) == 0 or self.c.params.g0  == 0 or \
           self.c.params.Eg == 0 or self.c.params.T == 0 or \
           self.c.params.gamma == 0 or self.c.params.gamma_schodek == 0:
              print("some value is 0!")
              dialog1 = gtk.MessageDialog(None, 0, gtk.MessageType.INFO,
                  gtk.ButtonsType.OK, "Values can't be zero!")
              dialog1.format_secondary_text(
                  "some of your values appears to be empty. Please check it and type again")
              dialog1.run()
              dialog1.destroy()

        self.spectrum_choice = self.spectrum_combobox.get_active()

        if self.spectrum_choice == 1:
           self.frame1.remove(self.currentGraph)
           self.c.calculate_all()
           self.c.plot_widmo_alfa()
           self.currentGraph = self.c.generated_alfa
        elif self.spectrum_choice == 2:
           self.frame1.remove(self.currentGraph)
           self.c = Spectrum_generator()
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
           self.c.save_to_files("widmo_alfa", "lambda_alfa")
        elif self.spectrum_choice == 2:
           self.c.save_to_files("widmo_beta", "lambda_beta")
        dialog3 = gtk.FileChooserDialog("Please choose a file", None,
            gtk.FileChooserAction.SAVE,
            (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
             gtk.STOCK_OPEN, gtk.ResponseType.OK))

        response = dialog3.run()
        if response == gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog3.get_filename())

        dialog3.destroy()


    def delete_event(self, widget, event, data=None):
        print("delete event occurred")
        return False

    def destroy(self, widget, data=None):
        print("destroy signal occurred")
        gtk.main_quit()

    def on_spectrum_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            print("Selected: ID=%d, name=%s" % (row_id, name))
        else:
            entry = combo.get_child()
            print("Entered: %s" % entry.get_text())

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(1024, 450)
        self.window.set_icon_from_file('icon.png')
        self.grid = gtk.Grid()

        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(10)
        self.window.add(self.grid)

        self.initGraph = gtk.Image.new_from_file('plot_alfa.png')
        self.currentGraph = self.initGraph

        spectrum_store = gtk.ListStore(int, str)
        spectrum_store.append([1, "--- Choose spectrum ---"])
        spectrum_store.append([11, "Widmo alfa"])
        spectrum_store.append([12, "Widmo beta"])
        spectrum_store.append([2, "Widmo gamma"])
        self.spectrum_combobox = gtk.ComboBox.new_with_model_and_entry(spectrum_store)
        self.spectrum_combobox.connect("changed", self.on_spectrum_combo_changed)
        self.spectrum_combobox.set_entry_text_column(1)
        self.spectrum_combobox.set_active(0)

        self.frame1 = gtk.Frame(label="Graph")
        self.frame1.set_label_align(0.5, 0.5)
        self.frame1.add(self.currentGraph)
        self.label_param_a0 = gtk.Label("A0")
        self.label_param_g0 = gtk.Label("g0")
        self.label_param_eg = gtk.Label("Eg")
        self.label_param_T = gtk.Label("T")
        self.label_param_gamma = gtk.Label("Gamma")
        self.label_param_gamma_schodek = gtk.Label("Gamma schodek")
        self.label_param_meh = gtk.Label("meh")

        self.label_param_a0.set_xalign(1)
        self.label_param_g0.set_xalign(1)
        self.label_param_eg.set_xalign(1)
        self.label_param_T.set_xalign(1)
        self.label_param_gamma.set_xalign(1)
        self.label_param_gamma_schodek.set_xalign(1)
        self.label_param_meh.set_xalign(1)

        self.entry_param_a0 = gtk.Entry()
        self.entry_param_g0 = gtk.Entry()
        self.entry_param_eg = gtk.Entry()
        self.entry_param_T = gtk.Entry()
        self.entry_param_gamma = gtk.Entry()
        self.entry_param_gamma_schodek = gtk.Entry()
        self.entry_param_meh = gtk.Entry()

        self.button1 = gtk.Button('Generate graph!')
        self.buttonExportToOrigin = gtk.Button('Export data to txt')
        self.buttonExportToOrigin.connect("clicked", self.save_to_origin, None)
        self.buttonSaveImage = gtk.Button('Save Graph')

        self.button5 = gtk.Button()

        self.button2 = gtk.Button('Save graph')

        self.button3 = gtk.Button('Compare two graphs')

        self.window.connect("delete_event", self.delete_event)

        self.window.connect("destroy", self.destroy)

        self.window.set_border_width(30)

        self.button1.connect("clicked", self.generate_graph, None)

        self.grid.attach(self.label_param_a0, 0, 2, 1, 1)
        self.grid.attach_next_to(self.label_param_g0, self.label_param_a0, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.label_param_eg, self.label_param_g0, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.label_param_T, self.label_param_eg, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.label_param_gamma, self.label_param_T, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.label_param_gamma_schodek, self.label_param_gamma, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.label_param_meh, self.label_param_gamma_schodek, gtk.PositionType.BOTTOM, 1, 1)

        self.grid.attach(self.entry_param_a0, 1, 2, 1, 1)
        self.grid.attach_next_to(self.entry_param_g0, self.entry_param_a0, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_param_eg, self.entry_param_g0, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_param_T, self.entry_param_eg, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_param_gamma, self.entry_param_T, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_param_gamma_schodek, self.entry_param_gamma, gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entry_param_meh, self.entry_param_gamma_schodek, gtk.PositionType.BOTTOM, 1, 1)

        self.grid.attach(self.frame1, 3, 0, 6, 14)
        self.grid.attach(self.button1, 6, 15, 3, 1)
        self.grid.attach_next_to(self.buttonExportToOrigin, self.button1, gtk.PositionType.TOP, 1, 1)
        self.grid.attach_next_to(self.buttonSaveImage, self.buttonExportToOrigin, gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(self.spectrum_combobox, self.buttonExportToOrigin, gtk.PositionType.LEFT, 1, 1)

        self.window.show_all()

    def main(self):
        gtk.main()
