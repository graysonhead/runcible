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
    CLAG_ID = 'clag_id'


class Bond(Module):
    parent_module = 'bonds'
    module_name = 'bond'
    identifier_attribute = BondResources.NAME

    configuration_attributes = {
        BondResources.NAME: {
            'type': str,
            'allowed_operations': [Op.CREATE, Op.REMOVE],
            'examples': ['po1', 'bond0'],
            'description': "Name of the bond"
        },
        BondResources.MTU: {
            'type': int,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': [1500, 9000],
            'description': "Sets the maximum allowed MTU for the bond"
        },
        BondResources.IPV4_ADDRESSES: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR],
            'examples': [['192.168.1.2/24', '192.168.1.3/24'], ['10.2.3.2/24']],
            'description': 'A list of IPV4 addresses of the bond in CIDR notation'
        },
        BondResources.SLAVES: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR],
            'examples': [['swp1', 'swp2'], ['ge0/0/1', 'ge0/0/2']],
            'description': 'A list of member interfaces that are slaves in the bond'
        },
        BondResources.IPV4_GATEWAY: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': ['192.168.1.1', '10.2.3.1'],
            'description': 'The IPV4 default gateway for the bond'
        },
        BondResources.VLANS: {
            'type': list,
            'sub_type': int,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR],
            'examples': [[1, 2, 3, 4], [200, 201, 202]],
            'description': 'A lit of tagged vlans on the bond'
        },
        BondResources.PVID: {
            'type': int,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': [1, 2, 3, 4000],
            'description': 'The untagged or PVID vlan on the bond'
        },
        BondResources.CLAG_ID: {
            'type': int,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': [1, 2],
            'description': 'The CLAG ID of the bond'
        }
    }

    def __repr__(self):
        return f"<Runcible Module: bond {self.name}>"
