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

today = datetime.datetime.today()

class TimeSerieGenerator(HasTraits):
    """ Very basic time serie generator.

    Each generate event will invalidate the data and dates properties. The data
    is a basic array of random values.

    """

    code = Str('Dataset1')
    from_date = Date(today - datetime.timedelta(days=365))
    to_date = Date(today)
    generate = Event

    timestamps = Property(depends_on='from_date,to_date')
    data = Property(depends_on='dates,generate')

    @cached_property
    def _get_data(self):
        days = (self.to_date - self.from_date).days
        results =  np.random.random(days)
        return results

    @cached_property
    def _get_timestamps(self):
        # horry gorry conversion
        days = np.arange(self.from_date, self.to_date, dtype='datetime64[D]')
        seconds = days.astype('datetime64[s]')
        timestamps = seconds.astype(int)
        return timestamps

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

if __name__ == '__main__':
    generator = TimeSerieGenerator()
    generator.configure_traits()
