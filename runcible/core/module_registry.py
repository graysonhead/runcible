import inspect
from runcible import modules
from runcible.modules.module import Module


class ModuleRegistry:
    modules = {}

    @classmethod
    def load_modules(cls):
        cls.load_core_modules()

    @classmethod
    def load_core_modules(cls):
        """
        Loads all the modules in runcible.modules
        :return:
        """
        # Collect all the modules in runcible.modules that aren't the base class
        core_modules = [getattr(modules, a) for a in dir(modules) if not a.startswith('__') and not a == 'module']
        for mod in core_modules:
            # Get a list of all attributes that aren't built-in
            module_class_candidates = [a for a in dir(mod) if not a.startswith('__')]
            for cl in module_class_candidates:
                # Ignore the base class
                if cl != 'Module':
                    # If anything we found in the previous step is a subclass of Module, add it to the registry
                    attr = getattr(mod, cl)
                    # Make sure we are looking at a class
                    if inspect.isclass(attr):
                        # Ensure its a subclass of Module
                        if issubclass(attr, Module):
                            # Add it to the registry
                            cls.add_module_to_registry(attr)

    @classmethod
    def add_module_to_registry(cls, module):
        """
        Adds a module to the registry using module.module_name as a key
        :param module:
        :return:
        """
        cls.modules.update({module.module_name: module})

    @classmethod
    def get_module(cls, module_name):
        if not cls.modules:
            cls.load_modules()
        return cls.modules[module_name]