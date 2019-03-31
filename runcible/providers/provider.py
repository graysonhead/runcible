

class ProviderBase(object):
    _provides_for=None

    def __init__(self, module_instance):
        """
        This class has two methods: get_cstate and execute_needs which fetch the current state from the
        system, and executes needs from it's parent device instance.

        :param module_instance:
            When created by it's parent module object, the module should inject self into
            this instance so the provider can make use of it's client functions
        """
        self.module = module_instance

