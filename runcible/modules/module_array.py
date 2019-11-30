from runcible.core.errors import RuncibleNotImplementedError
from runcible.core.need import Need, NeedOperation as Op


class ModuleArray(object):
    module_name = ''
    sort_key = ''
    sub_module = None

    def __init__(self, configuration_array: list, parent_modules=None):
        """
        This class is a contianer for other modules in an array with pass through methods for the
        nested modules.

        :param configuration_array:
        """
        if parent_modules:
            parent_modules.append(self.module_name)
            self.parent_modules = parent_modules
        else:
            self.parent_modules = [self.module_name]
        if self.sub_module is None:
            raise RuncibleNotImplementedError(f"The module {self.__str__()} does not set a sub_module attribute")
        setattr(self, self.module_name, [])
        for list_item in configuration_array:
            parent_mod_list = self.parent_modules
            parent_mod_list.append(list_item.get(self.sort_key))
            getattr(self, self.module_name).append(self.sub_module(list_item, parent_modules=self.parent_modules))

    def determine_needs(self, other):
        """
        This method compares an instance of a module array to another one and then runs the determine needs method of
        each matching module pair, or runs it against an empty instance of the module otherwise. This should ensure
        that all of the modules in the array get compared and a full needs list is generated. The "id attribute" method
        of each class is how the instances are associated with each other.

        Note that this module only cares about desired instances (self). If anything is present in other that isn't
        present in self, it will be ignored by default.
        :param other:
        :return:
        """
        if not self.sort_key:
            raise RuncibleNotImplementedError(msg=f"{self.module_name} module has not provided a sort key attribute.")
        needs_list = []
        # First sort each list so they can be directly compared, this saves some time when running repeatedly against
        # the same environment
        sorted_self = sorted(getattr(self, self.module_name), key=lambda x: getattr(x, self.sort_key))
        sorted_other = sorted(getattr(other, other.module_name), key=lambda x: getattr(x, other.sort_key))
        for item in sorted_self:
            # this selects the item from the other list to compare the item we are iterating on to
            try:
                other_item = list(filter(
                    lambda x: getattr(x, self.sort_key) == getattr(item, self.sort_key), sorted_other))[0]
            except IndexError:
                # If the item can't be matched to something in the list, compare the dstate to an empty state
                # so all of the needs can be generated on the first execution
                other_item = self.sub_module({})
                needs_list.append(Need(
                    self.module_name,
                    getattr(item, self.sort_key),
                    Op.CREATE,
                    parent_modules=self.parent_modules
                ))
            needs_list.extend(item.determine_needs(other_item))
        return needs_list

    def render(self):
        """
        Render the module and all sub_modules as a list.
        :return:
            A list representing the module and it's children
        """
        rendered_list = []
        for module in getattr(self, self.module_name):
            rendered_list.append(module.render())
        return rendered_list

    def validate(self):
        """
        Runs validate method on each module in the array.
        :return:
        """
        for module in getattr(self, self.module_name):
            module.validate()
