from runcible.modules.module import Module


class LLDPResources(object):
    DISCOVER_ADJACENT = 'discover_adjacent'


class LLDP(Module):
    module_name = 'lldp'
    configuration_attributes = {
        LLDPResources.DISCOVER_ADJACENT: {
            'type': bool,
            'allowed_operations': [],
            'examples': [True, False],
            'descripion': ''
        }
    }