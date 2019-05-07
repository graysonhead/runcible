from enum import Enum


class CBType(Enum):
    INFO = 1
    ERROR = 2
    FATAL = 3
    SUCCESS = 4
    CHANGED = 5
    WARNING = 6


class Callback(object):
    """
    A callback is a message to be delivered to the user via some means
    """

    def __init__(self, message, call_type=CBType.INFO, indent=False, decoration=False):
        self.message = message
        self.type = call_type
        self.indent = indent
        self.decoration = decoration

    def get_dict(self):
        return {
            "message": self.message,
            "callback_type": self.type.name,
        }
