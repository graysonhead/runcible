from runcible.core.need import NeedOperation as Op
from runcible.modules.module import Module


class VlanResources(object):
    NAME = 'name'
    ID = 'id'


class Vlan(Module):
    module_name = 'vlan'
    configuration_attributes = {
        VlanResources.NAME: {
            'type': str,
            'allowed_operations': [Op.DELETE, Op.ADD, Op.SET]
        },
        VlanResources.ID: {
            'type': int,
            'allowed_operations': [Op.DELETE, Op.ADD]
        }
    }

    def __repr__(self):
        return f"<Runcible Module: vlan {self.id}>"
