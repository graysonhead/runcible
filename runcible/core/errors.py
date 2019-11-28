class RuncibleError(Exception):
    """
    Base class for Runcible errors
    """

    def __init__(self, msg):
        self.msg = msg


class RuncibleExecutionError(Exception):
    """
    Raised when an error or anomolous situation occurs during execution
    """
    def __init__(self, msg):
        self.msg = msg


class RuncibleValidationError(RuncibleError):

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return f"<ValidationError: {self.msg}>"


class RuncibleNotConnectedError(RuncibleError):

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg


class RuncibleConnectionError(RuncibleError):

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg


class RuncibleNotImplementedError(RuncibleError):

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg


class RuncibleActionFailure(RuncibleError):

    def __init__(self, provider=None, tasks=None):
        self.provider = provider
        self.tasks = tasks

    def __str__(self):
        return f"Provider {self.provider} has uncorrected needs {self.tasks} after execution completed." \
            f"This is likely a bug in the provider."


class RuncibleClientExecutionError(RuncibleError):

    def __init__(self, msg=None, system=None, command=None):
        self.msg = msg
        self.system = system
        self.command = command

    def __str__(self):
        return f"A command failed to run on '{self.system}' while running command '{self.command}': {self.msg}"


class RuncibleSyntaxError(RuncibleError):

    def __str__(self):
        return self.msg

