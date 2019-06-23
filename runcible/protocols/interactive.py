import paramiko
from paramiko_expect import SSHClientInteraction
from time import sleep
import re


class InteractiveSSH(object):
    def __init__(self, hostname, username=None, password=None, timeout=5):
        self.shell = None
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.prompt = f'^{username}@vyos.*'

    def connect(self):
        self.client.connect(hostname=self.hostname, username=self.username, password = self.password, timeout=self.timeout)
        self.shell = self.client.invoke_shell()
        self.shell.settimeout(self.timeout)
        sleep(.5)
        return self.read_lines(65535)

    def send(self, body):
        return self.shell.send(body + '\n')

    def read(self, num_bytes=65535):
        return self.shell.recv(num_bytes).decode()

    def read_expect(self, pattern):
        string = self.read_until_pattern(self.prompt)
        if re.match(pattern, string):
            return string
        else:
            return f"Did not match {string}"

    def read_expect_lines(self, pattern_list):
        if pattern_list[-1] != self.prompt:
            pattern_list.append(self.prompt)
        output_lines = self.read_until_pattern_lines(self.prompt)
        results = []
        for line in pattern_list:
            results.append(re.match(line, output_lines[pattern_list.index(line)]))
        if all(results):
            return output_lines
        else:
            return f"nope {output_lines}"


    def read_until_pattern(self, pattern):
        complete = False
        while True:
            if complete:
                break
            string = ''
            string = string + self.read()
            string_lines = string.splitlines()
            for line in string_lines:
                if re.match(pattern, line):
                    complete = True
            sleep(.1)
        return string

    def read_until_pattern_lines(self, pattern):
        return self.read_until_pattern(pattern).splitlines()

    def read_lines(self, num_bytes=65535):
        raw_output = self.read()
        return raw_output.splitlines()
