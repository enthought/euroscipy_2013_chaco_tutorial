from chaco.api import ArrayPlotData, Plot
from chaco.tools.api import ZoomTool, PanTool
from chaco.scales.api import CalendarScaleSystem
from chaco.scales_tick_generator import ScalesTickGenerator
from enable.api import ColorTrait, Component, ComponentEditor
from traits.api import (
    Any, Date, Event, HasTraits, Instance, List, Property, Str,
    cached_property, on_trait_change
)
from traitsui.api import (
    ButtonEditor, EnumEditor, HGroup, Item, InstanceEditor, Spring, VGroup, View
)

from tutorial import TimeSerieGenerator

class DataViewer(HasTraits):

    data_provider = Instance(TimeSerieGenerator, ())

    dataset = Instance(ArrayPlotData)
    plot = Instance(Component)

    def _dataset_default(self):
        dataset = ArrayPlotData()
        dataset.set_data('dates', self.data_provider.timestamps)
        dataset.set_data(self.data_provider.code, self.data_provider.data)

        return dataset

    def _plot_default(self):
        plot = Plot(self.dataset)
        plot.plot( ('dates', self.data_provider.code), type='line')

        # Set the plot's bottom axis to use the Scales ticking system
        ticker = ScalesTickGenerator(scale=CalendarScaleSystem())
        plot.x_axis.tick_generator = ticker

        return plot

    @on_trait_change('data_provider.data')
    def _update_dataset(self, new_data):
        code = self.data_provider.code

        self.dataset.set_data(code, new_data)

    traits_view = View(
        HGroup(
            Item('data_provider', editor=InstanceEditor(), style='custom',
                  show_label=False),
            Item('plot', editor=ComponentEditor(size=(1024, 768)),
                 show_label=False),
        ),
        title='Data viewer',
        resizable=True,
    )

if __name__ == '__main__':
    viewer = DataViewer()
    viewer.configure_traits()
