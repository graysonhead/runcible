from runcible.modules.module import Module
from runcible.core.need import Need, NeedOperation as Op


class EthernetInterfaceResources(object):
    NAME = 'name'
    IPV4_ADDRESSES = 'ipv4_addresses'
    IPV6_ADDRESSES = 'ipv6_addresses'
    SPEED = 'speed'
    DUPLEX = 'duplex'
    MTU = 'mtu'


class EthernetInterface(Module):
    parent_module = 'ethernet_interfaces'
    module_name = 'ethernet_interface'
    identifier_attribute = EthernetInterfaceResources.NAME

    configuration_attributes = {
        EthernetInterfaceResources.NAME: {
            'type': str,
            'allowed_operations': [Op.CREATE, Op.REMOVE],
            'examples': ['eth0', 'eth1']
        },
        EthernetInterfaceResources.IPV4_ADDRESSES: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR],
            'examples': [['192.168.1.2/24', '192.168.1.3/24'], ['10.2.3.2/24'], ['dhcp']],
            'description': 'A list of IPV4 addresses of the interface in CIDR notation'
        },
        EthernetInterfaceResources.IPV6_ADDRESSES: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR],
            'examples': [['1::1/10', 'dhcp']],
            'description': 'A list of IPV6 addresses of the interface in CIDR notation'
        },
        EthernetInterfaceResources.SPEED: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': ['1G', '10G', '25G'],
            'description': 'Sets the line speed of the interface',
            'allowed_values': [
                '10',
                '100',
                '1G',
                '2.5G',
                '10G',
                '25G'
            ]
        },
        EthernetInterfaceResources.MTU: {
            'type': int,
            'allowed_operations': [Op.SET],
            'examples': [1500, 9000],
            'description': "Sets the maximum allowed MTU for the interface"
        },
        EthernetInterfaceResources.DUPLEX: {
            'type': str,
            'allowed_operations': [Op.SET],
            'examples': ['auto', 'half', 'full'],
            'description': "Sets the duplex mode of the interface"
        }
    }