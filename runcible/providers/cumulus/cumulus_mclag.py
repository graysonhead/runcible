from runcible.modules.cumulus_mclag import CumulusMCLAG, CumulusMCLAGResources
from runcible.providers.provider import ProviderBase
from runcible.core.need import NeedOperation as Op


class CumulusMCLAGProvider(ProviderBase):
    provides_for = CumulusMCLAG
    supported_attributes = [
        CumulusMCLAGResources.PEERLINK_IP,
        CumulusMCLAGResources.PEERLINK_INTERFACES
    ]

    def get_cstate(self):
