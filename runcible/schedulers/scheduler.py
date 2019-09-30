from runcible.core.device import Device
from runcible.core.callbacks import CBMethod
from runcible.core.terminalcallbacks import TermCallback
import re
import yaml

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
        if not self.devices:
            TermCallback.error(msg="No devices matched.")

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

    def get_cstate(self):
        self.set_devices()
        returned_dict = {}
        for device in self.devices:
            device.plan(mute_callbacks=True)
            returned_dict.update({device.name: device.get_cstate()})
        print(yaml.safe_dump(returned_dict))

    def run_adhoc_command(self, need):
        if not self.devices:
            TermCallback.error("No devices matched")
            exit(1)
        for device in self.devices:
            TermCallback.info(f"Device {device.name}:")
            TermCallback.info("==========================================")
            device.ad_hoc_command(need)



