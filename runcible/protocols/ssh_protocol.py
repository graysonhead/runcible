from paramiko import SSHClient, RejectPolicy
from runcible.core.errors import RuncibleClientExecutionError, \
    RuncibleConnectionError, \
    RuncibleNotConnectedError, \
    RuncibleValidationError
from runcible.protocols.protocol import TerminalProtocolBase


class SSHProtocol(TerminalProtocolBase):

    def __init__(self, config: dict):
        super().__init__(config=config)
        self.client = None

    def validate(self, config):
        for key in ['hostname', 'username']:
            if key not in config:
                raise RuncibleValidationError(msg=f"Key {key} missing from Protocol {self.__repr__()}")

    def connect(self):
        """Adds a paramiko ssh client to self.client"""
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(RejectPolicy)
        self.client.connect(hostname=getattr(self, 'hostname'),
                            port=getattr(self, 'port', 22),
                            username=getattr(self, 'username'),
                            password=getattr(self, 'password', None))

    def run_command(self, command):
        """
        Runs a command via self.ssh object

        :param command:
            The command to be run

        :return:
            stdout from the command

        :raises:
             ClientExecutionError
        """
        if self.client is None:
            raise RuncibleNotConnectedError("You must activate the client with self.connect() before executing commands")
        stdin, stdout, stderr = self.client.exec_command(command)
        err = '\n'.join(stderr.readlines())
        if err:
            raise RuncibleClientExecutionError(msg=err, command=command, system=self.hostname)
        return stdout.read().decode('utf-8')