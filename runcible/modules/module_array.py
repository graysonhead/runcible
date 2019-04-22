from runcible.core.errors import ValidationError


class ModuleArray(object):
    module_name = ''
    configuration_attributes = {}

    def __init__(self, config_dictionary):
        """
        This class is a container for multiple modules of the same type grouped under a single key.
        :param config_dictionary:
            The section of the cstate or dstate that is split up and passed to the inner modules.
        """
        