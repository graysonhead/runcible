from runcible.providers.provider import ProviderBase
from runcible.modules.interfaces import Interfaces
from runcible.providers.cumulus.utils import pre_parse_commands


class CumulusInterfacesProvider(ProviderBase):
    provides_for = Interfaces

    def get_cstate(self):
        commands = self.device.retrieve('parsed_commands')
        # This dict will contain a list of commands specific to each interface
        interface_commands = {}
        for line in commands:
            if "interface" in line or "bond" in line:
                split_line = line.split(' ')
                if "interface" == split_line[2] or "bond" == split_line[2]:
                    if_name = split_line[3]
                    truncated_line = split_line[4:]
                    if if_name not in interface_commands:
                        interface_commands.update({if_name: []})
                    interface_commands[if_name].append(truncated_line)
        for key, value in interface_commands.items():
            pass