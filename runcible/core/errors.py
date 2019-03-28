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
