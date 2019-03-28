from enum import Enum


class CBType(Enum):
    INFO = 1
    ERROR = 2
    FATAL = 3
    SUCCESS = 4


class Callback(object):
    """
    A callback is a message to be delivered to the user via some means
    """

    def __init__(self, message, call_type=CBType.INFO):
        self.message = message
        self.type = call_type

    def get_dict(self):
        return {
            "message": self.message,
            "callback_type": self.type.name
        }
