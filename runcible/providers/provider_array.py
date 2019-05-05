from runcible.providers.provider import ProviderBase
from runcible.core.need import NeedOperation as Op
import copy


class ProviderArrayBase(ProviderBase):
    sub_module_provider = None

    """
    This provider base class has pre-canned methods to reduce boilerplate when making Arrays. It's use is optional but
    encouraged.
    """

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