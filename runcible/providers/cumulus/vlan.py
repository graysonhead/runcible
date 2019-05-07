from runcible.providers.provider import ProviderBase


class CumulusVlanProvider(ProviderBase):
    supported_resources = ['id']

    def fix_need(self, need):
        pass
