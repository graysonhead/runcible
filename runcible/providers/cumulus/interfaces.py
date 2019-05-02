from runcible.providers.provider import ProviderBase
from runcible.providers.cumulus.interface import CumulusInterfaceProvider
from runcible.modules.interfaces import Interfaces
from runcible.providers.cumulus.utils import pre_parse_commands
import copy


class CumulusInterfacesProvider(ProviderBase):
    provides_for = Interfaces

    def get_cstate(self):
        commands = self.device.retrieve('parsed_commands')
        # Associate commands with their respective interfaces
        interface_commands = {}
        interface_instances = []
        for line in commands:
            if "interface" in line or "bond" in line:
                split_line = line.split(' ')
                if "interface" == split_line[2] or "bond" == split_line[2]:
                    if_name = split_line[3]
                    # Add the interface to the interface_commands dict if it's key doesn't exit
                    if if_name not in interface_commands:
                        interface_commands.update({if_name: []})
                    # Only add the truncated line if split_line contains an attribute we are interested in
                    # Any line shorter than 4 words simply defines the interface with no attributes
                    if split_line.__len__() > 4:
                        truncated_line = split_line[4:]
                        interface_commands[if_name].append(truncated_line)
        for k, v in interface_commands.items():
            interface_instances.append(CumulusInterfaceProvider.get_cstate(k, v))
        interfaces_inst = Interfaces({})
        interfaces_inst.interfaces = interface_instances
        return interfaces_inst

    def fix_needs(self):
        needed_actions = copy.deepcopy(self.needed_actions)
        for need in needed_actions:
            CumulusInterfaceProvider.fix_need(self, need)
