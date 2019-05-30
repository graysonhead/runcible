from runcible.core.device import Device
from runcible.core.callbacks import CBMethod
from runcible.core.terminalcallbacks import TermCallback


class SchedulerBase(object):

    def __init__(self, fabric_config: dict):
        self.fabric = fabric_config
        self.devices = []
        self.set_devices()

    def set_devices(self):
        for key, value in self.fabric.items():
            self.devices.append(Device(key, value, callback_method=CBMethod.TERMINAL))

    def plan(self):
        TermCallback.info("The following changes will be applied:")
        for device in self.devices:
            TermCallback.info(f"Device {device.name}:")
            TermCallback.info("==========================================")
            device.plan()
        prompt_to_continue = input("Would you like to apply the changes? y/[n]")
        if prompt_to_continue.lower() == 'y':
            for device in self.devices:
                device.execute()
