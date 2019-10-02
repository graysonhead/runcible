import argparse
import runcible
import os
import yaml
from runcible.schedulers.naive import NaiveScheduler
from runcible.core.need import Need, NeedOperation
from runcible.core.errors import RuncibleSyntaxError
from mergedb.data_types.database import Database
from runcible.core import logger
import logging


mergedb_default_config = {
    'merge_rules': {
        'keyed_array': [
            {'path': [], 'attribute': 'vlans', 'key': 'id'},
            {'path': [], 'attribute': 'interfaces', 'key': 'name'},
            {'path': [], 'attribute': 'bonds', 'key': 'name'}
        ]
    }
}


class Cli(object):
    """
    This parses arguments from the command line, and determines what gets run based on user input.
    """

    def __init__(self):
        self.args = None
        self.parseargs()
        self.validate_args()
        self.run()

    def parseargs(self):
        parser = argparse.ArgumentParser(
            description="Runcible is an application to orchestrate network device infrastructure"
        )
        parser.add_argument('target', type=str,
                            default=None,
                            nargs='?',
                            help="Target regular expression that selects the devices to be configured")
        parser.add_argument('func',
                            type=str,
                            default=None,
                            nargs='?',
                            help="The need string/function to be performed against targeted devices")
        parser.add_argument('value',
                            type=str,
                            default=None,
                            nargs='?',
                            help="The value provided to the need string, if required")
        parser.add_argument('--version', action='store_true', help="Show version number and exit")
        parser.add_argument('--verbose', '-v', action='store_true', dest='verbose', help="Show debug output")
        datasource_args = parser.add_argument_group("Datasources")
        datasource_args.add_argument(
                                '-m',
                                 '--mergedb-database',
                                 type=str,
                                 default=os.environ.get("MERGEDB_DATABASE", None),
                                 dest='mergedb_database',
                                 help="Path to the base directory of a MergeDB database. "
                                 "Can also be specified via environment variable 'MERGEDB_DATABASE'"
        )
        datasource_args.add_argument(
                                '-y',
                                '--yaml',
                                type=str,
                                dest='yaml',
                                help="Path to a yaml definition file"
        )
        self.args = parser.parse_args()

    def validate_args(self):
        """
        Ensures that the arguments given are sane and don't conflict with each other
        :raises:
            RuncibleSyntaxError
        """
        if not self.args.version:
            if self.args.yaml and self.args.mergedb_database:
                raise RuncibleSyntaxError(msg="Only one datasource can be specified")
            if not self.args.yaml and not self.args.mergedb_database:
                raise RuncibleSyntaxError(msg="You must specify a datasource with -m or -y")

    def run(self):
        # If --version is present, display the version number and exit
        if self.args.version:
            print(runcible.__version__)
            exit(0)
        if self.args.verbose:
            logger.basicConfig(level=logging.DEBUG)
        inp = {}
        if self.args.mergedb_database:
            mdb = Database(self.args.mergedb_database, mergedb_default_config)
            inp = mdb.build()
        elif self.args.yaml:
            with open(self.args.yaml) as file:
                raw = file.read()
            inp = yaml.safe_load(raw)
        if self.args.func == 'apply':
                scheduler = NaiveScheduler(inp, self.args.target)
                scheduler.apply()
        if self.args.func == 'cstate.GET':
            scheduler = NaiveScheduler(inp, self.args.target)
            scheduler.get_cstate()
        elif self.args.func == 'meta.labels.GET':
            scheduler = NaiveScheduler(inp, self.args.target)
            scheduler.get_labels()
        elif self.args.func:
            value = self.args.value
            need = self.get_need_from_func(self.args.func, value=value)
            scheduler = NaiveScheduler(inp, self.args.target)
            scheduler.run_adhoc_command(need)

    def get_need_from_func(self, funcstring, value=None):
        sections = funcstring.split('.')
        if len(sections) == 4:
            parent_module = sections[0]
            module = sections[1]
            attribute = sections[2]
            operation = sections[3]
        elif len(sections) == 3:
            parent_module = None
            module = sections[0]
            attribute = sections[1]
            operation = sections[2]
        else:
            raise RuncibleSyntaxError(msg='Invalid function string')

        try:
            op_object = getattr(NeedOperation, operation)
        except AttributeError:
            raise RuncibleSyntaxError(msg=f"Operation {operation} is not valid. Valid Operations: {list(NeedOperation)}")

        return Need(module, attribute, op_object, value=value, parent_module=parent_module)
