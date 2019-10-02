from runcible.modules.lldp import LLDP
from runcible.providers.provider import ProviderBase
from runcible.labels.adjacent_to import AdjacentTo


class LLDPProvider(ProviderBase):
    provides_for = LLDP
    supported_attributes = []

    def get_cstate(self):
        # self.device.labels.append(AdjacentTo({
        #     "device": "dist2",
        #     "port": "swp2"
        # }))
        return LLDP({})