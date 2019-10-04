from runcible.modules.lldp import LLDP
from runcible.providers.provider import ProviderBase
from runcible.labels.adjacent_to import AdjacentTo


class LLDPProvider(ProviderBase):
    provides_for = LLDP
    supported_attributes = []

    def get_cstate(self):
        neighbors_output = self._get_lldp_neighbors().split('\n')
        self.add_labels(neighbors_output)
        return LLDP({})

    def add_labels(self, input_lines: list):
        for line in input_lines:
            if line.startswith("Interface"):
                interface_string = line.strip("Interface:").strip().split(',')[0]
            elif line.strip().startswith('SysName'):
                sys_name = line.strip().split(' ')[-1]
                self.device.labels.append(
                    AdjacentTo(
                        {
                            "device": sys_name,
                            "port": interface_string
                        }
                    )
                )
            elif line.strip().startswith('MgmtIP'):
                mgmt_ip = line.strip().split(' ')[-1]
                self.device.labels.append(
                    AdjacentTo(
                        {
                            "device": mgmt_ip,
                            "port": interface_string
                        }
                    )
                )

    def _get_lldp_neighbors(self):
        # using the glob format here seems to work even when the high number overruns the number of switchports
        # on the system
        return self.device.send_command("net show lldp swp1-100")