from runcible.core.errors import RuncibleNotImplementedError
import logging
logger = logging.getLogger(__name__)


class TerminalProtocolBase(object):

    def __init__(self, config: dict):
        self.terminal = None
        self.validate(config)
        self.load_config(config)

    def validate(self, config):
        raise RuncibleNotImplementedError(msg=f"Protocol {self.__repr__()} doesn't provide input validation")

    def load_config(self, config):
        for key, value in config.items():
            setattr(self, key, value)

    def connect(self):
        raise RuncibleNotImplementedError(msg=f"Protocol {self.__repr__()} doesn't implement the connect method")

    def exec(self, command):
        self.exec_command(command)

    def exec_implement(self, command):
        raise RuncibleNotImplementedError(msg=f"Protocol {self.__repr__()} doesn't implement the exec_implement method")

    def send_implement(self, command):
        raise RuncibleNotImplementedError(
            msg=f"Protocol {self.__repr__()} doesn't implement the send_implement method")

    def send(self, command):
        logger.debug(f"Provider {self} sent command: {command}")
        response = self.send_implement(command)
        logger.debug(f"Provider {self} recieved response: {response}")
        return response

    def run_command(self, command):
        return self.send(command)

    def receive_implement(self):
        raise RuncibleNotImplementedError(
            msg=f"Protocol {self.__repr__()} doesn't implement the receive_implement method")

    def receive(self):
        return self.receive_implement()