from runcible.modules.interface import Interface, InterfaceResources
from runcible.providers.provider import ProviderBase
from runcible.core.need import NeedOperation as Op


class CumulusInterfaceProvider:

    @staticmethod
    def _set_pvid(provider, interface: str, pvid: int):
        return provider.device.send_command(f"net add interface {interface} bridge pvid {pvid}")

    @staticmethod
    def _delete_pvid(provider, interface: str):
        return provider.device.send_command(f"net del interface {interface} bridge pvid")

    @staticmethod
    def fix_need(provider, need):
        if need.sub_resource is InterfaceResources.PVID:
            if need.operation is Op.SET:
                CumulusInterfaceProvider._set_pvid(provider, need.resource, need.value)
                provider.complete(need)
            elif need.operation is Op.DELETE:
                CumulusInterfaceProvider._delete_pvid(provider, need.resource)
                provider.complete(need)
