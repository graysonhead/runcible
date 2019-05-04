from runcible.providers.provider import ProviderBase
from runcible.modules.vlans import Vlans
from runcible.providers.cumulus.utils import extrapolate_list

class CumulusVlansProvider(ProviderBase):
    provides_for = Vlans

    def get_cstate(self):
        commands = self.device.retrieve('parsed_commands')
        for line in commands:
            if line.startswith('net add bridge bridge vids'):
                split_line = line.split(' ')
                id_list = extrapolate_list(split_line[5].split(','))
                pass