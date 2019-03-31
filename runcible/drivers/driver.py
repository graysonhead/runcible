from runcible.providers.cumulus.system import CumulusSystemProvider


class DriverBase(object):
    # This is the string you can reference in the meta config to load this driver
    driver_name = ""

    # Maps modules to providers
    module_provider_map = {}

    @classmethod
    def load_provider(cls, module_name):
        return cls.module_provider_map[module_name]

    @classmethod
    def __repr__(cls):
        return f"<RuncibleDriver: {cls.driver_name}>"
