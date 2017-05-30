import pygtk
pygtk.require('2.0')
import gtk

from QSpectrum import Spectrum_generator

class GUI:

    # This is a callback function. The data arguments are ignored
    # in this example. More on callbacks below.
    def generate_graph(self, widget, data=None):
        c = Spectrum_generator()
	c.calculate_all()
	
	#print "Prawd"
	#print c.params.Prawd
	#print "LAMBDA"
	#print c.params.LAMBDA
	#print "Widmo"
	#print c.params.Widmo
	#print "Widmo5"
	#print c.Widmo5

	c.plot_widmo_beta()

    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    	self.window.set_size_request(500, 350)	
	self.entry = gtk.Entry()
        self.entry.set_text("Hello World")
	
	self.hbox = gtk.HButtonBox()
	self.hbox.set_layout(gtk.BUTTONBOX_SPREAD)
	self.hbox.set_border_width(5)
	
	self.bbox = gtk.VButtonBox()
	self.bbox.set_layout(gtk.BUTTONBOX_EDGE)
	self.bbox.set_border_width(5)
        self.bbox.pack_start(self.entry, True, True, 0)	
	
	self.button1 = gtk.Button('Generate graph!')
	self.bbox.add(self.button1)

	self.button2 = gtk.Button('Save graph')
	self.bbox.add(self.button2)

	self.button3 = gtk.Button('Compare two graphs')
	self.bbox.add(self.button3)

        self.window.connect("delete_event", self.delete_event)
    
        self.window.connect("destroy", self.destroy)
    
        self.window.set_border_width(30)
    
        #self.button = gtk.Button("Generate graph!")
    
        self.button1.connect("clicked", self.generate_graph, None)
    
        #self.window.add(self.button)
        self.window.add(self.bbox)
        #self.window.add(self.hbox)
        #self.window.add(self.entry)
    
        #self.button.show()
    	self.window.show_all()
        #self.window.show()

    def main(self):
        gtk.main()
