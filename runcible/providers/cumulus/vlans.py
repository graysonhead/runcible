from runcible.providers.provider_array import ProviderArrayBase
from runcible.modules.vlans import Vlans
from runcible.modules.vlan import Vlan
from runcible.providers.cumulus.vlan import CumulusVlanProvider
from runcible.providers.cumulus.utils import extrapolate_list


class CumulusVlansProvider(ProviderArrayBase):
    provides_for = Vlans
    sub_module_provider = CumulusVlanProvider

    def _create_module(self, vlan):
        return self.device.send_command(f"net add bridge bridge vids {vlan}")

    def _remove_module(self, vlan):
        return self.device.send_command(f"net del bridge bridge vids {vlan}")

    def get_cstate(self):
        vlan_modules = []
        commands = self.device.retrieve('parsed_commands')
        for line in commands:
            if line.startswith('net add bridge bridge vids'):
                split_line = line.split(' ')
                id_list = extrapolate_list(split_line[5].split(','), int_out=True)
                for id in id_list:
                    vlan_modules.append(Vlan({"id": id}))
        vlans_module = Vlans({})
        vlans_module.vlans = vlan_modules
        return vlans_module

