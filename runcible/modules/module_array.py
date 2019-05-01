from runcible.core.errors import NotImplementedError


class ModuleArray(object):
    module_name = ''
    sub_module = None

    def __init__(self, configuration_array: list):
        """
        This class is a contianer for other modules in an array with pass through methods for the
        nested modules.

        :param configuration_array:
        """
        if self.sub_module is None:
            raise NotImplementedError(f"The module {self.__str__()} does not set a sub_module attribute")
        setattr(self, self.module_name, [])
        for list_item in configuration_array:
            getattr(self, self.module_name).append(self.sub_module(list_item))

    def validate(self):
        """
        Runs validate method on each module in the array.
        :return:
        """
        for module in getattr(self, self.module_name):
            module.validate()
