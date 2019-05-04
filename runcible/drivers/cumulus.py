from runcible.providers.cumulus.system import CumulusSystemProvider
from runcible.providers.cumulus.interfaces import CumulusInterfacesProvider
from runcible.providers.cumulus.vlans import CumulusVlansProvider
from runcible.drivers.driver import DriverBase
from runcible.providers.cumulus.utils import pre_parse_commands



class CumulusDriver(DriverBase):
    driver_name = "cumulus"

    module_provider_map = {
        "system": CumulusSystemProvider,
        "interfaces": CumulusInterfacesProvider,
        "vlans": CumulusVlansProvider
    }
    post_exec_tasks = [
        'net commit'
    ]

    @staticmethod
    def pre_plan_tasks(device):
        commands = device.send_command("net show configuration commands", memoize=True)
        pre_parsed_commands = pre_parse_commands(commands.split("\n"))
        device.store('parsed_commands', pre_parsed_commands)
