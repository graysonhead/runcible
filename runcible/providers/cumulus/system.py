from runcible.modules.system import System, SystemResources
from runcible.providers.provider import ProviderBase
from runcible.core.need import NeedOperation as Op


class CumulusSystemProvider(ProviderBase):
    provides_for = System
    supported_attributes = [
        'hostname',
        'dns'
    ]

    def get_cstate(self):
        # TODO: Make this like all the other cumulus providers and retrieve the stored commands list
        hostname = self._get_hostname()
        return System({'hostname': hostname})

    def _get_hostname(self):
        return self.device.send_command('net show hostname').strip()

    def _set_hostname(self, hostname):
        return self.device.send_command(f"net add hostname {hostname}")

    def fix_needs(self):
        for need in self.needed_actions:
            if need.attribute is SystemResources.HOSTNAME:
                if need.operation is Op.SET:
                    self._set_hostname(need.value)
                    self.complete(need)
