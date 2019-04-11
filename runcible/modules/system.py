from runcible.modules.module import Module, Need
from runcible.core.need import NeedOperation as Op


class SystemResources(object):
    HOSTNAME = 'hostname'


class System(Module):
    module_name = 'system'
    configuration_attributes = {
        "hostname": {
            'type': str,
            'allowed_operations': [Op.SET]
        }
    }

    def determine_needs(self, other):
        """
        Iterate through the attributes of two instances, and determine what actions are needed to make the other match
        self

        :param other:
            The other instance to compare this class against.

        :return:
            None, this method adds needed action to self.needs
        """
        needs_list = []
        if self.hostname != other.hostname:
            needs_list.append(Need(
                SystemResources.HOSTNAME,
                Op.SET,
                value=self.hostname
            ))
        return needs_list
