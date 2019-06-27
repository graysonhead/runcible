from runcible.core.errors import RuncibleNotImplementedError


class SubProviderBase(object):
    provides_for = None
    supported_attributes = []

    def __init__(self, parent_provider, dstate):
        """
        This is fundementally similar to the ProviderBase class, however the subprovider isn't responsible for generating
        cstate (The parent provider is). The SubProvider is only responsible for applying task fixes.

        :param sort_key:
            The name of the sort_key for this instance
        :param parent_provider:
            Parent instance
        :param dstate:
            dstate of object
        """
        self.provider = parent_provider
        self.device = self.provider.device
        self.dstate = dstate

    def complete(self, need):
        self.provider.complete(need)

    def fix_needs(self):
        raise RuncibleNotImplementedError(msg="This provider doesn't implement a fix_needs class")