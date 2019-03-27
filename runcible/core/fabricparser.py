import yaml

class FabricParser(object):
    """
    Thiss parses the fabric yaml file or files and splits it up into individual items,
    these items are then passed to the ObjectParser
    """

    def __init__(self):

    def load_from_yaml_file(self, yaml_fabric_path):
        raw = self.read_file(yaml_fabric_path)
        #TODO: Add logic here to allow from multi-file imports
        dict = yaml.load(raw)

    @staticmethod
    def read_file(path):
        with open(path, 'r') as file:
            return file.read()

