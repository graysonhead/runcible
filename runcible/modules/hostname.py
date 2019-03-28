from runcible.modules.module import Module

class Hostname(Module):
    module_name='hostname'
    configuration_attributes = {
        "hostname": {
            'type': str
        }
    }