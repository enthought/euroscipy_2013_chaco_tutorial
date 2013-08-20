from chaco.api import ArrayPlotData, Plot
from chaco.tools.api import ZoomTool, PanTool
from chaco.scales.api import CalendarScaleSystem
from chaco.scales_tick_generator import ScalesTickGenerator
from enable.api import Component, ComponentEditor
from traits.api import (
    Bool, Date, Event, HasTraits, Instance, Property, Str, cached_property,
    on_trait_change
)
from traitsui.api import (
    ButtonEditor, HGroup, Item, InstanceEditor, Spring, VGroup, View
)

import Quandl

class QuandlDataLoader(HasTraits):

    code = Str('ECONWEBINS/INT_RATES_BELGIUM')
    filter_date = Bool(False)
    from_date = Date
    to_date = Date
    load = Event

    data = Property(depends_on='load')

    @cached_property
    def _get_data(self):
        """ Retrieves the dataset from Quandl. """

        kwargs = {'returns':'numpy'}

        if self.filter_date:
            kwargs['trim_start'] = self.from_date
            kwargs['trim_end'] = self.to_date

        results =  Quandl.get(self.code, **kwargs)
        # Assuming we only get a two columns structured array!
        # convert the result to something more useful
        columns = results.dtype.names

        # horry gorry conversion ... from str to timestamp
        dates = results[columns[0]].astype('datetime64[D]').astype('datetime64[s]').astype(int)
        values = results[columns[1]]

        return dates, values

    traits_view = View(
        VGroup(
            HGroup('code', 'filter_date'),
            HGroup('from_date', 'to_date', enabled_when='filter_date'),
            HGroup(Spring(), Item('load', editor=ButtonEditor(), show_label=False),)
        ),
        title ='Quandl Loader',
        width=200,
        resizable=True
    )


class DataViewer(HasTraits):

    loader = Instance(QuandlDataLoader, ())

    dataset = Instance(ArrayPlotData)
    plot = Instance(Component)
    mini_plot = Instance(Component)

    def _dataset_default(self):
        dataset = ArrayPlotData()
        dates, values = self.loader.data
        dataset.set_data('dates', dates)
        dataset.set_data('values', values)

        return dataset

    def _plot_default(self):
        plot = Plot(self.dataset)
        plot.plot( ('dates', 'values'), type='line')

        # Add tools
        plot.tools.append(ZoomTool(plot))
        plot.tools.append(PanTool(plot))

        # Set the plot's bottom axis to use the Scales ticking system
        ticker = ScalesTickGenerator(scale=CalendarScaleSystem())
        plot.x_axis.tick_generator = ticker

        return plot

    @on_trait_change('loader.data')
    def _update_dataset(self, new_data):
        dates, values = new_data
        self.dataset.set_data('dates', dates)
        self.dataset.set_data('values', values)

    traits_view = View(
        HGroup(
            Item('loader', editor=InstanceEditor(), style='custom',
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
