from runcible.core.errors import RuncibleValidationError, RuncibleNotImplementedError
from runcible.core.callback import CBType
from runcible.core.need import NeedOperation as Op
import copy
import logging
logger = logging.getLogger(__name__)


class ProviderBase(object):
    provides_for = None
    supported_attributes = []

    def __init__(self, device_instance, dstate):
        """
        This class has two methods: get_cstate and execute_needs which fetch the current state from the
        system, and executes needs from it's parent device instance.

        :param device_instance:
            When created by it's parent module object, the module should inject self into
            this instance so the provider can make use of it's client functions
        """
        self.device = device_instance
        self.cstate = self.provides_for({})
        self.dstate = None
        self.needed_actions = []
        self.completed_actions = []
        self.failed_actions = []
        self.load_module_dstate(dstate)

    def adhoc_need(self, need):
        if need.operation == Op.GET:
            return getattr(self.cstate, need.attribute)
        else:
            self.needed_actions.append(need)
            self.check_needs_compatibility()
            self.fix_needs()

    def get_supported_attributes(self):
        return self.supported_attributes

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
        supported_attributes = self.get_supported_attributes()
        for need in self.needed_actions:
            if need.attribute not in supported_attributes:
                # self.device.echo(f"WARNING: need {need.get_formatted_string()} is not supported by provider {str(self)}",
                #                  cb_type=CBType.WARNING,
                #                  indent=True)
                logger.warning(f"Need {need.get_formatted_string()} is not supported by provider {str(self)}")
                self.remove_need(need)

    def get_cstate(self):
        """
        Create a module for the current state and return it
        :return:
        """
        raise RuncibleNotImplementedError(f"The provider class {str(self)} has not provided a get_cstate method")

    def complete(self, need):
        # In some cases, modules create meta-needs that aren't exposed to the user. While this is discouraged, there are
        # some cases where it is necessary. As a result, we don't strictly check if the need was in the list of needed
        # actions.
        if need in self.needed_actions:
            self.needed_actions.remove(need)
        self.completed_actions.append(need)

    def get_needs(self):
        """
        This method gets a deep copy of the current needs set so that it can be safely iterated over by providers
        :return:
        """
        needs = copy.deepcopy(self.needed_actions)
        return needs

    def remove_need(self, need):
        self.needed_actions.remove(need)

    def fix_needs(self):
        raise RuncibleNotImplementedError(msg="This provider doesn't implement a fix_needs class")
