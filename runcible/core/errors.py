class RuncibleError(Exception):
    """
    Base class for Runcible errors
    """

    def __init__(self, msg):
        self.msg = msg


class ValidationError(RuncibleError):

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return f"<ValidationError: {self.msg}>"


class RuncibleConnectionError(RuncibleError):

    def __init(self, msg=None):
        self.msg = msg

    def __str__(self):
        return msg


class ClientExecutionError(RuncibleError):

    def __init__(self, msg=None, system=None, command=None):
        self.msg = msg
        self.system = system
        self.command = command

    def __str__(self):
        return f"A command failed to run on '{self.system}' while running command '{self.command}': {self.msg}"
