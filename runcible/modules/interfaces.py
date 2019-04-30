from runcible.modules.module_array import ModuleArray
from runcible.modules.interface import Interface
from runcible.core.need import Need
from runcible.core.need import NeedOperation as Op

class Interfaces(ModuleArray):
    module_name = 'interfaces'
    sub_module = Interface
    # configuration_attributes = {}
    #
    # def __init__(self, config_dictionary: dict):
    #     """
    #     We override the super class and do not call it as this handles it's attributes differently.
    #
    #     :param config_dictionary:
    #         The dstate or cstate that contains each interface configuration
    #     """
    #     self.interfaces = []
    #     for interface in config_dictionary:
    #         self.interfaces.append(Interface(interface))

    def determine_needs(self, other):
        """
        Iterate through the attached modules from another Interfaces module and compare the interfaces, matching them
        via their "name" attributes.

        :param other:
        :return:
        """
        needs_list = []
        interfaces_sorted_left = sorted(self.interfaces, key=lambda x: x.name)
        interfaces_sorted_right = sorted(other.interfaces, key=lambda x: x.name)
        for interface in interfaces_sorted_left:
            right_interface = list(filter(lambda x: x.name == interface.name, interfaces_sorted_right))[0]
            if not right_interface:
                needs_list.append(Need(
                    interface.name,
                    Op.ADD,
                ))
            needs_list.extend(interface.determine_needs(right_interface))
        return needs_list

