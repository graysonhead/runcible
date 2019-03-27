from runcible.callbacks.callback import Callback, CBType
from runcible.callbacks.terminalcallbacks import TermCallback
from enum import Enum


class CBMethod(Enum):
    """
    Determines what kind of output we expect from the callback.
    """
    JSON = 1  # Return JSON
    TERMINAL = 2  # Print text to stdout/stderr

class Callbacks(object):
    """
    An instance of this class is attached to executor objects in Runicble. It stores instances of callbacks
    in itself, so they can be returned at a later time.
    """

    def __init__(self):
        self.callbacks = []
        self.is_failed = False
        self.callback_method = CBMethod.TERMINAL

    def add_callback(self, callback_object):
        # TODO: This should accept a list as well
        if not isinstance(callback_object, Callback):
            raise TypeError("Only a Callback instance can be added to a Callbacks collection")
        self.callbacks.append(callback_object)
        # If we add any fatal callbacks to the collection, consider the collection failed
        if callback_object.type == CBType.FATAL:
            self.is_failed = True

    def run_callbacks(self):
        for callback in self.callbacks:
            if callback.type == CBType.INFO:
                TermCallback.info(callback.message)
            elif callback.type == CBType.SUCCESS:
                TermCallback.success(callback.message)
            elif callback.type == CBType.ERROR:
                TermCallback.error(callback.message)
            elif callback.type == CBType.FATAL:
                TermCallback.fatal(callback.message)
