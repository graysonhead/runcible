from runcible.providers.sub_provider import SubProviderBase
from runcible.modules.vlan import VlanResources, Vlan
from runcible.core.need import NeedOperation as Op


class CumulusVlanProvider(SubProviderBase):
    provides_for = Vlan
    supported_attributes = ['id', 'name']

    @staticmethod
    def get_cstate(id, vlan_commands):
        configuration_dict = {}
        configuration_dict.update({VlanResources.ID: id})
        for line in vlan_commands:
            if line[4] == 'alias':
                configuration_dict.update({VlanResources.NAME: line[5]})
        return Vlan(configuration_dict)

    def _create_vlan(self, vlan):
        return self.device.send_command(f"net add vlan {vlan} vlan-id {vlan}")

    def _remove_vlan(self, vlan):
        return self.device.send_command(f"net del vlan {vlan}")

    def _set_vlan_name(self, vlan, name):
        return self.device.send_command(f"net add vlan {vlan} alias {name}")

    def _del_vlan_name(self, vlan):
        return self.device.send_command(f"net del vlan {vlan} alias")

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

