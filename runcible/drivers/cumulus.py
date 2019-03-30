from runcible.providers.cumulus.system import CumulusSystemProvider
from runcible.drivers.driver import DriverBase


class CumulusDriver(DriverBase):
    driver_name = "cumulus"

    module_provider_map = {
        "system": CumulusSystemProvider
    }