import inspect
from runcible import modules


class ModuleRegistry:
    modules = {}

    @classmethod
    def load_modules(cls):
        for name, obj in inspect.getmembers(modules):
            if inspect.isclass(obj) and obj.module_name:
                cls.modules.update({obj.module_name: obj})

