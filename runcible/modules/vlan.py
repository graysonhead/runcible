from runcible.core.need import NeedOperation as Op
from runcible.modules.module import Module


class VlanResources(object):
    NAME = 'name'
    ID = 'id'
    IPV4_ADDRESSES = 'ipv4_addresses'
    IPV4_GATEWAY = 'ipv4_gateway'
    MTU = 'mtu'


class Vlan(Module):
    # module_name = 'vlan'
    identifier_attribute = VlanResources.ID
    configuration_attributes = {
        VlanResources.ID: {
            'type': int,
            'allowed_operations': [Op.CREATE, Op.REMOVE],
            'examples': [2, 20, 4094],
            'description': 'The VLAN id of the VLAN'
        },
        VlanResources.NAME: {
            'type': str,
            'allowed_operations': [Op.DELETE, Op.SET],
            'examples': ['office_vlan'],
            'description': 'The symbolic name of the vlan'
        },
        VlanResources.IPV4_ADDRESSES: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.DELETE, Op.SET, Op.ADD, Op.CLEAR],
            'examples': [['192.168.1.2/24', '192.168.1.3/24'], ['10.2.3.2/24']],
            'description': 'A list of IPV4 addresses of the interface in CIDR notation'
        },
        VlanResources.IPV4_GATEWAY: {
            'type': str,
            'allowed_operations': [Op.DELETE, Op.SET],
            'examples': ['192.168.1.1', '10.2.3.1'],
            'description': 'The IPV4 default gateway for the interface'
        },
        VlanResources.MTU: {
            'type': int,
            'allowed_operations': [Op.DELETE, Op.SET],
            'examples': [1500, 9000],
            'description': 'The maximum MTU of the interface'
        }
    }

    def __repr__(self):
        return f"<Runcible Module: vlan {self.id}>"
