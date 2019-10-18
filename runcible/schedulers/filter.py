from runcible.schedulers.scheduler import SchedulerBase
from runcible.core.terminalcallbacks import TermCallback
from runcible.labels.adjacent_to import AdjacentTo
import concurrent.futures
import logging
import yaml
logger = logging.getLogger(__name__)

# TODO: parameterize max workers value for scheduler
MAX_WORKERS = 20


def device_task_wrapper(device, operation: str, task: str = ''):
    logger.info(f"Starting thread for device {device.name}")
    getattr(device, operation)(run_callbacks=False)
    logger.info(f"Thread for device {device.name} complete")
    return device


class FilterScheduler(SchedulerBase):
    scheduler_name = 'filter'
    """
    The filter scheduler attempts to execute commands safely by filtering out devices from reach run using labels
    """

    def apply(self):
        planned_devices = []
        # executed_devices = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_device = {executor.submit(device_task_wrapper, device, 'plan'): device for device in self.devices}
            for future in concurrent.futures.as_completed(future_to_device):
                device = future_to_device[future]
                planned_devices.append(device)
                try:
                    data = future.result()
                except Exception as e:
                    raise e
        for device in planned_devices:
            device.run_callbacks("plan")
        TermCallback.info("Execution Order:")
        device_stages = self.filter_devices(planned_devices)
        for stage, devices in device_stages.items():
            TermCallback.info(f"Stage {stage}: {devices}")
        logger.info("Filtering devices to determine run order")
        prompt_to_continue = input("Would you like to apply the changes? y/[n]")
        if prompt_to_continue.lower() == 'y':
            for stage, devices in device_stages.items():
                executed_devices = []
                with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_to_device = {
                        executor.submit(device_task_wrapper, device, 'execute'): device for device in devices
                    }
                    for future in concurrent.futures.as_completed(future_to_device):
                        device = future_to_device[future]
                        executed_devices.append(device)
                        try:
                            data = future.result()
                        except Exception as e:
                            raise e
                for device in executed_devices:
                    device.run_callbacks('execute')

    def filter_devices(self, devices: list):
        counter = 1
        run_set = {}
        filter_list = [adjacency_filter]
        next_set = devices
        while True:
            for filter in filter_list:
                current_set, next_set = self.run_device_filter(next_set, filter)
            run_set.update({counter: current_set})
            counter += 1
            if not next_set:
                break
        return run_set

    def run_device_filter(self, devices: list, filter_function):
        current_run = []
        next_run = []
        current_run.append(devices[0])
        while devices:
            # Use the first device in the list to filter the others
            device = devices.pop(0)
            for other_device in devices:
                if filter_function(device, other_device):
                    # If the device is already in the current run, and the filter passes, do nothing
                    if other_device not in next_run and other_device not in current_run:
                        current_run.append(other_device)
                else:
                    # If the device fails a filter, remove it from current run and defer it to the next run
                    if other_device not in next_run:
                        next_run.append(other_device)
                    if other_device in current_run:
                        current_run.remove(other_device)
        return current_run, next_run


def adjacency_filter(this, other):
    for other_label in other.labels:
        if this.name == other_label.device:
            return False
    return True

