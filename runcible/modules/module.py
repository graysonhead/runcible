from runcible.core.errors import RuncibleValidationError, RuncibleNotImplementedError
from runcible.core.need import Need, NeedOperation as Op
from runcible.core.utilities import smart_append, compare_lists
from runcible.modules.module_array import ModuleArray


class Module(object):
    module_name = ''
    configuration_attributes = {}
    parent_module = None
    identifier_attribute = None

    def _get_instance_name(self):
        if self.identifier_attribute:
            return getattr(self, self.identifier_attribute, None)

    def __init__(self, config_dictionary: dict, parent_modules=None):
        """
        This class is the base class for all Modules in Runcible.
        :param config_dictionary:
            The section of the dstate or cstate after the module key in each host definition
        """
        if self.parent_module and not self.parent_modules:
            self.parent_modules = [self.parent_module]
        if parent_modules:
            if self.module_name:
                parent_modules.append(self.module_name)
            self.parent_modules = parent_modules
        else:
            self.parent_modules = [self.module_name]
        validated_config = self.validate(config_dictionary)
        for k, v in validated_config.items():
            if issubclass(self.configuration_attributes[k]['type'], ModuleArray) \
                    or issubclass(self.configuration_attributes[k]['type'], Module):
                setattr(self, k, self.configuration_attributes[k]['type'](v, parent_modules=self.parent_modules))
            else:
                setattr(self, k, v)
        self.provider = None

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
            if attribute != self.identifier_attribute:
                if issubclass(options['type'], Module) or issubclass(options['type'], ModuleArray):
                    our_module = getattr(self, attribute, options['type']({}))
                    other_module = getattr(other, attribute, options['type']({}))
                    submod_need_list = our_module.determine_needs(other_module)
                    for need in submod_need_list:
                        needs_list.append(need)
                if options['type'] is bool:
                    smart_append(needs_list, self._determine_needs_bool(attribute, other), Need)
                if options['type'] is str or options['type'] is int:
                    smart_append(needs_list, self._determine_needs_string_or_int(attribute, other), Need)
                if options['type'] is list:
                    needs_list.extend(self._determine_needs_list(attribute, other))
        return needs_list

    def _determine_needs_list(self, attribute, other):
        """
        Compares cstate and dstate to determine a list of needs to be handled

        :param attribute:
            dstate
        :param other:
            cstate
        :return:
            Need Object representing needed action to align states
        """
        needs_list = []
        if getattr(self, attribute, None) is not None:
            self_list = getattr(self, attribute)
            if self_list is False:
                needs_list.append(Need(
                    self._get_instance_name(),
                    attribute,
                    Op.CLEAR,
                    parent_modules=self.parent_modules
                ))
                return needs_list
            other_list = getattr(other, attribute, [])
            missing_items = compare_lists(self_list, other_list)
            for add_item in missing_items['missing_right']:
                needs_list.append(Need(
                    self._get_instance_name(),
                    attribute,
                    Op.ADD,
                    parent_modules=self.parent_modules,
                    value=add_item
                ))
            for del_item in missing_items['missing_left']:
                needs_list.append(Need(
                    self._get_instance_name(),
                    attribute,
                    Op.DELETE,
                    parent_modules=self.parent_modules,
                    value=del_item
                ))
        return needs_list

    def _determine_needs_string_or_int(self, attribute, other):
        """
        Compares cstate and dstate to determine a list of needs to be handled

        This method handles string or int datatypes

        :param attribute:
            dstate
        :param other:
            cstate
        :return:
            Need Object representing needed action to align states
        """
        if getattr(self, attribute, None) is False:
            if getattr(other, attribute, None) is not None:
                return Need(
                    self._get_instance_name(),
                    attribute,
                    Op.DELETE,
                    parent_modules=self.parent_modules
                )
        if getattr(self, attribute, None) is not None and getattr(self, attribute, None) is not False:
            if getattr(self, attribute) != getattr(other, attribute, None):
                return Need(
                    self._get_instance_name(),
                    attribute,
                    Op.SET,
                    parent_modules=self.parent_modules,
                    value=getattr(self, attribute)
                )

    def _determine_needs_bool(self, attribute, other):
        # If self is set to False or None and other is not False, SET to False
        if getattr(self, attribute, None) is not None:
            if getattr(self, attribute, None) is False and \
                    getattr(other, attribute, None) is True:
                return Need(
                    self._get_instance_name(),
                    attribute,
                    Op.SET,
                    parent_modules=self.parent_modules,
                    value=False
                )
            # If self is set to true and other is False or None, SET it to True
            elif getattr(self, attribute, None) is True:
                if getattr(other, attribute, None) is False or \
                        getattr(other, attribute, None) is None:
                    return Need(
                        self._get_instance_name(),
                        attribute,
                        Op.SET,
                        parent_modules=self.parent_modules,
                        value=True
                    )

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
        # Get list of Required Attributes
        required_attributes = []
        for k, v in self.configuration_attributes.items():
            if v.get('required', False):
                if k not in dictionary.keys():
                    raise RuncibleValidationError(f"{self.module_name} is missing required attribute {k}")
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
            # If this attribute is another module, perform tail recursion
            if issubclass(self.configuration_attributes[k]['type'], ModuleArray) \
                    or issubclass(self.configuration_attributes[k]['type'], Module):
                self.configuration_attributes[k]['type'](v)
                if k != self.configuration_attributes[k]['type'].module_name:
                    raise RuncibleValidationError(msg=f"The attribute of a sub module must match it's name, module {self}"
                    f"has sub_module {self.configuration_attributes[k]['type'].module_name} assigned to attribute {k}")

            else:
                # Then ensure the values match the supplied type attribute
                if not isinstance(v, self.configuration_attributes[k]['type']) and v is not False:
                    raise RuncibleValidationError(f"Value {v} of key {k} in {self.module_name} "
                                          f"must be a {self.configuration_attributes[k]['type']}")
                if isinstance(v, list):
                    try:
                        if self.configuration_attributes[k]['sub_type']:
                            for item in v:
                                if not isinstance(item, self.configuration_attributes[k]['sub_type']):
                                    raise RuncibleValidationError(f"Value {item} in {k}: {v} must be a "
                                                                  f"{self.configuration_attributes[k]['sub_type']}")
                    except KeyError:
                        raise RuncibleValidationError(msg=f"{dictionary} could not validate sub_type for attribute {k}, "
                        f"ensure a sub_type is defined")

        return dictionary

    def render(self):
        """
        Render the module as a dict.
        :return:
            A dict representing the module
        """
        rendered_dict = {}
        for key, config_value in self.configuration_attributes.items():
            if issubclass(config_value['type'], Module) or issubclass(config_value['type'], ModuleArray):
                if getattr(self, key, None) is not None:
                    rendered_dict.update({key: getattr(self, key).render()})
            elif getattr(self, key, None) is not None:
                rendered_dict.update({key: getattr(self, key)})
        return rendered_dict

    def __eq__(self, other):
        # This causes comparison operations between two instances of this class to only take into consideration the
        # values of attributes specified in self.configuration_attributes
        return all(getattr(self, key) == getattr(other, key) for key in self.configuration_attributes.keys())

    def __repr__(self):
        return f"<Runcible Module: {self.module_name}>"
