from runcible.core.errors import ValidationError
from runcible.core.need import Need

class Module(object):
    module_name = ''
    configuration_attributes = {}
    needed_actions = []

    def __init__(self, config_dictionary):
        """
        This class is the base class for all Modules in Runcible.
        :param config_dictionary:
            The section of the dstate or cstate after the module key in each host definition
        """
        self.validate(config_dictionary)
        for k, v in config_dictionary.items():
            setattr(self, k, v)

    def validate(self, dictionary):
        """
        This validates the configuration, and make sure that there are no typos in key names, or keys called that the
        module doesn't support.
        :param dictionary:
            The dstate dictionary for the module in question.
        :return:
            None

        :raises:
            ValidationError on syntax/type errors
        """
        for k, v in dictionary.items():
            # First ensure that all of the keys supplied in the configuration dictionary exist in
            # self.configuration_attributes
            if k not in self.configuration_attributes.keys():
                raise ValidationError(f"Key {k} not defined in module {self.module_name}")
            # Then ensure the values match the supplied type attribute
            if not isinstance(v, self.configuration_attributes[k]['type']):
                raise ValidationError(f"Value {v} of key {v} in {self.module_name} "
                                      f"must be a {self.configuration_attributes[k]['type']}")

    def __eq__(self, other):
        # This causes comparison operations between two instances of this class to only take into consideration the
        # values of attributes specified in self.configuration_attributes
        return all(getattr(self, key) == getattr(other, key) for key in self.configuration_attributes.keys())

    def needs(self, need):
        if not isinstance(need, Need):
            raise ValidationError("need objects must be an instance of need class")
        self.needed_actions.append(need)

    def get_needs(self):
        need_strings = []
        for need in self.needed_actions:
            need_strings.append(need.get_formatted_string())
        return need_strings
