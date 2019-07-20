from runcible.modules.bond import Bond, BondResources
from runcible.providers.sub_provider import SubProviderBase
from runcible.core.need import NeedOperation as Op


class CumulusBondProvider(SubProviderBase):
    provides_for = Bond
    supported_attributes = [
        BondResources.SLAVES,
        BondResources.MTU
    ]

    @staticmethod
    def get_cstate(name, bond_commands):
        interface_config = {}
        interface_config.update({'name': name})
        for command in bond_commands:
            if command[1] == 'slaves':
                if 'slaves' not in interface_config:
                    interface_config.update({'slaves': []})
                interface_config['slaves'].append(command[2])
            elif command[0] == 'mtu':
                interface_config.update({BondResources.MTU: command[1]})

        return Bond(interface_config)

    def _add_slave(self, bond, slave):
        return self.device.send_command(f"net add bond {bond} bond slaves {slave}")

    def _del_slave(self, bond, slave):
        return self.device.send_command(f"net del bond {bond} bond slave")

    def _set_mtu(self, bond, mtu):
        return self.device.send_command(f"net add bond {bond} mtu {mtu}")

    def _del_mtu(self, bond):
        return self.device.send_command(f"net del bond {bond} mtu")

    def fix_need(self, need):
        if need.attribute == BondResources.SLAVES:
            if need.operation == Op.ADD:
                self._add_slave(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._del_slave(need.module, need.value)
                self.complete(need)
        elif need.attribute == BondResources.MTU:
            if need.operation == Op.SET:
                self._set_mtu(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._del_mtu(need.module)
                self.complete(need)
