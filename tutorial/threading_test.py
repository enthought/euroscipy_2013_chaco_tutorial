import time
import threading

import numpy as np

from traits.etsconfig.etsconfig import ETSConfig
ETSConfig.toolkit = "qt4"

from enable.api import ComponentEditor
from chaco.api import ArrayPlotData, Plot

from traits.api import Event, HasTraits, Instance
from traitsui.api import View, Item

class PlotWindow(HasTraits):

    dataset = Instance(ArrayPlotData)
    plot = Instance(Plot)

    def _dataset_default(self):
        x = np.linspace(0,2*np.pi,200)
        y = np.sin(x)
        plotdata = ArrayPlotData(x=x, y=y)
        return plotdata

    def _plot_default(self):
        plot = Plot(self.dataset, padding=50, border_visible=True)
        plot.plot(('x', 'y'))
        return plot

    def update_display(self, x, y):
        print 'updating', threading.current_thread()
        self.dataset.set_data('x', x)
        self.dataset.set_data('y', y)

    traits_view = View(
        Item('plot', editor=ComponentEditor(size=(400, 400)), show_label=False)
    )

def run_collection(datamodel):
    # this is where I would start and stop my hardware,
    # but I will just call the read function myself here
    for i in range(1,10):
        x = np.linspace(0,2*np.pi,200)
        y = np.sin(x*i)
        datamodel.update_display(x, y)
        time.sleep(0.5)

def main():
    plot = PlotWindow()

    t = threading.Thread(target=run_collection, args=(plot,))
    t.start()

    # Starts the UI and the GUI mainloop
    plot.configure_traits()

    # don't call t.join() as it blocks the current thread...

if __name__ == "__main__":
    main()
