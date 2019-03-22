class NaiveScheduler(object):
    """
    The naive scheduler runs each executor instance in the order it receives them, without error checking or rollback
    """

    def __init__(self, executors):
        self.executors = executors


