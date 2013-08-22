from chaco.api import ArrayPlotData, Plot, VPlotContainer
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

from tutorial import TimeSerieGenerator   )

class DataViewer(HasTraits):

    data_provider = Instance(TimeSerieGenerator, ())

    dataset = Instance(ArrayPlotData)
    container = Instance(Component)

    def _dataset_default(self):
        dataset = ArrayPlotData()
        dataset.set_data('dates', self.data_provider.timestamps)
        dataset.set_data(self.data_provider.code, self.data_provider.data)

        return dataset

    def _container_default(self):
        plot = Plot(self.dataset)
        plot.plot( ('dates', self.data_provider.code), type='line')

        # Add tools
        plot.tools.append(ZoomTool(plot))
        plot.tools.append(PanTool(plot))

        # Set the plot's bottom axis to use the Scales ticking system
        ticker = ScalesTickGenerator(scale=CalendarScaleSystem())
        plot.x_axis.tick_generator = ticker

        container = VPlotContainer()
        container.add(plot)

        return container

    @on_trait_change('data_provider.data')
    def _add_new_plot(self, new_data):
        code = self.data_provider.code

        if code in self.dataset.list_data():
            create_new_plot = False
        else:
            create_new_plot = True

        self.dataset.set_data(code, new_data)

        if create_new_plot:
            new_plot = Plot(self.dataset)
            new_plot.plot(('dates', code), type='line')
            new_plot.tools.append(PanTool(new_plot))
            tick_generator = ScalesTickGenerator(scale=CalendarScaleSystem())
            new_plot.x_axis.tick_generator = tick_generator

            # connect the index of the first plot with the new plot
            first_plot = self.container.components[0]
            new_plot.index_range = first_plot.index_range


            self.container.add(new_plot)
            self.container.request_redraw()

    traits_view = View(
        HGroup(
            Item('data_provider', editor=InstanceEditor(), style='custom',
                  show_label=False),
            Item('container', editor=ComponentEditor(size=(1024, 768)),
                 show_label=False),
        ),
        title='Data viewer',
        resizable=True,
    )

if __name__ == '__main__':
    viewer = DataViewer()
    viewer.configure_traits()
