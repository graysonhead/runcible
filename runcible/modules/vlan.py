from runcible.core.need import NeedOperation as Op
from runcible.modules.module import Module


class VlanResources(object):
    NAME = 'name'
    ID = 'id'
    IPV4_ADDRESS = 'ipv4_address'
    IPV4_GATEWAY = 'ipv4_gateway'
    MTU = 'mtu'


class Vlan(Module):
    module_name = 'vlan'
    identifier_attribute = VlanResources.ID
    configuration_attributes = {
        VlanResources.NAME: {
            'type': str,
            'allowed_operations': [Op.DELETE, Op.SET]
        },
        VlanResources.ID: {
            'type': int,
            'allowed_operations': [Op.DELETE, Op.ADD]
        },
        VlanResources.IPV4_ADDRESS: {
            'type': str,
            'allowed_operations': [Op.DELETE, Op.SET]
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
