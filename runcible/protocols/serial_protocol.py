from runcible.protocols.protocol import TerminalProtocolBase
from runcible.core.errors import RuncibleClientExecutionError, \
    RuncibleConnectionError, \
    RuncibleNotConnectedError, \
    RuncibleValidationError
from serial import Serial


class SerialProtocol(TerminalProtocolBase):

    def __init__(self, config: dict):
        super().__init__(config=config)
        self.client = None

    def validate(self, config):
        for key in ['device', 'speed', 'username', 'password']:
            if key not in config:
                raise RuncibleValidationError(msg=f"Key {key} missing from protocol {self.__repr__()}")

    def connect(self):
        self.client = Serial(self.device, self.speed, timeout=1)
        self.client.write(b'\r\n')
        lines = self.client.readlines()
        if 'password' in lines[-1].decode():
            self.send_implement('exit')
            self.connect()
        elif 'login' in lines[-1].decode().lower():
            response = self.send_implement(self.username)
            if 'password' in response[-1].decode().lower():
                response = self.send_implement(self.password)
                if 'incorrect' in response[-1].decode().lower():
                    raise RuncibleConnectionError(msg=f"Login error occured in {self.__repr__()}: {response}")
        if '#' in lines[-1].decode():
            self.send_implement('exit')

    def disconnect(self):
        self.client.close()

    def send_implement(self, command):
        if self.client is None:
            raise RuncibleNotConnectedError("Activate with self.connect() before executing")
        self.client.write(f"{command}\r\n".encode('utf-8'))
        lines = self.client.readlines()
        decoded_lines = []
        for line in lines:
            decoded_lines.append(line.decode())
        return lines
