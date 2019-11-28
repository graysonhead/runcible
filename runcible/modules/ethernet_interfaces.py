from runcible.modules.module_array import ModuleArray
from runcible.modules.ethernet_interface import EthernetInterface


class EthernetInterfaces(ModuleArray):
    module_name = 'ethernet_interfaces'
    sort_key = 'name'
    sub_module = EthernetInterface
