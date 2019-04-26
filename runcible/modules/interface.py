from runcible.modules.module import Module
from runcible.core.need import Need
from runcible.core.need import NeedOperation as Op


class InterfaceResources(object):
    PVID = 'pvid'


class Interface(Module):
    module_name = 'interface'
    configuration_attributes = {
        "name": {
            'type': str,
            'allowed_operations': []
        },
        "pvid": {
            'type': int,
            'allowed_operations': [Op.SET, Op.DELETE]
        }
    }

    def determine_needs(self, other):
        """
        Iterate through attributes of two instances and determine needed actions

        :param other:
            Other instance of this class to compare.

        :return:
            A list of needs
        """
        needs_list = []
        if self.pvid is False and other.pvid:
            needs_list.append(Need(
                InterfaceResources.PVID,
                Op.DELETE
            ))
        elif self.pvid != other.pvid:
            needs_list.append(Need(
                InterfaceResources.PVID,
                Op.SET,
                value=self.pvid
            ))
        return needs_list

    def __repr__(self):
        return f"<Runcible Module: interface {self.name}>"