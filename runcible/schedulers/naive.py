from runcible.schedulers.scheduler import SchedulerBase

class NaiveScheduler(SchedulerBase):
    """
    The naive scheduler runs each executor instance in the order it receives them, without error checking or rollback
    """




