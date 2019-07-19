from runcible.modules.module import Module
from runcible.core.need import NeedOperation as Op


class NtpClientResources(object):
    SERVERS = 'servers'
    INTERFACE = 'interface'


class NtpClient(Module):
    module_name = 'ntp_client'
    configuration_attributes = {
        NtpClientResources.SERVERS: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.DELETE, Op.SET, Op.ADD, Op.CLEAR]
        },
        NtpClientResources.INTERFACE: {
            'type': str,
            'allowed_operations': [Op.DELETE, Op.SET]
        }
    }

    def __repr__(self):
        return f"<Runcible Module: ntp_client>"
