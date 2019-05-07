from runcible.providers.provider import ProviderBase
from runcible.core.errors import RuncibleNotImplementedError
from runcible.core.need import NeedOperation as Op
from runcible.core.callbacks import CBType
import copy


class ProviderArrayBase(ProviderBase):
    sub_module_provider = None

    """
    This provider base class has pre-canned methods to reduce boilerplate when making Arrays. It's use is optional but
    encouraged.
    """

    def check_needs_compatibility(self):
        """
        Ensure that all the needs present are supported by the provider, and raise a warning if not.
        :return:
        """
        supported_resources = self.get_supported_resources()
        for need in self.needed_actions:
            if need.resource is not 'module':
                if need.sub_resource not in supported_resources:
                    self.device.echo(f"WARNING: need {need.get_formatted_string()} is not supported by module {str(self)}",
                                     cb_type=CBType.WARNING,
                                     indent=True)
                    self.remove_need(need)

    def get_supported_resources(self):
        try:
            return self.sub_module_provider.supported_resources
        except AttributeError:
            raise RuncibleNotImplementedError(msg=f"Provider_array {str(self)} does not provide a sub_module_provider "
                                                f"or a list of supported resource types.")

    def fix_needs(self):
        needed_actions = copy.deepcopy(self.needed_actions)
        for need in needed_actions:
            if need.resource == 'module' and need.operation == Op.CREATE:
                self._create_module(need.value)
                self.complete(need)
            elif need.resource == 'module' and need.operation == Op.REMOVE:
                self._remove_module(need.value)
                self.complete(need)
            if self.sub_module_provider:
                self.sub_module_provider.fix_need(self, need)