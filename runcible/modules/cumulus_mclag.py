from runcible.modules.module import Module
from runcible.core.need import NeedOperation as Op


class CumulusMCLAGResources(object):
    SYSMAC = 'system_mac_address'
    PEERLINK_INTERFACES = 'peerlink_interfaces'
    PRIORITY = 'priority'
    BACKUP_IP = 'backup_ip'
    PEER_IP = 'peer_ip'
    INTERFACE_IP = 'interface_ip'
    CLAGD_ARGS = 'clagd_args'


class CumulusMCLAG(Module):
    module_name = 'cumulus_mclag'
    configuration_attributes = {
        CumulusMCLAGResources.SYSMAC: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': ['44:38:39:ff:01:01'],
            'description': 'The emulated mac address of the CLAG cluster'
        },
        CumulusMCLAGResources.PEERLINK_INTERFACES: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR],
            'examples': [['swp47', 'swp48']],
            'description': 'The interfaces used to create the peerlink bond'
        },
        CumulusMCLAGResources.PRIORITY: {
            'type': int,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': [1000, 0],
            'description': 'The priority of this device in the CLAG cluster'
        },
        CumulusMCLAGResources.BACKUP_IP: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': ['192.168.122.18'],
            'description': 'The backup ip used for the CLAG cluster if the peer_ip is unreachable'
        },
        CumulusMCLAGResources.PEER_IP: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': ['169.254.2.2'],
            'description': 'The CLAG peers ip address'
        },
        CumulusMCLAGResources.INTERFACE_IP: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE],
            'examples': ['169.254.2.1/30'],
            'description': 'The IP address that will be assigned to the peerlink bond for state syncing'
        },
        CumulusMCLAGResources.CLAGD_ARGS: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR],
            'examples': ['--vm'],
            'description': 'Additional arguments passed to the CLAG daemon on startup (such as --vm to enable CLAG in a '
                           'virtual machine'
        }
    }