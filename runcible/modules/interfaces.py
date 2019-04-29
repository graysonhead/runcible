from runcible.modules.module import Module
from runcible.modules.interface import Interface
from runcible.core.need import Need

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

    def determine_needs(self, other):
        """
        Iterate through the attached modules from another Interfaces module and compare the interfaces, matching them
        via their "name" attributes.

        :param other:
        :return:
        """
        needs_list = []
