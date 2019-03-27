class Device(object):
    """
    A device represents a single network device in Runcible. A device will have:
        - A connection method (such as SSH)
        - A driver plugin (such as cumulus)
        - Current State
        - Desired State
    """

    def __init__(self, name):
        self.name = name
        self.meta = {}
        self.modules = {}
        self.callback =

    def load_dstate(self, dstate):
        if not isinstance(dstate, dict):