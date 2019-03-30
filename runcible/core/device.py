from runcible.core.callbacks import CBMethod, Callbacks
from runcible.core.callback import CBType as CBT
from runcible.core.plugin_registry import PluginRegistry
from runcible.core.errors import ValidationError
from runcible.protocols.ssh import SSHClient


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
        self.modules = []
        self.callbacks = Callbacks(callback_method=callback_method)

    def load_dstate(self, dstate):
        if not isinstance(dstate, dict):
            raise ValidationError("load_dstate accepts a dict")
        for key, value in dstate.items():
            if key not in ['meta']:
                # Any key in the dstate that isn't 'meta' is a module, so load that
                # module and inject it's configuration
                self.modules.append(PluginRegistry.get_module(key)(value))
            elif key == 'meta':
                # Store the meta dict in self.meta so we can use it to load and configure the driver
                self.meta = value

    def load_config_from_meta(self):

