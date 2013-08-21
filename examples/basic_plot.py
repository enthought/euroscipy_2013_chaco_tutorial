"""
The most basic plot.
"""

# Major library imports
from numpy import sort
from numpy.random import random

# Enthought library imports
from enable.api import Component, ComponentEditor
from traits.api import HasTraits, Instance
from traitsui.api import Item, Group, View

# Chaco imports
from chaco.api import ArrayPlotData, Plot

class BasicPlotViewer(HasTraits):

    dataset = Instance(ArrayPlotData)
    plot = Instance(Component)

    def _dataset_default(self):
        # Create some data
        numpts = 5000
        x = sort(random(numpts))
        y = random(numpts)

        # Create a plot data object and give it this data
        dataset = ArrayPlotData()
        dataset.set_data("index", x)
        dataset.set_data("value", y)

        return dataset

    def _plot_default(self):
        # Create the plot
        plot = Plot(self.dataset)

        plot.plot(
            ("index", "value"),
            type="scatter",
            marker='circle',
            color='blue'
        )

        # Tweak some of the plot properties
        plot.title = "Scatter Plot"
        plot.line_width = 0.5
        plot.padding = 50

        return plot


    ### Traits UI view #########################################################

    traits_view = View(
        Group(
            Item(
                'plot',
                editor=ComponentEditor(size=(650, 650)),
                show_label=False
            ),
            orientation = "vertical"
        ),
        resizable=True, title="Basic scatter plot"
    )


if __name__ == "__main__":

    viewer = BasicPlotViewer()
    viewer.configure_traits()

#--EOF---
