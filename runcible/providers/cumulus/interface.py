from runcible.modules.interface import Interface, InterfaceResources
from runcible.providers.sub_provider import SubProviderBase
from runcible.core.need import NeedOperation as Op
from runcible.providers.cumulus.utils import extrapolate_list


class CumulusInterfaceProvider(SubProviderBase):
    provides_for = Interface
    supported_attributes = [
        InterfaceResources.NAME,
        InterfaceResources.PORTFAST,
        InterfaceResources.PVID,
        InterfaceResources.BPDUGUARD,
        InterfaceResources.VLANS,
        InterfaceResources.IPV4_ADDRESSES
    ]

    @staticmethod
    def get_cstate(name, interface_commands):
        """
        This method is called by CumulusInterfacesProvider to generate an Interface module for each set of
        interface arguments
        :return:
        """
        interface_config = {}
        for command in interface_commands:
            if command[0] == 'bridge':
                if command[1] == 'pvid':
                    interface_config.update({'pvid': command[2]})
                elif command[1] == 'vids':
                    interface_config.update({'vlans': extrapolate_list(command[2].split(','), int_out=True)})
            elif command[0] == 'stp':
                if command[1] == 'bpduguard':
                    interface_config.update({InterfaceResources.BPDUGUARD: True})
                elif command[1] == 'portadminedge':
                    interface_config.update({InterfaceResources.PORTFAST: True})
            elif command[0] == 'ip':
                if command[1] == 'address':
                    if not interface_config.get(InterfaceResources.IPV4_ADDRESSES, None):
                        interface_config.update({InterfaceResources.IPV4_ADDRESSES: []})
                    interface_config[InterfaceResources.IPV4_ADDRESSES].append(command[2])
        interface_config.update({'name': name})
        return Interface(interface_config)

    def _add_vids(self, interface: str, vids):
        return self.device.send_command(f"net add interface {interface} bridge vids {vids}")

    def _del_vids(self, interface: str, vids):
        return self.device.send_command(f"net del interface {interface} bridge vids {vids}")

    def _clear_vids(self, interface: str):
        return self.device.send_command(f"net del interface {interface} bridge vids")

    def _set_vids(self, interface: str, vid_list):
        self._clear_vids(interface)
        for vid in vid_list:
            self._add_vids(interface, vid)

    def _set_pvid(self, interface: str, pvid: int):
        return self.device.send_command(f"net add interface {interface} bridge pvid {pvid}")

    def _add_interface_ipv4_address(self, interface, address):
        return self.device.send_command(f"net add interface {interface} ip address {address}")

    def _del_interface_ipv4_address(self, interface, address):
        return self.device.send_command(f"net del interface {interface} ip address {address}")

    def _clear_interface_ipv4_address(self, interface):
        return self.device.send_command(f"net del interface {interface} ip address")

    def _set_ipv4_addresses(self, interface, addresses):
        self._clear_interface_ipv4_address(interface)
        for address in addresses:
            self._add_interface_ipv4_address(interface, address)

    def _delete_pvid(self, interface: str):
        return self.device.send_command(f"net del interface {interface} bridge pvid")

    def _set_bpduguard(self, interface: str, value: bool):
        if value:
            arg = "add"
        else:
            arg = "del"
        return self.device.send_command(f"net {arg} interface {interface} stp bpduguard")

    def _set_portfast(self, interface: str, value: bool):
        if value:
            arg = "add"
        else:
            arg = "del"
        return self.device.send_command(f"net {arg} interface {interface} stp portadminedge")
    
    def fix_need(self, need):
        if need.attribute == InterfaceResources.PVID:
            if need.operation == Op.SET:
                self._set_pvid(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._delete_pvid(need.module)
                self.complete(need)
        elif need.attribute == InterfaceResources.BPDUGUARD:
            self._set_bpduguard(need.module, need.value)
            self.complete(need)
        elif need.attribute == InterfaceResources.PORTFAST:
            self._set_portfast(need.module, need.value)
            self.complete(need)
        elif need.attribute == InterfaceResources.VLANS:
            if need.operation == Op.ADD:
                self._add_vids(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._del_vids(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.CLEAR:
                self._clear_vids(need.module)
                self.complete(need)
            elif need.operation == Op.SET:
                self._set_vids(need.module, need.value)
                self.complete(need)
        elif need.attribute == InterfaceResources.IPV4_ADDRESSES:
            if need.operation == Op.ADD:
                self._add_interface_ipv4_address(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.DELETE:
                self._del_interface_ipv4_address(need.module, need.value)
                self.complete(need)
            elif need.operation == Op.CLEAR:
                self._clear_interface_ipv4_address(need.module)
                self.complete(need)
            elif need.operation == Op.SET:
                self._set_ipv4_addresses(need.module, need.value)
                self.complete(need)
