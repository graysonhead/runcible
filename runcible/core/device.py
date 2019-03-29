from runcible.core.callbacks import CBMethod, Callbacks
from runcible.core.callback import CBType as CBT


class Device(object):
    """
    A device represents a single network device in Runcible. A device will have:
        - A connection method (such as SSH)
        - A driver plugin (such as cumulus)
        - Current State
        - Desired State
    """

    def __init__(self, name, callback_method=CBMethod.JSON):
        self.name = name
        self.meta = {}
        self.modules = {}
        self.callbacks = Callbacks(callback_method=callback_method)

    def load_dstate(self, dstate):
        if not isinstance(dstate, dict):

    def load_modules(self):

