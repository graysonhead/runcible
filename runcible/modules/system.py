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
            'allowed_operations': [Op.SET],
            'examples': ['hostname', 'hostname.domain.com'],
            'description': "This attribute defines the system's hostname, it can be either a short name or fully "
                           "qualified"
        },
        SystemResources.DNS: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR],
            'examples': [['8.8.8.8', '8.8.4.4'], ['1.1.1.1', '2.2.2.2', '3.3.3.3']],
            'description': "This attribute configures the system resolver, it is a list containing the IP address of "
                           "one or more DNS servers."
        }
    }