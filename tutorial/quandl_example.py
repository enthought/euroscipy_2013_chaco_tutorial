import datetime

import numpy as np

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

import Quandl

today = datetime.datetime.today()

class QuandlDataProvider(HasTraits):
    """ Very basic time serie generator. """

    code = Str('NYX/XBRU_ABI')
    from_date = Date(today - datetime.timedelta(days=365))
    to_date = Date(today)
    generate = Event

    timestamps = Property(depends_on='_resultset')
    data = Property(depends_on='_resultset')

    _resultset = Property(depends_on='generate')

    @cached_property
    def _get__resultset(self):
        results = Quandl.get(
            self.code, trim_start=self.from_date, trim_end=self.to_date,
            returns='numpy'
        )
        return results

    @cached_property
    def _get_data(self):
        results = self._resultset
        # return the first time serie assuming the
        return results[results.dtype.names[1]]

    @cached_property
    def _get_timestamps(self):
        results = self._resultset
        # horry gorry conversion of the first column that we assume to be the
        # dates S10 and that we convert to M8[D] then to M8[s]
        days = results[results.dtype.names[0]].astype('datetime64[D]')
        seconds = days.astype('datetime64[s]')
        timestamps = seconds.astype(int)
        return timestamps

    ### Traits UI view #########################################################

    traits_view = View(
        VGroup(
            HGroup('code'),
            HGroup('from_date', 'to_date'),
            HGroup(
                Spring(),
                Item('generate', editor=ButtonEditor(), show_label=False)
            )
        ),
        title ='Generator',
        width=200,
        resizable=True
    )

class DataViewer(HasTraits):

    data_provider = Instance(QuandlDataProvider, ())

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

    ### Traits UI view #########################################################
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
