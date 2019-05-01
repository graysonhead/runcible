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
        if getattr(self, 'pvid', None) is not None:
            if self.pvid is False:
                if getattr(other, 'pvid', None) is not None:
                    needs_list.append(Need(
                        self.name,
                        Op.DELETE,
                        sub_resource=InterfaceResources.PVID
                    ))
            elif self.pvid != getattr(other, 'pvid', None):
                needs_list.append(Need(
                    self.name,
                    Op.SET,
                    sub_resource=InterfaceResources.PVID,
                    value=self.pvid
                ))
        return needs_list

    def __repr__(self):
        return f"<Runcible Module: interface {self.name}>"
