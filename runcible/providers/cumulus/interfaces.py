from runcible.providers.provider import ProviderBase
from runcible.providers.cumulus.interface import CumulusInterfaceProvider
from runcible.modules.interfaces import Interfaces
from runcible.providers.cumulus.utils import pre_parse_commands


class CumulusInterfacesProvider(ProviderBase):
    provides_for = Interfaces

    def get_cstate(self):
        commands = self.device.retrieve('parsed_commands')
        # Associate commands with their respective interfaces
        interface_commands = {}
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
        interfaces_config = []
        for key, value in interface_commands.items():
            # Build the parameter list to pass to each interface module
            interface_config = {"name": key}
            # Only parse the command if the list for this interface isn't empty
            if value:
                for command in value:
                    if command[0] == 'bridge':
                        if command[1] == 'pvid':
                            interface_config.update({'pvid': command[2]})
            interfaces_config.append(interface_config)
        return Interfaces(interfaces_config)

    def fix_needs(self):
        for need in self.needed_actions:
            CumulusInterfaceProvider.fix_need(self, need)
