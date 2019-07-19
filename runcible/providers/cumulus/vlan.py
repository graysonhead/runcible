from runcible.providers.sub_provider import SubProviderBase
from runcible.modules.vlan import VlanResources, Vlan
from runcible.core.need import NeedOperation as Op


class CumulusVlanProvider(SubProviderBase):
    provides_for = Vlan
    supported_attributes = [
        VlanResources.ID,
        VlanResources.NAME,
        VlanResources.IPV4_ADDRESSES,
        VlanResources.IPV4_GATEWAY,
        VlanResources.MTU
    ]

    @staticmethod
    def get_cstate(id, vlan_commands):
        configuration_dict = {}
        configuration_dict.update({VlanResources.ID: id})
        for line in vlan_commands:
            if line[4] == 'alias':
                configuration_dict.update({VlanResources.NAME: line[5]})
            elif line[4] == 'mtu':
                configuration_dict.update({VlanResources.MTU: line[5]})
            elif line[4] == 'ip':
                if line[5] == 'address':
                    if VlanResources.IPV4_ADDRESSES not in configuration_dict:
                        configuration_dict.update({VlanResources.IPV4_ADDRESSES: []})
                    configuration_dict[VlanResources.IPV4_ADDRESSES].append(line[6])
                if line[5] == 'gateway':
                    configuration_dict.update({VlanResources.IPV4_GATEWAY: line[6]})
        return Vlan(configuration_dict)

    def _create_vlan(self, vlan):
        return self.device.send_command(f"net add vlan {vlan} vlan-id {vlan}")

    def _remove_vlan(self, vlan):
        return self.device.send_command(f"net del vlan {vlan}")

    def _set_vlan_name(self, vlan, name):
        return self.device.send_command(f"net add vlan {vlan} alias {name}")

    def _del_vlan_name(self, vlan):
        return self.device.send_command(f"net del vlan {vlan} alias")

    def _add_vlan_ipv4_address(self, vlan, address):
        return self.device.send_command(f"net add vlan {vlan} ip address {address}")

    def _del_vlan_ipv4_address(self, vlan, address):
        return self.device.send_command(f"net del vlan {vlan} ip address {address}")

    def _clear_vlan_ipv4_address(self, vlan):
        return self.device.send_command(f"net del vlan {vlan} ip address")

    def _set_ipv4_gateway(self, vlan, gateway):
        return self.device.send_command(f"net add vlan {vlan} ip gateway {gateway}")

    def _del_ipv4_gateway(self, vlan):
        return self.device.send_command(f"net del vlan {vlan} ip gateway")

    def _del_mtu(self, vlan):
        return self.device.send_command(f"net del vlan {vlan} mtu")

    def _set_mtu(self, vlan, mtu):
        return self.device.send_command(f"net add vlan {vlan} mtu {mtu}")

    def fix_need(self, need):
        if need.attribute == VlanResources.ID:
            if need.operation == Op.ADD:
                pass
        elif need.attribute == VlanResources.NAME:
            if need.operation == Op.SET:
                self._set_vlan_name(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._del_vlan_name(need.module)
                self.complete(need)
        elif need.attribute == VlanResources.MTU:
            if need.operation == Op.SET:
                self._set_mtu(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._del_mtu(need.module)
                self.complete(need)
        elif need.attribute == VlanResources.IPV4_ADDRESSES:
            if need.operation == Op.ADD:
                self._add_vlan_ipv4_address(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._del_vlan_ipv4_address(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.CLEAR:
                self._clear_vlan_ipv4_address(need.module)
                self.complete(need)
        elif need.attribute == VlanResources.IPV4_GATEWAY:
            if need.operation == Op.SET:
                self._set_ipv4_gateway(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._del_ipv4_gateway(need.module)
                self.complete(need)

