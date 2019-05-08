from runcible.providers.provider import ProviderBase
from runcible.modules.vlan import VlanResources
from runcible.core.need import NeedOperation as Op


class CumulusVlanProvider(ProviderBase):
    supported_attributes = ['id']

    def _create_vlan(self, vlan):
        return self.device.send_command(f"net add bridge bridge vids {vlan}")

    def _remove_vlan(self, vlan):
        return self.device.send_command(f"net del bridge bridge vids {vlan}")

    def fix_need(self, need):
        if need.attribute == VlanResources.ID:
            if need.operation == Op.ADD:
                pass

