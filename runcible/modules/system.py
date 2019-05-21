from runcible.modules.module import Module
from runcible.core.need import Need
from runcible.core.need import NeedOperation as Op


class SystemResources(object):
    HOSTNAME = 'hostname'
    DNS = 'dns'


class System(Module):
    module_name = 'system'
    configuration_attributes = {
        SystemResources.HOSTNAME: {
            'type': str,
            'allowed_operations': [Op.SET]
        },
        SystemResources.DNS: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR]
        }
    }