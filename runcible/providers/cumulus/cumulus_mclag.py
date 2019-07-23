from runcible.modules.cumulus_mclag import CumulusMCLAG, CumulusMCLAGResources
from runcible.providers.provider import ProviderBase
from runcible.providers.cumulus.utils import extrapolate_list
from runcible.core.need import NeedOperation as Op


class CumulusMCLAGProvider(ProviderBase):
    provides_for = CumulusMCLAG
    supported_attributes = [
        CumulusMCLAGResources.INTERFACE_IP,
        CumulusMCLAGResources.PEERLINK_INTERFACES,
        CumulusMCLAGResources.SYSMAC,
        CumulusMCLAGResources.PEER_IP,
        CumulusMCLAGResources.PRIORITY,
        CumulusMCLAGResources.BACKUP_IP,
        CumulusMCLAGResources.CLAGD_ARGS
    ]

    def get_cstate(self):
        commands = self.device.retrieve('parsed_commands')
        configuration_dict = {}
        for line in commands:
            if line.startswith('net add interface peerlink.4094'):
                split_line = line.split(' ')
                if split_line.__len__() > 4 and split_line[4] == 'ip':
                    if split_line[5] == 'address':
                        configuration_dict.update({'interface_ip': split_line[6]})
                elif split_line.__len__() > 4 and split_line[4] == 'clag':
                    if split_line[5] == 'backup-ip':
                        configuration_dict.update({'backup_ip': split_line[6]})
                    elif split_line[5] == 'priority':
                        configuration_dict.update({'priority': int(split_line[6])})
                    elif split_line[5] == 'sys-mac':
                        # TODO: Case sensitivity may be an issue here
                        configuration_dict.update({'system_mac_address': split_line[6].lower()})
                    elif split_line[5] == 'backup-ip':
                        configuration_dict.update({'backup_ip': split_line[6]})
                    elif split_line[5] == 'peer-ip':
                        configuration_dict.update({'peer_ip': split_line[6]})
                    elif split_line[5] == 'args':
                        if 'clagd_args' not in configuration_dict:
                            configuration_dict.update({'clagd_args': []})
                        configuration_dict['clagd_args'].append(split_line[6])
            elif line.startswith('net add bond peerlink bond slaves'):
                split_line = line.split(' ')
                split_interfaces = extrapolate_list(split_line[6].split(','))
                if 'peerlink_interfaces' not in configuration_dict:
                    configuration_dict.update({'peerlink_interfaces': []})
                for interface in split_interfaces:
                    configuration_dict['peerlink_interfaces'].append(interface)
        return CumulusMCLAG(configuration_dict)

    def _add_peerlink_interface(self, interface):
        return self.device.send_command(f"net add bond peerlink bond slaves {interface}")

    def _del_peerlink_interface(self, interface):
        return self.device.send_command(f"net del bond peerlink bond slaves {interface}")

    def _clear_peerlink_interface(self):
        return self.device.send_command(f"net del bond peerlink")

    def _set_peerlink_ip(self, ip):
        return self.device.send_command(f"net add interface peerlink.4094 ip address {ip}")

    def _del_peerlink_ip(self):
        return self.device.send_command(f"net del interface peerlink.4094 ip address")

    def _set_sysmac(self, mac):
        return self.device.send_command(f"net add interface peerlink.4094 clag sys-mac {mac}")

    def _del_sysmac(self):
        return self.device.send_command(f"net del interface peerlink.4094 clag sys-mac")

    def _set_peerip(self, peer_ip):
        return self.device.send_command(f"net add interface peerlink.4094 clag peer-ip {peer_ip}")

    def _del_peerip(self):
        return self.device.send_command(f"net del interface peerlink.4094 clag peer-ip")

    def _set_priority(self, priority):
        return self.device.send_command(f"net add interface peerlink.4094 clag priority {priority}")

    def _del_priority(self):
        return self.device.send_command(f"net del interface peerlink.4094 clag priority")

    def _set_backupip(self, backup_ip):
        return self.device.send_command(f"net add interface peerlink.4094 clag backup-ip {backup_ip}")

    def _del_backupip(self):
        return self.device.send_command(f"net del interface peerlink.4094 clag backup-ip")

    def _add_clagdargs(self, arg):
        return self.device.send_command(f"net add interface peerlink.4094 clag args {arg}")

    def _del_clagdargs(self, arg):
        return self.device.send_command(f"net del interface peerlink.4094 clag args {arg}")

    def _clear_clagdargs(self):
        return self.device.send_command(f"net del interface peerlink.4094 clag args")

    def fix_needs(self):
        # All other actions require the peerlink bond to be created, so we need to fufill any needs related to it first
        for need in self.get_needs():
            if need.attribute == CumulusMCLAGResources.PEERLINK_INTERFACES:
                if need.operation == Op.ADD:
                    self._add_peerlink_interface(need.value)
                    self.complete(need)
                elif need.operation == Op.DELETE:
                    self._del_peerlink_interface(need.value)
                    self.complete(need)
                elif need.operation == Op.CLEAR:
                    self._clear_peerlink_interface()
                    self.complete(need)
        # All of the CLAG setup requires the peerlink.4094 interface to both exist and have an IP
        for need in self.get_needs():
            if need.attribute == CumulusMCLAGResources.INTERFACE_IP:
                if need.operation == Op.SET:
                    self._set_peerlink_ip(need.value)
                    self.complete(need)
                elif need.operation == Op.DELETE:
                    self._del_peerlink_ip()
                    self.complete(need)
        # Once the peerlink bond has been created and IP set, we can do everything else
        for need in self.get_needs():
            if need.attribute == CumulusMCLAGResources.SYSMAC:
                if need.operation == Op.SET:
                    self._set_sysmac(need.value)
                    self.complete(need)
                elif need.operation == Op.DELETE:
                    self._del_sysmac()
                    self.complete(need)
            elif need.attribute == CumulusMCLAGResources.PEER_IP:
                if need.operation == Op.SET:
                    self._set_peerip(need.value)
                    self.complete(need)
                elif need.operation == Op.DELETE:
                    self._del_peerip()
                    self.complete(need)
            elif need.attribute == CumulusMCLAGResources.PRIORITY:
                if need.operation == Op.SET:
                    self._set_priority(need.value)
                    self.complete(need)
                elif need.operation == Op.DELETE:
                    self._del_priority()
                    self.complete(need)
            elif need.attribute == CumulusMCLAGResources.BACKUP_IP:
                if need.operation == Op.SET:
                    self._set_backupip(need.value)
                    self.complete(need)
                elif need.operation == Op.DELETE:
                    self._del_backupip()
                    self.complete(need)
            elif need.attribute == CumulusMCLAGResources.CLAGD_ARGS:
                if need.operation == Op.ADD:
                    self._add_clagdargs(need.value)
                    self.complete(need)
                elif need.operation == Op.DELETE:
                    self._del_clagdargs(need.value)
                    self.complete(need)
                elif need.operation == Op.CLEAR:
                    self._clear_clagdargs()
                    self.complete(need)
