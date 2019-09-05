from runcible.modules.module import Module
from runcible.core.need import Need
from runcible.core.need import NeedOperation as Op


class InterfaceResources(object):
    NAME = 'name'
    PVID = 'pvid'
    VLANS = 'vlans'
    BPDUGUARD = 'bpduguard'
    PORTFAST = 'portfast'
    MTU = 'mtu'
    IPV4_ADDRESSES = 'ipv4_addresses'
    SPEED = 'speed'


class Interface(Module):
    parent_module = 'interfaces'
    module_name = 'interface'
    identifier_attribute = InterfaceResources.NAME

    configuration_attributes = {
        InterfaceResources.NAME: {
            'type': str,
            'allowed_operations': [Op.CREATE, Op.REMOVE],
            'examples': ['swp1', 'ge01/0/1'],
            'description': "The name of the interface"
        },
        InterfaceResources.PVID: {
            'type': int,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': [10, 20, 30],
            'description': "Vlan ID of the untagged PVID vlan for this interface."
        },
        InterfaceResources.BPDUGUARD: {
            'type': bool,
            'allowed_operations': [Op.SET],
            'examples': [False, True],
            'description': "Enables BPDU Guard on the interface"
            # 'default': False
        },
        InterfaceResources.PORTFAST: {
            'type': bool,
            'allowed_operations': [Op.SET],
            'examples': [False, True],
            'description': "Enables spanning tree portfast on the interface"
        },
        InterfaceResources.VLANS: {
            'type': list,
            'sub_type': int,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR],
            'examples': [[1, 10, 15, 50], [20, 30, 40], [20]],
            'description': f"A list of the tagged VLANS trunked to this interface. Depending on the switch and interface "
                           f"mode, this may be mutually exclusive with {InterfaceResources.PVID}."
        },
        InterfaceResources.MTU: {
            'type': int,
            'allowed_operations': [Op.SET],
            'examples': [1500, 9000],
            'description': "Sets the maximum allowed MTU for the interface"
        },
        InterfaceResources.IPV4_ADDRESSES: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR],
            'examples': [['192.168.1.2/24', '192.168.1.3/24'], ['10.2.3.2/24']],
            'description': 'A list of IPV4 addresses of the interface in CIDR notation'
        },
        InterfaceResources.SPEED: {
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
        }
    }

    def get_bool_needs(self, other, attribute):
        # TODO: This could probably be put the parent class, as handling of boolean needs is pretty universal
        needs_list = []
        if getattr(self, attribute, None) is not None:
            if getattr(self, attribute, None) is False and \
                    getattr(other, attribute, None) is True:
                needs_list.append(Need(
                    self.name,
                    attribute,
                    Op.SET,
                    parent_module=self.parent_module,
                    value=False
                ))
            elif getattr(self, attribute, None) is True:
                if getattr(other, attribute, None) is False or \
                        getattr(other, attribute, None) is None:
                    needs_list.append(Need(
                        self.name,
                        attribute,
                        Op.SET,
                        parent_module=self.parent_module,
                        value=True
                    ))
        return needs_list

    def __repr__(self):
        return f"<Runcible Module: interface {self.name}>"
