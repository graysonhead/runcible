import argparse
import runcible
import os
from runcible.core.terminalcallbacks import TermCallback
from runcible.schedulers.naive import NaiveScheduler
from mergedb.data_types.database import Database

mergedb_default_config = {
    'merge_rules': {
        'keyed_array': [
            {'path': [], 'attribute': 'vlans', 'key': 'id'},
            {'path': [], 'attribute': 'interfaces', 'key': 'name'}
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
        self.run()

    def parseargs(self):
        parser = argparse.ArgumentParser(
            description="Runcible is an application to orchestrate network device infrastructure"
        )
        parser.add_argument('target', type=str, default=None, nargs='?')
        parser.add_argument('func', type=str, default=None, nargs='?')
        parser.add_argument('value', type=str, default=None, nargs='?')
        parser.add_argument('--version', action='store_true')
        # parser.add_argument(
        #     '--fabric',
        #     '-f',
        #     type=str,
        #     dest='fabric_file',
        #     help='YAML Fabric definition',
        #     default=os.environ.get("RUNCILBE_FABRIC")
        # )
        parser.add_argument('-m',
                            '--mergedb-database',
                            type=str,
                            default=os.environ.get("MERGEDB_DATABASE", None),
                            dest='mergedb_database'
                            )
        self.args = parser.parse_args()

    def run(self):
        # If --version is present, display the version number and exit
        if self.args.version:
            print(runcible.__version__)
            exit(0)
        if self.args.mergedb_database:
            mdb = Database(self.args.mergedb_database, mergedb_default_config)
            inp = mdb.build()
            scheduler = NaiveScheduler(inp)
            scheduler.plan()

