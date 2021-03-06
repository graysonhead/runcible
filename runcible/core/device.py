from runcible.core.callbacks import CBMethod, Callbacks
from runcible.core.callback import CBType, Callback
from runcible.core.plugin_registry import PluginRegistry
from runcible.core.errors import RuncibleValidationError, RuncibleNotConnectedError, RuncibleActionFailure
from runcible.core.terminalcallbacks import TermCallback


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
        self.labels = []
        self.default_client = None
        self.callbacks = Callbacks(callback_method=callback_method)
        self._memoized_comands = {}
        self._kvstore = {}

        self.load_config_from_meta(config['meta']['device'])
        if config['meta'].get('labels', None) is not None:
            self.load_labels(config['meta']['labels'])
        self.load_dstate(config)
        # self.load_module_providers()
        if protocol:
            self.protocol = self.clients[protocol]
        else:
            self.protocol = self.clients[self.default_client]

    def get_labels(self):
        """
        Returns any labels assigned to the device during the Planning stage

        :return:
            An array containing dict representation of labels
        """
        label_array = []
        for label in self.labels:
            label_array.append(label.render_as_dict())
        return label_array

    def load_labels(self, labels_array):
        """
        Takes an array of dict labels and creates/assigns instances of labels to the device instance
        :param labels_array:
            An array of labels:

            Example:
                        [
                            {
                                "type": "adjacent_to",
                                "device": "device1",
                                "switchport": "swp1"
                            }
                        ]
        :return:
        """

        for label_def in labels_array:
            try:
                label_class = PluginRegistry.get_label(label_def['type'])
            except Exception as e:
                raise e
            label_instance = label_class(label_def)
            self.labels.append(label_instance)

    def get_cstate(self):
        """
        Renders the cstate of each module and returns it as a single dict
        :return:
            A dict of the current state
        """
        rendered_dict = {}
        for provider in self.providers:
            rendered_dict.update({provider.cstate.module_name: provider.cstate.render()})
        return rendered_dict

    def plan(self, run_callbacks=True):
        """
        Plan is the stage at which the cstate is fetched from the device and generated

        :param mute_callbacks:
            Prevents printing callbacks to stdout, used when the user is calling "cstate.GET" and only expects yaml or
            json output.

        :return:
            List of callbacks
        """
        self._clear_memoization()
        self.clear_kv_store()
        if getattr(self.driver, 'pre_plan_tasks', None):
            self.driver.pre_plan_tasks(self)
        self.load_cstate()
        self.determine_needs()
        if getattr(self.driver, 'post_plan_tasks', None):
            self.driver.post_plan_tasks(self)
        self.needs_as_callbacks()
        if run_callbacks:
            return self.run_callbacks("plan")

    def run_callbacks(self, stage: str):
        """
        Run all callbacks for the device.

        :param stage:
            String representing the stage that the callbacks are run for. Usually 'plan' or 'execute'

        :return:
            If CBmethod is CBMethod.JSON, a DICT of the callbacks will be returned
        """
        if self.callbacks.callback_method == CBMethod.TERMINAL:
            TermCallback.info(f"Device {self.name} {stage}:")
            TermCallback.info("==========================================")
        callbacks = self.callbacks.run_callbacks()
        self.callbacks.clear_callbacks()
        return callbacks

    def execute(self, run_callbacks=True):
        """
        Execute all planned actions on the device

        :param run_callbacks:
            If true, callbacks will be run automatically after execution completion. Set to false if you need run
            callbacks manually (I.E. When using a multithreaded scheduler.

        :return:
            If run_callbacks=True and CBMethod.JSON, this will return a DICT representing callbacks
        """
        if self.needs_changes:
            if getattr(self.driver, 'pre_exec_tasks', None):
                self.driver.pre_exec_tasks(self)
            self.fix_provider_needs()
            if getattr(self.driver, 'post_exec_tasks', None):
                self.driver.post_exec_tasks(self)
            self.completed_as_callbacks()
        else:
            self.echo("No changes needed",
                      cb_type=CBType.SUCCESS,
                      indent=True,
                      decoration=True)
        self.check_complete()
        self.clear_actions()
        if run_callbacks:
            return self.run_callbacks("execute")
        self.disconnect()

    def ad_hoc_command(self, need):
        """
        Manually execute a single need on this host

        :param need:
            String representing the need object

            Example:
                interface.swp1.ipv4_address.SET: 192.168.1.2/24

        """
        self._clear_memoization()
        self.clear_kv_store()
        if getattr(self.driver, 'pre_plan_tasks', None):
            self.driver.pre_plan_tasks(self)
        self.load_cstate()
        if getattr(self.driver, 'post_plan_tasks', None):
            self.driver.post_plan_tasks()
        # TODO: Better error handling for when wrong parent module is selected
        if need.parent_module:
            provider = next(iter(list(filter(lambda x: x.provides_for.module_name == need.parent_module, self.providers))))
        else:
            provider = next(iter(list(filter(lambda x: x.provides_for.module_name == need.module, self.providers))))
        if getattr(self.driver, 'pre_exec_tasks', None):
            self.driver.pre_exec_tasks(self)
        result = provider.adhoc_need(need)
        self.check_complete()
        if getattr(self.driver, 'post_exec_tasks', None):
            self.driver.post_exec_tasks(self)
        if not result:
            for need in provider.completed_actions:
                self.echo(f"{provider.provides_for.module_name}.{need.get_formatted_string()}",
                          cb_type=CBType.SUCCESS,
                          indent=True)
            # self.post_execution_tasks()
            callbacks = self.callbacks.run_callbacks()
            self.callbacks.clear_callbacks()
        else:
            self.echo(f"{result}")
            self.callbacks.run_callbacks()

    def check_complete(self):
        """
        Checks for needed tasks that haven't run
        :raises TaskFailure:
        """
        for provider in self.providers:
            if provider.needed_actions:
                raise RuncibleActionFailure(provider=provider.provides_for, tasks=provider.needed_actions)

    def clear_actions(self):
        """
        Clears the completed, failed, and needed actions for each provider.
        :return:
        """
        for provider in self.providers:
            provider.needed_actions = []
            provider.completed_actions = []
            provider.failed_actions = []

    def fix_provider_needs(self):
        """
        Iterates over the providers and instructs them to fix their needs
        """
        for provider in self.providers:
            provider.fix_needs()

    def completed_as_callbacks(self):
        """
        Converts completed needs to callbacks
        """
        for provider in self.providers:
            for need in provider.completed_actions:
                self.echo(f"{need.get_formatted_string()}",
                          cb_type=CBType.SUCCESS,
                          indent=True)

    def disconnect(self):
        """
        Disconnect the protocol in use by the device
        """
        self. protocol.disconnect()

    def send_command(self, command, memoize: bool = False):
        """
        A wrapper for sending commands via the default protocol. If you attempt to send a command while the client isn't
        connected and returns a RuncibleNotConnectedError, the client will attempt to connect and re-send the message.

        :param command:
            Command to be executed

        :param memoize:
            If True, this method will return the previous result without re-running the command. Memoization operates
            only within the scope of each instance. This method will only store results from commands run with memoize
            = True

        :return:
            stdout of command

        :raises:
            ClientExecutionError on a non 0 return code on the client
        """
        # If the user
        if memoize:
            for key, value in self._memoized_comands:
                if key == command:
                    return self._memoized_comands[command]
        try:
            result = self.protocol.run_command(command)
            # Store the result if memoize is True
            if memoize:
                self._memoized_comands.update({'command': result})
            return result
        except RuncibleNotConnectedError:
            self.protocol.connect()
            return self.protocol.run_command(command)

    def load_dstate(self, dstate):
        """
        Loads the desired state from the user-specified datasource

        :param dstate:
            Dict representing the desired state of the device
        """
        if not isinstance(dstate, dict):
            raise RuncibleValidationError("load_dstate accepts a dict")
        for key, value in dstate.items():
            if key not in ['meta']:
                # Any key in the dstate that isn't 'meta' is a module, so load the provider for that module
                try:
                    self.providers.append(self.driver.module_provider_map[key](self, value))
                except KeyError:
                    raise RuncibleValidationError(f"{self.driver.driver_name} driver doesn't have a {key} module")

    def load_cstate(self):
        """
        This initializes the selected connection protocol and begins loading cstate from the devices via it's providers
        :return:
        """
        for provider in self.providers:
            provider.load_module_cstate()

    def determine_needs(self):
        """
        Instructs providers to determine and create need objects
        :return:
        """
        for provider in self.providers:
            provider.determine_needs()
            if provider.needed_actions:
                self.needs_changes = True

    def needs_as_callbacks(self):
        """
        Converts needs to callbacks
        """
        for provider in self.providers:
            if provider.needed_actions:
                self.echo(f"{provider.provides_for.module_name} needs:", decoration=True)
                for need in provider.needed_actions:
                    self.echo(f"{need.get_formatted_string()}",
                              cb_type=CBType.CHANGED,
                              indent=True)
            else:
                self.echo(f"{provider.provides_for.module_name} needs no changes.")

    def echo(self, message, indent=False, cb_type=CBType.INFO, decoration=False):
        self.callbacks.add_callback(
            Callback(message, call_type=cb_type, indent=indent, decoration=decoration)
        )

    def _clear_memoization(self):
        """
        Clears any cached memoized commands
        :return:
        """
        self._memoized_comands = {}

    def load_config_from_meta(self, meta_device):
        """
        Loads device config from "meta" key

        :param meta_device:
            The dict of the "meta" key in dstate

        """
        self.meta_device = meta_device
        # First load the driver
        if 'driver' in self.meta_device:
            self.load_driver(self.meta_device['driver'])
        else:
            raise RuncibleValidationError("A device must be specified with a driver")
        for client_type in ['ssh', 'telnet', 'serial', 'rest']:
            if client_type in self.meta_device:
                if client_type not in self.driver.protocol_map:
                    raise RuncibleValidationError(msg=f"Provider {self.driver} doesn't have a {client_type} protocol")
                else:
                    self.clients.update({
                        client_type: self.driver.protocol_map[client_type](self.meta_device[client_type])
                    })
        if 'default_management_protocol' in self.meta_device:
            self.default_client = self.meta_device['default_management_protocol']

    def load_driver(self, driver_name):
        """
        Loads the named driver from the plugin registry class

        :param driver_name:
            Name of the driver
        """
        self.driver = PluginRegistry.get_driver(driver_name)
        # Pass the driver an instance of this object so it can call it's methods
        self.driver.device = self

    def store(self, key: str, value):
        """
        Store is used when one method needs to share data with another. The self.retrieve method can
        be used to access stored values/objects. All kvs are erased when the plan method is run.

        :param key:
            Key to store an object under

        :param value:
            An object to be stored under a key
        :return:
            None
        """
        self._kvstore.update({key: value})

    def retrieve(self, key: str):
        """
        Allows an object to be retrieved from this instances KV store.

        :param key:
            Key used to retrieve object

        :return:
            Value of the key
        """
        return self._kvstore[key]

    def clear_kv_store(self):
        """
        Clears the key/value store
        :return:
        """
        self._kvstore = {}

    def __repr__(self):
        return f"<runcible.core.device.Device: {self.name}>"
