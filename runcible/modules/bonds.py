from runcible.modules.module_array import ModuleArray
from runcible.modules.bond import Bond


class Bonds(ModuleArray):
    module_name = "bonds"
    sub_module = Bond
    sort_key = 'name'
