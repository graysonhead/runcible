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

    def __init__(self, device_instance, dstate):
        super().__init__(device_instance, dstate)
        # self.device = device_instance
        self.sub_provider = self.sub_module_provider(self, dstate)

    def check_needs_compatibility(self):
        """
        Ensure that all the needs present are supported by the provider, and raise a warning if not.
        :return:
        """
        supported_attributes = self.get_supported_attributes()
        if self.needed_actions:
            needed_actions = list(self.needed_actions)
        else:
            needed_actions = []
        for need in needed_actions:
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

        # Set the dstate list to a local variable for better readability
        # dstate_list = getattr(self.dstate, self.provides_for.module_name)
        # module_attr_name = self.provides_for.module_name
        # module_key_name = self.provides_for.sort_key
        # for need in needed_actions:
        #     if need.parent_module: #Indicates this is a need for a sub_provider to handle
        #         if not list(filter(lambda x: getattr(x, module_attr_name) == need.module, sub_provider_instances)):
        #             # Get the dstate for the module we are creating an instance for if it exists
        #             dstate_for_instance = list(filter(lambda x: getattr(x, module_key_name) == need.module, dstate_list))
        #             if dstate_for_instance:
        #                 dstate = dstate_for_instance[0].get_state_dict()
        #             else:
        #                 dstate = {}
        #             sub_provider_instances.append(self.sub_module_provider(self.device, dstate))
        for need in needed_actions:
            if need.operation == Op.CREATE:
                self._create_module(need.attribute)
                self.complete(need)
            elif need.operation == Op.REMOVE:
                self._remove_module(need.attribute)
                self.complete(need)
            if self.sub_module_provider:
                self.sub_provider.fix_need(need)
