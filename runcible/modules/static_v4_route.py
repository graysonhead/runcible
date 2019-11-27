from runcible.modules.module import Module
from runcible.core.need import Need, NeedOperation as Op


class StaticV4RouteResources(object):
    PREFIX = 'prefix'
    GATEWAY_INTERFACE = 'gateway_interface'
    GATEWAY_IP = 'gateway_ip'
    DISTANCE = 'distance'
    DESCRIPTION = 'description'


class StaticV4Route(Module):
    parent_module = 'static_v4_routes'
    module_name = 'static_v4_route'
    identifier_attribute = StaticV4RouteResources.PREFIX

    configuration_attributes = {
        StaticV4RouteResources.PREFIX: {
            'type': str,
            'allowed_operations': [Op.CREATE, Op.REMOVE],
            'examples': ['10.1.0.0/16', '192.168.1.0/24'],
            'description': 'The prefix used for routing in CIDR notation'
        },
        StaticV4RouteResources.GATEWAY_INTERFACE: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': ['eth0'],
            'description': f'The name of the Interface used for Interface routing. Mutually exclusive with '
            f'{StaticV4RouteResources.GATEWAY_IP}',
            'mutually_exclusive': [StaticV4RouteResources.GATEWAY_IP]
        },
        StaticV4RouteResources.GATEWAY_IP: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': ['10.1.2.3', '192.168.1.1'],
            'mutually_exclusive': [StaticV4RouteResources.GATEWAY_INTERFACE]
        },
        StaticV4RouteResources.DISTANCE: {
            'type': int,
            'allowed_operations': [Op.SET],
            'examples': [255, 1],
            'description': 'Administrative distance to the gateway specified'
        },
        StaticV4RouteResources.DESCRIPTION: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': "This is a description",
            'description': 'Describe the route'
        }
    }