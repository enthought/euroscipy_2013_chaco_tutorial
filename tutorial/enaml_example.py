import enaml
from enaml.stdlib.sessions import show_simple_view

from quandl_example import DataViewer

if __name__ == '__main__':
    with enaml.imports():
        from enaml_viewer import Viewer

    viewer = Viewer(model=DataViewer())
    show_simple_view(viewer)
