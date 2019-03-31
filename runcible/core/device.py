from runcible.core.callbacks import CBMethod, Callbacks
from runcible.core.callback import CBType as CBT
from runcible.core.plugin_registry import PluginRegistry
from runcible.core.errors import ValidationError
from runcible.protocols.ssh_protocol import SSHProtocol


class Device(object):
    """
    A device represents a single network device in Runcible. A device will have:
        - A connection method (such as SSH)
        - A driver plugin (such as cumulus)
        - Current State
        - Desired State
    """

    def __init__(self, name, config, callback_method=CBMethod.JSON, protocol=None):
        self.name = name
        self.meta_device = {}
        self.clients = {}
        self.modules = []
        self.driver = None
        self.default_client = None
        self.callbacks = Callbacks(callback_method=callback_method)

        self.load_dstate(config)
        self.load_config_from_meta()
        self.load_module_providers()
        if protocol:
            self.protocol = self.clients[protocol]
        else:
            self.protocol = self.clients[self.default_client]

    def get_cstate(self):
        self.protocol.connect()
        for module in self.modules:
            module.provider.get_cstate()

    def send_command(self, command):
        return self.protocol.run_command(command)

    def load_dstate(self, dstate):
        if not isinstance(dstate, dict):
            raise ValidationError("load_dstate accepts a dict")
        for key, value in dstate.items():
            if key not in ['meta']:
                # Any key in the dstate that isn't 'meta' is a module, so load that
                # module and inject it's configuration
                self.modules.append(PluginRegistry.get_module(key)(value, device=self))
            elif key == 'meta':
                # Store the meta dict in self.meta so we can use it to load and configure the driver
                if 'device' not in value:
                    raise ValidationError("A device instance must have a device configuration section")
                self.meta_device = value['device']

    def load_config_from_meta(self):
        # First load the driver
        if 'driver' in self.meta_device:
            self.load_driver(self.meta_device['driver'])
        else:
            raise ValidationError("A device must be specified with a driver")
        # Then load the connection protocols
        if 'ssh' in self.meta_device:
            ssh_conf = self.meta_device['ssh']
            if 'hostname' not in ssh_conf or 'username' not in ssh_conf:
                raise ValidationError("SSH connection method requires a username and hostname at a minimum")
            ssh = SSHProtocol(
                hostname=ssh_conf['hostname'],
                username=ssh_conf['username'],
                password=getattr(ssh_conf, 'password', None),
                port=getattr(ssh_conf, 'port', 22)

            )
            self.clients.update({'ssh': ssh})
        if 'default_management_protocol' in self.meta_device:
            self.default_client = self.meta_device['default_management_protocol']

    def load_driver(self, driver_name):
        self.driver = PluginRegistry.get_driver(driver_name)

    def load_module_providers(self):
        for module in self.modules:
            module.load_provider(self.driver.load_provider(module.module_name))
