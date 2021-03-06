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

from tutorial import TimeSerieGenerator

class RendererEditor(HasTraits):

    plot = Instance(Plot)
    color = ColorTrait('blue')

    renderers = Property(List, depends_on='plot.plots')
    selected_renderer = Any

    def _get_renderers(self):
        return self.plot.plots.keys()

    def _selected_renderer_default(self):
        return self.renderers[0]

    def _color_changed(self):
        renderer = self.plot.plots[self.selected_renderer][0]
        renderer.color = self.color

    def _selected_renderer_changed(self):
        renderer = self.plot.plots[self.selected_renderer][0]
        self.color = renderer.color

    traits_view = View(
        HGroup(
            Item('selected_renderer', editor=EnumEditor(name='renderers'),
                show_label=False),
            Item('color', show_label=False),
        )
    )


class DataViewer(HasTraits):

    data_provider = Instance(TimeSerieGenerator, ())

    dataset = Instance(ArrayPlotData)
    plot = Instance(Component)
    renderer_editor = Instance(RendererEditor)

    def _dataset_default(self):
        dataset = ArrayPlotData()
        dataset.set_data('dates', self.data_provider.timestamps)
        dataset.set_data(self.data_provider.code, self.data_provider.data)

        return dataset

    def _plot_default(self):
        code = self.data_provider.code
        plot = Plot(self.dataset)
        plot.plot(
            ('dates', code), type='line', color='blue',name=code
        )

        # Add tools
        plot.tools.append(ZoomTool(plot))
        plot.tools.append(PanTool(plot))

        # Set the plot's bottom axis to use the Scales ticking system
        ticker = ScalesTickGenerator(scale=CalendarScaleSystem())
        plot.x_axis.tick_generator = ticker

        return plot

    def _renderer_editor_default(self):
        editor = RendererEditor(plot=self.plot, color='blue')
        return editor

    @on_trait_change('data_provider.data')
    def _add_new_plot(self, new_data):
        code = self.data_provider.code

        if code in self.dataset.list_data():
            add_to_plot = False
        else:
            add_to_plot = True

        self.dataset.set_data(code, new_data)

        if add_to_plot:
            random_color = np.random.random(3).tolist()
            self.plot.plot(
                ('dates', code), type='line', color=random_color, name=code
            )

    traits_view = View(
        HGroup(
            VGroup(
                Item('data_provider', editor=InstanceEditor(), style='custom',
                  show_label=False),
                Item('renderer_editor', editor=InstanceEditor(), style='custom',
                    show_label=False),
            ),
            Item('plot', editor=ComponentEditor(size=(1024, 768)),
                 show_label=False),
        ),
        title='Data viewer',
        resizable=True,
    )

if __name__ == '__main__':
    viewer = DataViewer()
    viewer.configure_traits()
