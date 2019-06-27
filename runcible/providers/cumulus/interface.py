from runcible.modules.interface import Interface, InterfaceResources
from runcible.providers.sub_provider import SubProviderBase
from runcible.core.need import NeedOperation as Op
from runcible.providers.cumulus.utils import extrapolate_list


class CumulusInterfaceProvider(SubProviderBase):
    provides_for = Interface
    supported_attributes = [
        InterfaceResources.BPDUGUARD,
        InterfaceResources.PORTFAST,
        InterfaceResources.PVID,
        InterfaceResources.VLANS
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

        interface_config.update({'name': name})
        return Interface(interface_config)

    def _add_vids(self, interface: str, vids):
        return self.device.send_command(f"net add interface {interface} bridge vids {vids}")

    def _del_vids(self, interface: str, vids):
        return self.device.send_command(f"net del interface {interface} bridge vids {vids}")

    def _set_pvid(self, interface: str, pvid: int):
        return self.device.send_command(f"net add interface {interface} bridge pvid {pvid}")

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
    
# class CumulusInterfaceProviderNot:
#     supported_attributes = [
#         InterfaceResources.BPDUGUARD,
#         InterfaceResources.PORTFAST,
#         InterfaceResources.PVID,
#         InterfaceResources.VLANS
#     ]
#     @staticmethod
#     def get_cstate(name, interface_commands):
#         """
#         This method is called by CumulusInterfacesProvider to generate an Interface module for each set of
#         interface arguments
#         :return:
#         """
#         interface_config = {}
#         for command in interface_commands:
#             if command[0] == 'bridge':
#                 if command[1] == 'pvid':
#                     interface_config.update({'pvid': command[2]})
#                 elif command[1] == 'vids':
#                     interface_config.update({'vlans': extrapolate_list(command[2].split(','), int_out=True)})
#             elif command[0] == 'stp':
#                 if command[1] == 'bpduguard':
#                     interface_config.update({InterfaceResources.BPDUGUARD: True})
#                 elif command[1] == 'portadminedge':
#                     interface_config.update({InterfaceResources.PORTFAST: True})
#
#         interface_config.update({'name': name})
#         return Interface(interface_config)
#
#     @staticmethod
#     def _add_vids(provider, interface: str, vids):
#         return provider.device.send_command(f"net add interface {interface} bridge vids {vids}")
#
#     @staticmethod
#     def _del_vids(provider, interface: str, vids):
#         return provider.device.send_command(f"net del interface {interface} bridge vids {vids}")
#
#     @staticmethod
#     def _set_pvid(provider, interface: str, pvid: int):
#         return provider.device.send_command(f"net add interface {interface} bridge pvid {pvid}")
#
#     @staticmethod
#     def _delete_pvid(provider, interface: str):
#         return provider.device.send_command(f"net del interface {interface} bridge pvid")
#
#     @staticmethod
#     def _set_bpduguard(provider, interface: str, value: bool):
#         if value:
#             arg = "add"
#         else:
#             arg = "del"
#         return provider.device.send_command(f"net {arg} interface {interface} stp bpduguard")
#
#     @staticmethod
#     def _set_portfast(provider, interface: str, value: bool):
#         if value:
#             arg = "add"
#         else:
#             arg = "del"
#         return provider.device.send_command(f"net {arg} interface {interface} stp portadminedge")
#
#     @staticmethod
#     def fix_need(provider, need):
#         if need.attribute == InterfaceResources.PVID:
#             if need.operation == Op.SET:
#                 CumulusInterfaceProvider._set_pvid(provider, need.module, need.value)
#                 provider.complete(need)
#             elif need.operation == Op.DELETE:
#                 CumulusInterfaceProvider._delete_pvid(provider, need.module)
#                 provider.complete(need)
#         elif need.attribute == InterfaceResources.BPDUGUARD:
#             CumulusInterfaceProvider._set_bpduguard(provider, need.module, need.value)
#             provider.complete(need)
#         elif need.attribute == InterfaceResources.PORTFAST:
#             CumulusInterfaceProvider._set_portfast(provider, need.module, need.value)
#             provider.complete(need)
#         elif need.attribute == InterfaceResources.VLANS:
#             if need.operation == Op.ADD:
#                 CumulusInterfaceProvider._add_vids(provider, need.module, need.value)
#                 provider.complete(need)
#             elif need.operation == Op.DELETE:
#                 CumulusInterfaceProvider._del_vids(provider, need.module, need.value)
#                 provider.complete(need)
