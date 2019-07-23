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
            'allowed_operations': [Op.SET, Op.DELETE]
        },
        CumulusMCLAGResources.PEERLINK_INTERFACES: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR]
        },
        CumulusMCLAGResources.PRIORITY: {
            'type': int,
            'allowed_operations': [Op.SET, Op.DELETE]
        },
        CumulusMCLAGResources.BACKUP_IP: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE]
        },
        CumulusMCLAGResources.PEER_IP: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE]
        },
        CumulusMCLAGResources.INTERFACE_IP: {
            'type': str,
            'allowed_operations': [Op.SET, Op.DELETE]
        },
        CumulusMCLAGResources.CLAGD_ARGS: {
            'type': list,
            'sub_type': str,
            'allowed_operations': [Op.SET, Op.ADD, Op.DELETE, Op.CLEAR]
        }
    }