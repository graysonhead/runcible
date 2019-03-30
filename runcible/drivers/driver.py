from runcible.providers.cumulus.system import CumulusSystemProvider


class DriverBase(object):
    # This is the string you can reference in the meta config to load this driver
    driver_name = ""

    # Maps modules to providers
    module_provider_map = {}

    def load_provider(self, module_name):
        return self.module_provider_map[module_name]