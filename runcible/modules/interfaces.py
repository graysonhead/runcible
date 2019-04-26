from runcible.modules.module import Module
from runcible.modules.interface import Interface

class Interfaces(Module):
    module_name = 'interfaces'
    configuration_attributes = {}

    def __init__(self, config_dictionary: dict):
        """
        We override the super class and do not call it as this handles it's attributes differently.

        :param config_dictionary:
            The dstate or cstate that contains each interface configuration
        """
        self.interfaces = []
        for interface in config_dictionary:
            self.interfaces.append(Interface(interface))