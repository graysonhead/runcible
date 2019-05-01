from paramiko import SSHClient, RejectPolicy
from runcible.core.errors import RuncibleClientExecutionError, RuncibleConnectionError, RuncibleNotConnectedError


class SSHProtocol(object):

    def __init__(self, hostname=None, username=None, password=None, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = None

    def connect(self):
        """Adds a paramiko ssh client to self.client"""
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(RejectPolicy)
        self.client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

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
            raise RuncibleClientExecutionError(msg=stdout.read(), command=command, system=self.hostname)
        return stdout.read().decode('utf-8')