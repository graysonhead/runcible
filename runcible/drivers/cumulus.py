from runcible.providers.cumulus.system import CumulusSystemProvider
from runcible.providers.cumulus.interfaces import CumulusInterfacesProvider
from runcible.providers.cumulus.vlans import CumulusVlansProvider
from runcible.providers.cumulus.ntp_client import CumulusNtpClientProvider
from runcible.providers.cumulus.bonds import CumulusBondsProvider
from runcible.protocols.ssh_protocol import SSHProtocol
from runcible.drivers.driver import DriverBase
from runcible.providers.cumulus.utils import pre_parse_commands


class CumulusDriver(DriverBase):
    driver_name = "cumulus"

    module_provider_map = {
        "system": CumulusSystemProvider,
        "interfaces": CumulusInterfacesProvider,
        "vlans": CumulusVlansProvider,
        "ntp_client": CumulusNtpClientProvider,
        "bonds": CumulusBondsProvider
    }

    protocol_map = {
        "ssh": SSHProtocol
    }
    @staticmethod
    def post_exec_tasks(device):
        device.send_command('net commit')

    @staticmethod
    def pre_plan_tasks(device):
        commands = device.send_command("net show configuration commands", memoize=True)
        pre_parsed_commands = pre_parse_commands(commands.split("\n"))
        device.store('parsed_commands', pre_parsed_commands)
