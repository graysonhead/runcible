from runcible.modules.interface import Interface, InterfaceResources
from runcible.providers.provider import ProviderBase
from runcible.core.need import NeedOperation as Op


class CumulusInterfaceProvider:
    supported_attributes = [
        'pvid',
        'portadminedge',
        'bpduguard'
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
            if command[0] == 'stp':
                if command[1] == 'bpduguard':
                    interface_config.update({InterfaceResources.BPDUGUARD: True})
                if command[1] == 'portadminedge':
                    interface_config.update({InterfaceResources.PORTFAST: True})

        interface_config.update({'name': name})
        return Interface(interface_config)

    @staticmethod
    def _set_pvid(provider, interface: str, pvid: int):
        return provider.device.send_command(f"net add interface {interface} bridge pvid {pvid}")

    @staticmethod
    def _delete_pvid(provider, interface: str):
        return provider.device.send_command(f"net del interface {interface} bridge pvid")

    @staticmethod
    def _set_bpduguard(provider, interface: str, value: bool):
        if value:
            arg = "add"
        else:
            arg = "del"
        return provider.device.send_command(f"net {arg} interface {interface} stp bpduguard")

    @staticmethod
    def _set_portfast(provider, interface: str, value: bool):
        if value:
            arg = "add"
        else:
            arg = "del"
        return provider.device.send_command(f"net {arg} interface {interface} stp portadminedge")

    @staticmethod
    def fix_need(provider, need):
        if need.attribute is InterfaceResources.PVID:
            if need.operation is Op.SET:
                CumulusInterfaceProvider._set_pvid(provider, need.module, need.value)
                provider.complete(need)
            elif need.operation is Op.DELETE:
                CumulusInterfaceProvider._delete_pvid(provider, need.module)
                provider.complete(need)
        if need.attribute is InterfaceResources.BPDUGUARD:
            CumulusInterfaceProvider._set_bpduguard(provider, need.module, need.value)
            provider.complete(need)
        if need.attribute is InterfaceResources.PORTFAST:
            CumulusInterfaceProvider._set_portfast(provider, need.module, need.value)
            provider.complete(need)
