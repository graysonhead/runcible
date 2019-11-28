from runcible.modules.module import Module
from runcible.core.need import Need, NeedOperation as Op


class StaticV4RouteInterfaceResources(object):
    PREFIX = 'prefix'
    GATEWAY_INTERFACE = 'gateway_interface'
    DISTANCE = 'distance'
    DESCRIPTION = 'description'


class StaticV4InterfaceRoute(Module):
    parent_module = 'static_v4_routes'
    module_name = 'static_v4_route'
    identifier_attribute = StaticV4RouteInterfaceResources.PREFIX

    configuration_attributes = {
        StaticV4RouteInterfaceResources.PREFIX: {
            'type': str,
            'allowed_operations': [Op.CREATE, Op.REMOVE],
            'examples': ['10.1.0.0/16', '192.168.1.0/24'],
            'description': 'The prefix used for routing in CIDR notation'
        },
        StaticV4RouteInterfaceResources.GATEWAY_INTERFACE: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': ['eth3'],
            'required': True
        },
        StaticV4RouteInterfaceResources.DISTANCE: {
            'type': int,
            'allowed_operations': [Op.SET],
            'examples': [255, 1],
            'description': 'Administrative distance to the gateway specified'
        },
        StaticV4RouteInterfaceResources.DESCRIPTION: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': "This is a description",
            'description': 'Describe the route'
        }
    }