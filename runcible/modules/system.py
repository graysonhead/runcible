from runcible.modules.module import Module, Need
from runcible.core.need import NeedOperation as Op


class SystemResources(object):
    HOSTNAME = 'hostname'


class System(Module):
    module_name= 'system'
    configuration_attributes = {
        "hostname": {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE]
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
        if self.hostname is False:
            self.needs(Need(
                SystemResources.HOSTNAME,
                Op.DELETE
            ))
        elif self.hostname != other.hostname:
            self.needs(Need(
                SystemResources.HOSTNAME,
                Op.SET,
                value=self.hostname
            ))