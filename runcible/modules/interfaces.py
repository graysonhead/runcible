from runcible.modules.module_array import ModuleArray
from runcible.modules.interface import Interface
from runcible.core.need import Need
from runcible.core.need import NeedOperation as Op


class Interfaces(ModuleArray):
    module_name = 'interfaces'
    sub_module = Interface
    sort_key = 'name'

