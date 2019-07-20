from runcible.modules.module import Module
from runcible.core.need import Need, NeedOperation as Op


class BondResources(object):
    NAME = 'name'
    MTU = 'mtu'
    IPV4_ADDRESS = 'ipv4_address'
    SLAVES = 'slaves'


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
        BondResources.IPV4_ADDRESS: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR]
        },
        BondResources.SLAVES: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR]
        }
    }

    def __repr__(self):
        return f"<Runcible Module: bond {self.name}>"
