from runcible.core.errors import RuncibleValidationError, RuncibleNotImplementedError
from runcible.core.callback import CBType


class ProviderBase(object):
    provides_for = None
    supported_resources = []

    def __init__(self, device_instance, dstate):
        """
        This class has two methods: get_cstate and execute_needs which fetch the current state from the
        system, and executes needs from it's parent device instance.

        :param device_instance:
            When created by it's parent module object, the module should inject self into
            this instance so the provider can make use of it's client functions
        """
        self.device = device_instance
        self.cstate = None
        self.dstate = None
        self.needed_actions = []
        self.completed_actions = []
        self.failed_actions = []
        self.load_module_dstate(dstate)

    def get_supported_resources(self):
        return self.supported_resources

    def load_module_dstate(self, dstate):
        self.dstate = self.provides_for(dstate)

    def load_module_cstate(self):
        self.cstate = self.get_cstate()

    def determine_needs(self):
        needs = self.dstate.determine_needs(self.cstate)
        self.needed_actions = needs
        # Ensure that the provider supports all of the needs, and raise a warning if not
        self.check_needs_compatibility()

    def check_needs_compatibility(self):
        """
        Ensure that all the needs present are supported by the provider, and raise a warning if not.
        :return:
        """
        supported_resources = self.get_supported_resources()
        for need in self.needed_actions:
            if need.resource not in supported_resources:
                self.device.echo(f"WARNING: need {need.get_formatted_string()} is not supported by module {str(self)}",
                                 cb_type=CBType.WARNING,
                                 indent=True)
                self.remove_need(need)

    def get_cstate(self):
        """
        Create a module for the current state and return it
        :return:
        """
        raise RuncibleNotImplementedError(f"The provider class {str(self)} has not provided a get_cstate method")

    def complete(self, need):
        self.needed_actions.remove(need)
        self.completed_actions.append(need)

    def remove_need(self, need):
        self.needed_actions.remove(need)
