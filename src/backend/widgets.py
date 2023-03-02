# widgets.py
import uuid


def compose(f, g):
    return lambda x: f(g(x))


class Widget(object):
    '''The base Widget class'''

    def __init__(self):
        self.id = uuid.uuid1()
        self.algorithm = lambda ws: ws
        self._cache = None
        self._workset = None
        self.type = "Generic"

    @property
    def workset(self):
        return self._workset

    @workset.setter
    def workset(self, workset):
        self.reset()
        self._workset = workset

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"

    def add_step(self, fn):
        self.algorithm = compose(fn, self.algorithm)

    def reset(self):
        self._cache = None

    def refresh(self):
        self.reset()
        self.apply_to(self.workset)

    def apply_to(self, ws):
        if self._cache is None:
            self._cache = self.algorithm(ws)
        return self._cache

    @property
    def data(self):
        if self._cache is None:
            self.refresh()
        return self._cache


class MetadataWidget(Widget):
    '''Shows metadata for a workset'''

    def __init__(self):
        super().__init__()
        self.type = "MetadataWidget"

        def return_values(ws):
            return ws.metadata

        self.add_step(lambda ws: return_values(ws))



class TimelineWidget(Widget):
    '''publication timeline for workset'''

    def __init__(self):
        super().__init__()
        self.type = "TimelineWidget"

        def return_values(ws):
            return [{"title": v.title,
                     "pub_date": v.pub_date}
                    for v in ws.volumes]

        self.add_step(lambda ws: return_values(ws))

class WidgetFactory:
    def __init__(self):
        self._widget_classes = {}

    @classmethod
    def make_widget(cls, widget_class: str):
        try:
            klass = globals()[widget_class]
            widget = klass()
            return widget
        except KeyError:
            print(f"Widget class {widget_class} not defined")
            raise KeyError()
