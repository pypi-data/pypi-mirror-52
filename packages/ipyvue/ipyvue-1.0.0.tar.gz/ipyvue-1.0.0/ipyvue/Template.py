from traitlets import Unicode, Dict
from .VueWidget import VueWidget


class Template(VueWidget):

    _model_name = Unicode('TemplateModel').tag(sync=True)

    v_slot = Unicode().tag(sync=True)


__all__ = ['Template']
