from runcible.core.errors import RuncibleValidationError, RuncibleNotImplementedError


class ProviderBase(object):
    provides_for=None

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

    def load_module_dstate(self, dstate):
        self.dstate = self.provides_for(dstate)

    def load_module_cstate(self):
        self.cstate = self.get_cstate()

    def determine_needs(self):
        needs = self.dstate.determine_needs(self.cstate)
        self.needed_actions = needs

    def get_cstate(self):
        """
        Create a module for the current state and return it
        :return:
        """
        raise RuncibleNotImplementedError(f"The provider class {str(self)} has not provided a get_cstate method")

    def complete(self, need):
        self.needed_actions.remove(need)
        self.completed_actions.append(need)
