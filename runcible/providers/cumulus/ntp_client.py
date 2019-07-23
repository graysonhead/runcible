from runcible.modules.ntp_client import NtpClient, NtpClientResources
from runcible.providers.provider import ProviderBase
from runcible.core.need import NeedOperation as Op


class CumulusNtpClientProvider(ProviderBase):
    provides_for = NtpClient
    supported_attributes = [
        NtpClientResources.INTERFACE,
        NtpClientResources.SERVERS
    ]

    def get_cstate(self):
        commands = self.device.retrieve('parsed_commands')
        configuration_dict = {}
        for line in commands:
            if line.startswith('net add time ntp'):
                split_line = line.split(' ')
                if split_line[4] == 'server':
                    if NtpClientResources.SERVERS not in configuration_dict:
                        configuration_dict.update({NtpClientResources.SERVERS: []})
                    configuration_dict[NtpClientResources.SERVERS].append(split_line[5])
                elif split_line[4] == 'source':
                    configuration_dict.update({'interface': split_line[5]})
        return NtpClient(configuration_dict)

    def _add_server(self, server):
        return self.device.send_command(f"net add time ntp server {server} iburst")

    def _del_server(self, server):
        return self.device.send_command(f"net del time ntp server {server}")

    def _clear_server(self):
        return self.device.send_command(f"net del time ntp server")

    def _set_interface(self, interface):
        return self.device.send_command(f"net add time ntp source {interface}")

    def _del_interface(self, interface):
        return self.device.send_command(f"net del time ntp source")

    def fix_needs(self):
        for need in self.get_needs():
            if need.attribute is NtpClientResources.SERVERS:
                if need.operation == Op.ADD:
                    self._add_server(need.value)
                    self.complete(need)
                elif need.operation == Op.DELETE:
                    self._del_server(need.value)
                    self.complete(need)
                elif need.operation == Op.CLEAR:
                    self._clear_server()
                    self.complete(need)
            if need.attribute is NtpClientResources.INTERFACE:
                if need.operation == Op.SET:
                    self._set_interface(need.value)
                    self.complete(need)
                elif need.operation == Op.DELETE:
                    self._del_interface()
                    self.complete(need)
