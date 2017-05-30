from gi import pygtkcompat

pygtkcompat.enable() 
pygtkcompat.enable_gtk(version='3.0')

import gtk

from QSpectrum import Spectrum_generator

class GUI:

    def generate_graph(self, widget, data=None):
        c = Spectrum_generator()
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
    
        self.entry = gtk.Entry()
        self.entry.set_text("Hello World")
    
        self.button1 = gtk.Button('Generate graph!')

        self.button2 = gtk.Button('Save graph')

        self.button3 = gtk.Button('Compare two graphs')

        self.window.connect("delete_event", self.delete_event)
    
        self.window.connect("destroy", self.destroy)
    
        self.window.set_border_width(30)
    
        self.button1.connect("clicked", self.generate_graph, None)
    
        grid.add(self.entry)
        grid.attach_next_to(self.button1, self.entry, gtk.PositionType.RIGHT, 2, 1)
	
        self.window.show_all()

    def main(self):
        gtk.main()
