from runcible.core.device import Device
from runcible.core.callbacks import CBMethod
from runcible.core.terminalcallbacks import TermCallback
from runcible.core.plugin_registry import PluginRegistry
import re
import yaml

DEFAULT_SCHEDULER = 'naive'


class SchedulerBase(object):
    scheduler_name = ''

    @classmethod
    def get_scheduler(cls, fabric_config, device_regex):
        scheduler_type = None
        meta_config = fabric_config.get('meta', None)
        if meta_config:
            meta_scheduler = meta_config.get('scheduler', None)
            if meta_scheduler:
                scheduler_type = meta_scheduler.get('type', None)
        if scheduler_type:
            return PluginRegistry.get_scheduler(scheduler_type)(fabric_config, device_regex)
        else:
            return PluginRegistry.get_scheduler(DEFAULT_SCHEDULER)(fabric_config, device_regex)

    def __init__(self, fabric_config: dict, device_regex: str):
        self.meta_config = fabric_config.get('meta', {})
        self.fabric = fabric_config
        # Purge the 'meta' key from the fabric config, if it exists
        try:
            del self.fabric['meta']
        except KeyError:
            pass
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

    def get_labels(self):
        self.set_devices()
        returned_dict = {}
        for device in self.devices:
            device.plan(mute_callbacks=True)
            returned_dict.update({
                device.name: {"meta": {"labels": device.get_labels()}}
            })
        print(yaml.safe_dump(returned_dict))


    def run_adhoc_command(self, need):
        if not self.devices:
            TermCallback.error("No devices matched")
            exit(1)
        for device in self.devices:
            TermCallback.info(f"Device {device.name}:")
            TermCallback.info("==========================================")
            device.ad_hoc_command(need)



