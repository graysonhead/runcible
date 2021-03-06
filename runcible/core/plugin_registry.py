import inspect
# from runcible import modules, drivers, labels
import runcible
from runcible.modules.module import Module
from runcible.drivers.driver import DriverBase
from runcible.labels.label import LabelBase
# from runcible.schedulers.scheduler import SchedulerBase
import pkg_resources

class PluginRegistry:
    modules = {}
    drivers = {}
    labels = {}
    schedulers = {}

    @classmethod
    def load_drivers(cls):
        cls.load_core_labels()
        cls.load_core_drivers()
        cls.load_plugin_drivers()

    @classmethod
    def load_schedulers(cls):
        cls.load_core_schedulers()

    @classmethod
    def load_core_drivers(cls):
        driver_list = cls.class_loader(
            runcible.drivers,
            DriverBase,
            'driver'
        )
        for drv in driver_list:
            cls.add_driver_to_registry(drv)

    @classmethod
    def load_plugin_drivers(cls):
        plugins = {
            entry_point.name: entry_point.load()
            for entry_point
            in pkg_resources.iter_entry_points('runcible.drivers')
        }
        for name, driver_class in plugins.items():
            cls.add_driver_to_registry(driver_class)

    @classmethod
    def load_modules(cls):
        cls.load_core_modules()

    @classmethod
    def load_core_modules(cls):
        mods = cls.class_loader(
            runcible.modules,
            Module,
            'module'
        )
        for mod in mods:
            cls.add_module_to_registry(mod)

    @classmethod
    def class_loader(cls, search_base, parent, base_package):
        found_classes = []
        # Collect all the modules in runcible.modules that aren't the base class
        core_modules = [getattr(search_base, a) for a in dir(search_base) if not a.startswith('__') and not a == base_package]
        for mod in core_modules:
            # Get a list of all attributes that aren't built-in
            module_class_candidates = [a for a in dir(mod) if not a.startswith('__')]
            for cl in module_class_candidates:
                # If anything we found in the previous step is a subclass of Module, add it to the registry
                attr = getattr(mod, cl)
                # Make sure we are looking at a class
                if inspect.isclass(attr):
                    # Ensure its a subclass of Module and ignore the base class
                    if issubclass(attr, parent) and attr is not parent:
                        # Add it to the list
                        found_classes.append(attr)
        return found_classes

    @classmethod
    def load_core_labels(cls):
        label_list = cls.class_loader(
            runcible.labels,
            LabelBase,
            'label'
        )
        for lab in label_list:
            cls.add_label_to_registry(lab)

    @classmethod
    def load_core_schedulers(cls):
        scheduler_list = cls.class_loader(
            runcible.schedulers,
            runcible.schedulers.scheduler.SchedulerBase,
            'scheduler'
        )
        for sched in scheduler_list:
            cls.add_scheduler_to_registry(sched)

    @classmethod
    def add_scheduler_to_registry(cls, scheduler):
        """
        Adds a scheduler to the registry using scheduler.scheduler_name as a key
        :param scheduler:
        :return:
        """
        cls.schedulers.update({scheduler.scheduler_name: scheduler})

    @classmethod
    def add_label_to_registry(cls, label):
        """
        Adds a label to the registry using label.type_label as a key
        :param label:
        :return:
        """
        cls.labels.update({label.type_label: label})

    @classmethod
    def add_module_to_registry(cls, module):
        """
        Adds a module to the registry using module.module_name as a key
        :param module:
        :return:
        """
        cls.modules.update({module.module_name: module})

    @classmethod
    def add_driver_to_registry(cls, driver):
        """
        Adds a driver to the registry using driver.driver_name as a key
        :param driver:
        :return:
        """
        cls.drivers.update({driver.driver_name: driver})

    @classmethod
    def get_module(cls, module_name):
        if not cls.modules:
            cls.load_modules()
        return cls.modules[module_name]

    @classmethod
    def get_driver(cls, driver_name):
        if not cls.drivers:
            cls.load_drivers()
        return cls.drivers[driver_name]

    @classmethod
    def get_label(cls, label_name):
        if not cls.labels:
            cls.load_core_labels()
        return cls.labels[label_name]

    @classmethod
    def get_scheduler(cls, scheduler_name):
        if not cls.schedulers:
            cls.load_core_schedulers()
        return cls.schedulers[scheduler_name]