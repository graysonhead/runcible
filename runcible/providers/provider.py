

class ProviderBase(object):
    _provides_for=None

    def __init__(self, device_object):
        """
        This class has two methods: get_cstate and execute_needs which fetch the current state from the
        system, and executes needs from it's parent device instance.

        :param device_object:
            When created by it's parent device object, the device object should inject itself here so this
            instance can call it's methods
        """
        self.device = device_object

