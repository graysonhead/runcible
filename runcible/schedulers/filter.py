from runcible.schedulers.scheduler import SchedulerBase
from runcible.core.terminalcallbacks import TermCallback
import asyncio


async def async_device_plan(device):
    await device_plan_wrapper(device)
    return device


async def device_plan_wrapper(device):
    TermCallback.info(f"Device {device.name}")
    TermCallback.info("==========================================")
    device.plan()
    return device


class FilterScheduler(SchedulerBase):
    scheduler_name = 'filter'
    """
    The filter scheduler attempts to execute commands safely by filtering out devices from reach run using labels
    """

    def apply(self):
        TermCallback.info("The following changes will be applied:")
        loop = asyncio.get_event_loop()
        plan_tasks = []
        for device in self.devices:
            # planned_devices = asyncio.run(asyncio.gather(async_device_plan(device)))
            plan_tasks.append(async_device_plan(device))
        planned_devices = loop.run_until_complete(asyncio.gather(*plan_tasks))
        loop.close()


        prompt_to_continue = input("Would you like to apply the changes? y/[n]")
