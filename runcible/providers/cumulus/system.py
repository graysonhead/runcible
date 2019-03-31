from runcible.modules.system import System
from runcible.providers.provider import ProviderBase


class CumulusSystemProvider(ProviderBase):
    provides_for = System

    def get_cstate(self):
        hostname = self._get_hostname()
        return System({'hostname': hostname})

    def _get_hostname(self):
        return self.device.send_command('hostname').strip()
