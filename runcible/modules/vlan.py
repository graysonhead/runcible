from runcible.core.need import NeedOperation as Op
from runcible.modules.module import Module


class VlanResources(object):
    NAME = 'name'
    ID = 'id'
    IPV4_ADDRESSES = 'ipv4_addresses'
    IPV4_GATEWAY = 'ipv4_gateway'
    MTU = 'mtu'


class Vlan(Module):
    module_name = 'vlan'
    identifier_attribute = VlanResources.ID
    configuration_attributes = {
        VlanResources.ID: {
            'type': int,
            'allowed_operations': [Op.CREATE, Op.REMOVE]
        },
        VlanResources.NAME: {
            'type': str,
            'allowed_operations': [Op.DELETE, Op.SET]
        },
        VlanResources.IPV4_ADDRESSES: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.DELETE, Op.SET, Op.ADD, Op.CLEAR]
        },
        VlanResources.IPV4_GATEWAY: {
            'type': str,
            'allowed_operations': [Op.DELETE, Op.SET]
        },
        VlanResources.MTU: {
            'type': int,
            'allowed_operations': [Op.DELETE, Op.SET]
        }
    }

    def __repr__(self):
        return f"<Runcible Module: vlan {self.id}>"
