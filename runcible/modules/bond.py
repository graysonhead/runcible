from runcible.modules.module import Module
from runcible.core.need import Need, NeedOperation as Op


class BondResources(object):
    NAME = 'name'
    MTU = 'mtu'
    IPV4_ADDRESSES = 'ipv4_addresses'
    IPV4_GATEWAY = 'ipv4_gateway'
    SLAVES = 'slaves'
    PVID = 'pvid'
    VLANS = 'vlans'


class Bond(Module):
    parent_module = 'bonds'
    module_name = 'bond'
    identifier_attribute = BondResources.NAME

    configuration_attributes = {
        BondResources.NAME: {
            'type': str,
            'allowed_operations': []
        },
        BondResources.MTU: {
            'type': int,
            'allowed_operations': [Op.SET, Op.DELETE]
        },
        BondResources.IPV4_ADDRESSES: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR]
        },
        BondResources.SLAVES: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR]
        },
        BondResources.IPV4_GATEWAY: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE]
        },
        BondResources.VLANS: {
            'type': list,
            'sub_type': int,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR]
        },
        BondResources.PVID: {
            'type': int,
            'allowed_operations': [Op.SET, Op.DELETE]
        },
    }

    def __repr__(self):
        return f"<Runcible Module: bond {self.name}>"
