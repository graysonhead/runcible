from runcible.core.device import Device
from runcible.core.callbacks import CBMethod
from runcible.core.terminalcallbacks import TermCallback
import re


class SchedulerBase(object):

    def __init__(self, fabric_config: dict, device_regex: str):
        self.fabric = fabric_config
        self.regex = device_regex.strip('\'"')
        self.devices = []
        self.set_devices()

    def set_devices(self):
        for key, value in self.fabric.items():
            if re.match(self.regex, key):
                self.devices.append(Device(key, value, callback_method=CBMethod.TERMINAL))

    def apply(self):
        TermCallback.info("The following changes will be applied:")
        for device in self.devices:
            TermCallback.info(f"Device {device.name}:")
            TermCallback.info("==========================================")
            device.plan()
        prompt_to_continue = input("Would you like to apply the changes? y/[n]")
        if prompt_to_continue.lower() == 'y':
            for device in self.devices:
                TermCallback.info(f"Device {device.name}")
                TermCallback.info("==========================================")
                device.execute()

    def run_adhoc_command(self, need):
        if not self.devices:
            TermCallback.error("No devices matched")
            exit(1)
        for device in self.devices:
            TermCallback.info(f"Device {device.name}:")
            TermCallback.info("==========================================")
            device.ad_hoc_command(need)



