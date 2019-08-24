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
            'allowed_operations': [Op.DELETE, Op.SET, Op.ADD, Op.CLEAR],
            'examples': [['0.pool.ntp.org', '1.pool.ntp.org', '2.pool.ntp.org']],
            'description': 'A list of servers hostname or IP addresses used for NTP'
        },
        NtpClientResources.INTERFACE: {
            'type': str,
            'allowed_operations': [Op.DELETE, Op.SET],
            'examples': ['swp1', 'eth0'],
            'description': 'Interface used for NTP'
        }
    }

    def __repr__(self):
        return f"<Runcible Module: ntp_client>"
