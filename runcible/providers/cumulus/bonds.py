from runcible.providers.provider_array import ProviderArrayBase
from runcible.providers.cumulus.bond import CumulusBondProvider
from runcible.modules.bonds import Bonds


class CumulusBondsProvider(ProviderArrayBase):
    provides_for = Bonds
    sub_module_provider = CumulusBondProvider

    def _create_module(self, bond):
        pass

    def _remove_module(self, bond):
        return self.device.send_command(f"net del bond {bond}")

    def get_cstate(self):
        commands = self.device.retrieve('parsed_commands')
        bond_commands = {}
        bond_instances = []
        for line in commands:
            split_line = line.split(' ')
            if split_line.__len__() > 2:
                if split_line[2] == 'bond':
                    bond_name = split_line[3]
                    if bond_name not in bond_commands:
                        bond_commands.update({bond_name: []})
                    if split_line.__len__() > 4:
                        truncated_line = split_line[4:]
                        bond_commands[bond_name].append(truncated_line)
        for key, value in bond_commands.items():
            bond_instances.append(CumulusBondProvider.get_cstate(key, value))
        bonds_instance = Bonds({})
        bonds_instance.bonds = bond_instances
        return bonds_instance
