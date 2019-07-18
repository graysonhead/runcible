from runcible.providers.provider_array import ProviderArrayBase
from runcible.modules.vlans import Vlans
from runcible.modules.vlan import Vlan, VlanResources
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
        # Create an instance of the Vlans module_array to hold our Vlan modules
        vlans_module = Vlans({})
        # Fetch the parsed_commands value from the device key/value store
        commands = self.device.retrieve('parsed_commands')
        vlan_commands = {}
        for line in commands:
            if line.startswith('net add vlan'):
                split_line = line.split(' ')
                vlan_id = split_line[3]
                if vlan_id not in vlan_commands:
                    vlan_commands.update({vlan_id: []})
                vlan_commands[vlan_id].append(split_line)
        for key, value in vlan_commands.items():
            vlans_module.vlans.append(CumulusVlanProvider.get_cstate(key, value))
        return vlans_module

