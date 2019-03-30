from paramiko import SSHClient, RejectPolicy
from runcible.core.errors import ClientExecutionError


class SSHClient(object):

    def __init__(self, hostname=None, username=None, password=None, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = None

    def connect(self):
        """Adds a paramiko ssh client to self.client"""
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(RejectPolicy)
        self.ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

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
        stdin, stdout, stderr = self.ssh.exec_command(command)
        err = '\n'.join(stderr.readlines())
        if err:
            raise ClientExecutionError(msg=stdout.read(), command=command, system=self.hostname)
