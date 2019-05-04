from runcible.modules.module_array import ModuleArray
from runcible.modules.vlan import Vlan
from runcible.core.need import Need
from runcible.core.need import NeedOperation as Op


class Vlans(ModuleArray):
    module_name = 'vlans'
    sub_module = Vlan

    def determine_needs(self, other):
        needs_list = []
        vlans_sorted_left = sorted(self.vlans, key=lambda x: x.id)
        vlans_sorted_right = sorted(self.vlans, key=lambda x: x.id)
        for vlan in vlans_sorted_left:
            right_vlan = list(filter(lambda x: x.id == vlan.id, vlans_sorted_right))[0]
            if not right_vlan:
                needs_list.append(Need(
                    vlan.id,
                    Op.ADD
                ))
            needs_list.extend(vlan.determine_needs(right_vlan))
        return needs_list
