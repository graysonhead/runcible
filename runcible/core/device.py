from runcible.core.callbacks import CBMethod, Callbacks
from runcible.core.callback import CBType, Callback
from runcible.core.plugin_registry import PluginRegistry
from runcible.core.errors import ValidationError, RuncibleNotConnectedError
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
        self.providers = []
        self.needs_changes = False
        self.driver = None
        self.default_client = None
        self.callbacks = Callbacks(callback_method=callback_method)

        self.load_config_from_meta(config['meta']['device'])
        self.load_dstate(config)
        # self.load_module_providers()
        if protocol:
            self.protocol = self.clients[protocol]
        else:
            self.protocol = self.clients[self.default_client]

    def plan(self):
        self.load_cstate()
        self.determine_needs()
        self.needs_as_callbacks()
        self.callbacks.run_callbacks()

    def execute(self):
        if self.needs_changes:
            self.fix_provider_needs()
            self.completed_as_callbacks()
            self.post_execution_tasks()
        else:
            self.echo("No changes needed",
                      cb_type=CBType.SUCCESS,
                      indent=True,
                      decoration=True)
        self.callbacks.run_callbacks()

    def post_execution_tasks(self, changed=False):
        if self.driver.post_exec_tasks:
            for command in self.driver.post_exec_tasks:
                self.send_command(command)

    def fix_provider_needs(self):
        for provider in self.providers:
            provider.fix_needs()

    def completed_as_callbacks(self):
        for provider in self.providers:
            for need in provider.completed_actions:
                self.echo(f"{provider.provides_for.module_name}.{need.get_formatted_string()}",
                          cb_type=CBType.SUCCESS,
                          indent=True)

    def send_command(self, command):
        """
        A wrapper for sending commands via the default protocol. If you attempt to send a command while the client isn't
        connected and returns a RuncibleNotConnectedError, the client will attempt to connect and re-send the message.

        :param command:
            Command to be executed

        :return:
            stdout of command

        :raises:
            ClientExecutionError on a non 0 return code on the client
        """
        try:
            return self.protocol.run_command(command)
        except RuncibleNotConnectedError:
            self.protocol.connect()
            return self.protocol.run_command(command)

    def load_dstate(self, dstate):
        if not isinstance(dstate, dict):
            raise ValidationError("load_dstate accepts a dict")
        for key, value in dstate.items():
            if key not in ['meta']:
                # Any key in the dstate that isn't 'meta' is a module, so load the provider for that module
                self.providers.append(self.driver.module_provider_map[key](self, value))

    def load_cstate(self):
        """
        This initializes the selected connection protocol and begins loading cstate from the devices via it's providers
        :return:
        """
        for provider in self.providers:
            provider.load_module_cstate()

    def determine_needs(self):
        for provider in self.providers:
            provider.determine_needs()
            if provider.needed_actions:
                self.needs_changes = True

    def needs_as_callbacks(self):
        for provider in self.providers:
            if provider.needed_actions:
                self.echo(f"{provider.provides_for.module_name} needs:", decoration=True)
                for need in provider.needed_actions:
                    self.echo(f"{provider.provides_for.module_name}.{need.get_formatted_string()}",
                              cb_type=CBType.CHANGED,
                              indent=True)
            else:
                self.echo(f"{provider.provides_for.module_name} needs no changes.")

    def echo(self, message, indent=False, cb_type=CBType.INFO, decoration=False):
        self.callbacks.add_callback(
            Callback(message, call_type=cb_type, indent=indent, decoration=decoration)
        )

    def load_config_from_meta(self, meta_device):
        self.meta_device = meta_device
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
