from runcible.modules.module import Module
from runcible.core.need import Need
from runcible.core.need import NeedOperation as Op


class InterfaceResources(object):
    NAME = 'name'
    PVID = 'pvid'
    VLANS = 'vlans'
    BPDUGUARD = 'bpduguard'
    PORTFAST = 'portfast'


class Interface(Module):
    parent_module = 'interfaces'
    module_name = 'interface'
    identifier_attribute = InterfaceResources.NAME

    configuration_attributes = {
        InterfaceResources.NAME: {
            'type': str,
            'allowed_operations': []
        },
        "pvid": {
            'type': int,
            'allowed_operations': [Op.SET, Op.DELETE]
        },
        InterfaceResources.BPDUGUARD: {
            'type': bool,
            'allowed_operations': [Op.SET],
            # 'default': False
        },
        InterfaceResources.PORTFAST: {
            'type': bool,
            'allowed_operations': [Op.SET]
        },
        InterfaceResources.VLANS: {
            'type': list,
            'sub_type': int,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR]
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
