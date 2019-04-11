from runcible.modules.system import System, SystemResources
from runcible.providers.provider import ProviderBase
from runcible.core.need import NeedOperation as Op


class CumulusSystemProvider(ProviderBase):
    provides_for = System

    def get_cstate(self):
        hostname = self._get_hostname()
        return System({'hostname': hostname})

    def _get_hostname(self):
        return self.device.send_command('hostname').strip()

    def _set_hostname(self, hostname):
        return self.device.send_command(f"net add hostname {hostname}")

    def fix_needs(self):
        for need in self.needed_actions:
            if need.resource is SystemResources.HOSTNAME:
                if need.operation is Op.SET:
                    self._set_hostname(need.value)
                    self.complete(need)
