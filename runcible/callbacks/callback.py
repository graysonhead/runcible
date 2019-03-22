
class Callback(object):
    """
    All callback classes inherit from this one. Has methods that are called by the executor and providers.

    An instance of the callback class is created and attached to each executor instance, it stores messages to be
    returned to the user at the end of each run. Each instance is self-contained to make threading easier for different
    schedulers.
    """

    def fatal_failure(self, msg):
        raise NotImplementedError