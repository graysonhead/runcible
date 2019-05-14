from runcible.modules.module import Module
from runcible.core.need import Need
from runcible.core.need import NeedOperation as Op


class SystemResources(object):
    HOSTNAME = 'hostname'


class System(Module):
    module_name = 'system'
    configuration_attributes = {
        "hostname": {
            'type': str,
            'allowed_operations': [Op.SET]
        }
    }