import argparse
import runcible
import os
from runcible.callbacks.terminalcallbacks import TermCallback


class Cli(object):
    """
    This parses arguments from the command line, and determines what gets run based on user input.
    """

    def __init__(self):
        self.args = None
        self.parseargs()
        self.run()

    def parseargs(self):
        parser = argparse.ArgumentParser(
            description="Runcible is an application to orchestrate network device infrastructure"
        )
        parser.add_argument('target', type=str, default=None, nargs='?')
        parser.add_argument('func', type=str, default=None, nargs='?')
        parser.add_argument('value', type=str, default=None, nargs='?')
        parser.add_argument('--version', action='store_true')
        parser.add_argument(
            '--fabric',
            '-f',
            type=str,
            dest='fabric_file',
            help='YAML Fabric definition',
            default=os.environ.get("RUNCILBE_FABRIC")
        )
        self.args = parser.parse_args()

    def run(self):
        # If --version is present, display the version number and exit
        if self.args.version:
            print(runcible.__version__)
            exit(0)
        # Target, function, and --fabric are required when running from the CLI
        if not all([self.args.target, self.args.func, self.args.fabric_file]):
            TermCallback.fatal("You must specify a target, function, and fabric file when running from CLI")
            exit(1)
