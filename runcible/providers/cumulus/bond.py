from runcible.modules.bond import Bond, BondResources
from runcible.providers.sub_provider import SubProviderBase
from runcible.core.need import NeedOperation as Op
from runcible.providers.cumulus.utils import extrapolate_list


class CumulusBondProvider(SubProviderBase):
    provides_for = Bond
    supported_attributes = [
        BondResources.NAME,
        BondResources.SLAVES,
        BondResources.MTU,
        BondResources.IPV4_ADDRESSES,
        BondResources.IPV4_GATEWAY,
        BondResources.VLANS,
        BondResources.PVID,
        BondResources.CLAG_ID
    ]

    @staticmethod
    def get_cstate(name, bond_commands):
        interface_config = {}
        interface_config.update({'name': name})
        for command in bond_commands:
            if command[1] == 'slaves':
                if 'slaves' not in interface_config:
                    interface_config.update({'slaves': []})
                slave_list = extrapolate_list(command[2].split(','))
                for slave in slave_list:
                    interface_config['slaves'].append(slave)
            elif command[0] == 'mtu':
                interface_config.update({BondResources.MTU: command[1]})
            elif command[0] == 'ip':
                if command[1] == 'address':
                    if BondResources.IPV4_ADDRESSES not in interface_config:
                        interface_config.update({BondResources.IPV4_ADDRESSES: []})
                    interface_config[BondResources.IPV4_ADDRESSES].append(command[2])
                if command[1] == 'gateway':
                    interface_config.update({BondResources.IPV4_GATEWAY: command[2]})
            elif command[0] == 'bridge':
                if command[1] == 'pvid':
                    interface_config.update({BondResources.PVID: command[2]})
                elif command[1] == 'vids':
                    interface_config.update({
                        BondResources.VLANS: extrapolate_list(command[2].split(','), int_out=True)
                    })
            elif command[0] == 'clag':
                interface_config.update({BondResources.CLAG_ID: int(command[2])})

        return Bond(interface_config)

    def _add_slave(self, bond, slave):
        return self.device.send_command(f"net add bond {bond} bond slaves {slave}")

    def _del_slave(self, bond, slave):
        return self.device.send_command(f"net del bond {bond} bond slaves {slave}")

    def _set_mtu(self, bond, mtu):
        return self.device.send_command(f"net add bond {bond} mtu {mtu}")

    def _del_mtu(self, bond):
        return self.device.send_command(f"net del bond {bond} mtu")

    def _add_ipv4_address(self, bond, address):
        return self.device.send_command(f"net add bond {bond} ip address {address}")

    def _del_ipv4_address(self, bond, address):
        return self.device.send_command(f"net del bond {bond} ip address {address}")

    def _clear_ipv4_address(self, bond):
        return self.device.send_command(f"net del bond {bond} ip address")

    def _set_ipv4_gateway(self, bond, gateway):
        return self.device.send_command(f"net add bond {bond} ip gateway {gateway}")

    def _del_ipv4_gateway(self, bond):
        return self.device.send_command(f"net del bond {bond} ip gateway")

    def _add_vid(self, bond, vid):
        return self.device.send_command(f"net add bond {bond} bridge vids {vid}")

    def _del_vid(self, bond, vid):
        return self.device.send_command(f"net del bond {bond} bridge vids {vid}")

    def _clear_vid(self, bond):
        return self.device.send_command(f"net del bond {bond} bridge vids")

    def _set_pvid(self, bond, pvid):
        return self.device.send_command(f"net add bond {bond} bridge pvid {pvid}")

    def _del_pvid(self, bond):
        return self.device.send_command(f"net add bond {bond} bridge pvid")

    def _set_clag_id(self, bond, clag_id):
        return self.device.send_command(f"net add bond {bond} clag id {clag_id}")

    def _del_clag_id(self, bond):
        return self.device.send_command(f"net add bond {bond} clag id")

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
        elif need.attribute == BondResources.IPV4_ADDRESSES:
            if need.operation == Op.ADD:
                self._add_ipv4_address(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._del_ipv4_address(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.CLEAR:
                self._clear_ipv4_address(need.module)
                self.complete(need)
        elif need.attribute == BondResources.IPV4_GATEWAY:
            if need.operation == Op.SET:
                self._set_ipv4_gateway(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._del_ipv4_gateway(need.module)
                self.complete(need)
        elif need.attribute == BondResources.VLANS:
            if need.operation == Op.ADD:
                self._add_vid(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._del_vid(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.CLEAR:
                self._clear_vid(need.module)
                self.complete(need)
        elif need.attribute == BondResources.PVID:
            if need.operation == Op.SET:
                self._set_pvid(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._del_pvid(need.module)
                self.complete(need)
        elif need.attribute == BondResources.CLAG_ID:
            if need.operation == Op.SET:
                self._set_clag_id(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._del_clag_id(need.module)
                self.complete(need)

