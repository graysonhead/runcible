from runcible.modules.module_array import ModuleArray
from runcible.modules.vlan import Vlan
from runcible.core.need import Need
from runcible.core.need import NeedOperation as Op


class Vlans(ModuleArray):
    module_name = 'vlans'
    sub_module = Vlan
    sort_key = 'id'
