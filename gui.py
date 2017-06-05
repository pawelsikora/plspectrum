from gi import pygtkcompat

pygtkcompat.enable() 
pygtkcompat.enable_gtk(version='3.0')

import gtk

from QSpectrum import Spectrum_generator

class GUI:

    def generate_graph(self, widget, data=None):
        c = Spectrum_generator()

        c.arams.A0 = float(self.entry_param_a0.get_text())
        c.params.g0 = float(self.entry_param_g0.get_text())
        c.params.Eg = float(self.entry_param_eg.get_text())
        c.params.T = float(self.entry_param_T.get_text())
        c.params.gamma = float(self.entry_param_gamma.get_text())
        c.params.gamma_schodek = float(self.entry_param_gamma_schodek.get_text())

        c.calculate_all()
        c.plot_widmo_beta()

    def delete_event(self, widget, event, data=None):
        print("delete event occurred")
        return False

    def destroy(self, widget, data=None):
        print("destroy signal occurred")
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(500, 350)    
    
        grid = gtk.Grid()
        self.window.add(grid)    

        self.label_param_a0 = gtk.Label("A0")
        self.label_param_g0 = gtk.Label("g0")
        self.label_param_eg = gtk.Label("Eg")
        self.label_param_T = gtk.Label("T")
        self.label_param_gamma = gtk.Label("Gamma")
        self.label_param_gamma_schodek = gtk.Label("Gamma schodek")

        self.label_param_a0.set_xalign(1)
        self.label_param_g0.set_xalign(1)
        self.label_param_eg.set_xalign(1)
        self.label_param_T.set_xalign(1)
        self.label_param_gamma.set_xalign(1)
        self.label_param_gamma_schodek.set_xalign(1)

        self.entry_param_a0 = gtk.Entry()
        self.entry_param_g0 = gtk.Entry()
        self.entry_param_eg = gtk.Entry()
        self.entry_param_T = gtk.Entry()
        self.entry_param_gamma = gtk.Entry()
        self.entry_param_gamma_schodek = gtk.Entry()

        self.button1 = gtk.Button('Generate graph!')

        self.button2 = gtk.Button('Save graph')

        self.button3 = gtk.Button('Compare two graphs')

        self.window.connect("delete_event", self.delete_event)
    
        self.window.connect("destroy", self.destroy)
    
        self.window.set_border_width(30)
    
        self.button1.connect("clicked", self.generate_graph, None)

        grid.add(self.label_param_a0)
        grid.attach_next_to(self.label_param_g0, self.label_param_a0, gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(self.label_param_eg, self.label_param_g0, gtk.PositionType.BOTTOM, 1, 3)
        grid.attach_next_to(self.label_param_T, self.label_param_eg, gtk.PositionType.BOTTOM, 1, 4)
        grid.attach_next_to(self.label_param_gamma, self.label_param_T, gtk.PositionType.BOTTOM, 1, 5)
        grid.attach_next_to(self.label_param_gamma_schodek, self.label_param_gamma, gtk.PositionType.BOTTOM, 1, 6)

        grid.add(self.entry_param_a0)
        grid.attach_next_to(self.entry_param_g0, self.entry_param_a0, gtk.PositionType.BOTTOM, 2, 2)
        grid.attach_next_to(self.entry_param_eg, self.entry_param_g0, gtk.PositionType.BOTTOM, 2, 3)
        grid.attach_next_to(self.entry_param_T, self.entry_param_eg, gtk.PositionType.BOTTOM, 2, 4)
        grid.attach_next_to(self.entry_param_gamma, self.entry_param_T, gtk.PositionType.BOTTOM, 2, 5)
        grid.attach_next_to(self.entry_param_gamma_schodek, self.entry_param_gamma, gtk.PositionType.BOTTOM, 2, 6)
        grid.attach_next_to(self.button1, self.entry_param_gamma_schodek, gtk.PositionType.RIGHT, 3, 6)

        self.window.show_all()

    def main(self):
        gtk.main()
