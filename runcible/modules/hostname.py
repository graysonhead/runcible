from runcible.modules.module import Module, Need
from runcible.core.need import NeedOperation as Op

PLUGIN_PROVIDES = {'hostname': 'Hostname'}


class HostnameResources(object):
    HOSTNAME = 'hostname'


class Hostname(Module):
    module_name='hostname'
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
                HostnameResources.HOSTNAME,
                Op.DELETE
            ))
        elif self.hostname != other.hostname:
            self.needs(Need(
                HostnameResources.HOSTNAME,
                Op.SET,
                value=self.hostname
            ))
