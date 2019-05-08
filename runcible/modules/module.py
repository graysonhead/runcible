from runcible.core.errors import RuncibleValidationError, RuncibleNotImplementedError
from runcible.core.need import Need, NeedOperation as Op


class Module(object):
    module_name = ''
    configuration_attributes = {}
    parent_module = None
    identifier_attribute = None

    def _get_instance_name(self):
        if self.identifier_attribute:
            return getattr(self, self.identifier_attribute, None)

    def __init__(self, config_dictionary: dict):
        """
        This class is the base class for all Modules in Runcible.
        :param config_dictionary:
            The section of the dstate or cstate after the module key in each host definition
        """
        validated_config = self.validate(config_dictionary)
        for k, v in validated_config.items():
            setattr(self, k, v)
        self.provider = None

    # Override the following classes in each subclass

    def determine_needs(self, other):
        """
        Iterate through the attributes of two instances, and determine what actions are needed to make the other match
        self. Override this in your custom module if you need custom logic.

        :param other:
            The other instance to compare this class against.

        :return:
            None, this method adds needed action to self.needs
        """
        #TODO: Clean this up, determine if a need is for a attribute or sub-attribute
        needs_list = []
        for attribute, options in self.configuration_attributes.items():
            # Boolean Logic
            if options['type'] is bool:
                if getattr(self, attribute, None) is not None:
                    if getattr(self, attribute, None) is False and \
                            getattr(other, attribute, None) is True:
                        needs_list.append(Need(
                            self._get_instance_name(),
                            attribute,
                            Op.SET,
                            parent_module=self.parent_module,
                            value=False
                        ))
                    elif getattr(self, attribute, None) is True:
                        if getattr(other, attribute, None) is False or \
                                getattr(other, attribute, None) is None:
                            needs_list.append(Need(
                                self._get_instance_name(),
                                attribute,
                                Op.SET,
                                parent_module=self.parent_module,
                                value=True
                            ))
            if options['type'] is str or options['type'] is int:
                if getattr(self, attribute, None) is not None:
                    if getattr(self, attribute) != getattr(other, attribute, None):
                        needs_list.append(Need(
                            self._get_instance_name(),
                            attribute,
                            Op.SET,
                            parent_module=self.parent_module,
                            value=getattr(self, attribute)
                        ))
        return needs_list
    # Inherited modules below

    def validate(self, dictionary: dict):
        """
        This validates the configuration, and make sure that there are no typos in key names, or keys called that the
        module doesn't support. It will also change strings containing only digits to integers if the
        module schema defines them as an integer.

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
                raise RuncibleValidationError(f"Key {k} not defined in module {self.module_name}")
            # If the string only has numbers and the type is int, we cast it to int
            if self.configuration_attributes[k]['type'] is int and type(v) is str:
                if v.isdigit():
                    v = int(v)
                    dictionary[k] = v
            # Then ensure the values match the supplied type attribute
            if not isinstance(v, self.configuration_attributes[k]['type']) and v is not False:
                raise RuncibleValidationError(f"Value {v} of key {k} in {self.module_name} "
                                      f"must be a {self.configuration_attributes[k]['type']}")
        # Set default values for bool attributes
        # for k, v in self.configuration_attributes.items():
        #     if 'default' in v:
        #         if k not in dictionary:
        #             dictionary.update({k: v['default']})
        return dictionary

    def __eq__(self, other):
        # This causes comparison operations between two instances of this class to only take into consideration the
        # values of attributes specified in self.configuration_attributes
        return all(getattr(self, key) == getattr(other, key) for key in self.configuration_attributes.keys())

    def __repr__(self):
        return f"<Runcible Module: {self.module_name}>"
