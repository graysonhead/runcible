from runcible.providers.sub_provider import SubProviderBase
from runcible.modules.vlan import VlanResources, Vlan
from runcible.core.need import NeedOperation as Op


class CumulusVlanProvider(SubProviderBase):
    provides_for = Vlan
    supported_attributes = ['id']

    def _create_vlan(self, vlan):
        return self.device.send_command(f"net add bridge bridge vids {vlan}")

    def _remove_vlan(self, vlan):
        return self.device.send_command(f"net del bridge bridge vids {vlan}")

    def fix_need(self, need):
        if need.attribute == VlanResources.ID:
            if need.operation == Op.ADD:
                pass

