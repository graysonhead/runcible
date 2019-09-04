from runcible.providers.provider_array import ProviderArrayBase
from runcible.providers.cumulus.bond import CumulusBondProvider
from runcible.modules.bonds import Bonds
from runcible.modules.bond import BondResources
from runcible.core.need import NeedOperation as Op
import copy


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

    def fix_needs(self):
        needed_actions = copy.deepcopy(self.needed_actions)
        for need in needed_actions:
            if need.operation == Op.CREATE:
                self._create_module(need.attribute)
                self.complete(need)
            elif need.operation == Op.REMOVE:
                self._remove_module(need.attribute)
                self.complete(need)
            if need.attribute == BondResources.SLAVES:
                self.sub_provider.fix_need(need)
        needed_actions = copy.deepcopy(self.needed_actions)
        for need in needed_actions:
            if self.sub_module_provider:
                self.sub_provider.fix_need(need)
