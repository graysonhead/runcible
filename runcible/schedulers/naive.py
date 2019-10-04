from runcible.schedulers.scheduler import SchedulerBase
from runcible.core.terminalcallbacks import TermCallback
import yaml


class NaiveScheduler(SchedulerBase):
    scheduler_name = 'naive'
    """
    The naive scheduler runs each executor instance in the order it receives them, without error checking or rollback
    """

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