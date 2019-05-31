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
        supported_attributes = self.get_supported_attributes()
        for need in self.needed_actions:
            if need.operation != Op.CREATE and need.operation != Op.REMOVE:
                if need.attribute not in supported_attributes:
                    self.device.echo(f"WARNING: need "
                                     f"{need.get_formatted_string()} is not supported by provider {str(self)}",
                                     cb_type=CBType.WARNING,
                                     indent=True)
                    self.remove_need(need)

    def get_supported_attributes(self):
        try:
            return self.sub_module_provider.supported_attributes
        except AttributeError:
            raise RuncibleNotImplementedError(msg=f"Provider_array {str(self)} does not provide a sub_module_provider "
                                                f"or a list of supported attributes.")

    def adhoc_need(self, need):
        if need.operation == Op.GET:
            item = list(filter(lambda x: x.name == need.module, getattr(self.cstate, self.provides_for.module_name)))[0]
            return getattr(item, need.attribute)
        else:
            self.needed_actions.append(need)
            self.check_needs_compatibility()
            self.fix_needs()

    def fix_needs(self):
        needed_actions = copy.deepcopy(self.needed_actions)
        for need in needed_actions:
            if need.operation == Op.CREATE:
                self._create_module(need.attribute)
                self.complete(need)
            elif need.operation == Op.REMOVE:
                self._remove_module(need.attribute)
                self.complete(need)
            if self.sub_module_provider:
                self.sub_module_provider.fix_need(self, need)