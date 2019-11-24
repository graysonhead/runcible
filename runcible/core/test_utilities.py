from runcible.core.need import Need, NeedOperation as Op
from runcible.providers.provider_array import ProviderArrayBase


def make_test_function(provider, module, attribute, operation, value=None, parent_module=None):
    def test(self):
        if parent_module:
            provider.needed_actions.append(
                Need(module, attribute, operation=operation, value=value, parent_module=parent_module.module_name))
        else:
            provider.needed_actions.append(Need(module.module_name, attribute, operation=operation, value=value))
        provider.fix_needs()
        self.assertEqual([], provider.needed_actions)
    return test


def append_operation_test_cases(provider, system_dict, test_class):
    if isinstance(provider, ProviderArrayBase):
        for sup_attribute in provider.sub_provider.supported_attributes:
            module = provider.provides_for
            sub_module = provider.sub_provider.provides_for
            sub_mod_name = sub_module.configuration_attributes[sub_module.identifier_attribute]['examples'][0]
            config_dict = sub_module.configuration_attributes[sup_attribute]
            system_dict.update({sup_attribute: config_dict['examples'][0]})
            for op in config_dict['allowed_operations']:
                if op == Op.SET:
                    test_func = make_test_function(
                        provider,
                        sub_mod_name,
                        sup_attribute,
                        Op.SET,
                        value=config_dict['examples'][0],
                        parent_module=module
                    )
                    setattr(test_class, f"test_{module.module_name}_{sup_attribute}_{op.name}", test_func)
                elif op == Op.CLEAR:
                    test_func = make_test_function(
                        provider,
                        sub_mod_name,
                        sup_attribute,
                        Op.CLEAR,
                        parent_module=module
                    )
                    setattr(test_class, f"test_{module.module_name}_{sup_attribute}_{op.name}", test_func)
                elif op == Op.ADD:
                    test_func = make_test_function(
                        provider,
                        sub_mod_name,
                        sup_attribute,
                        Op.ADD,
                        value=config_dict['examples'][0],
                        parent_module=module
                    )
                    setattr(test_class, f"test_{module.module_name}_{sup_attribute}_{op.name}", test_func)
                elif op == Op.DELETE:
                    test_func = make_test_function(
                        provider,
                        sub_mod_name,
                        sup_attribute,
                        Op.DELETE,
                        value=config_dict['examples'][0],
                        parent_module=module
                    )
                    setattr(test_class, f"test_{module.module_name}_{sup_attribute}_{op.name}", test_func)
                elif op == Op.CREATE:
                    test_func = make_test_function(
                        provider,
                        sub_mod_name,
                        sup_attribute,
                        Op.CREATE,
                        value=config_dict['examples'][0],
                        parent_module=module
                    )
                    setattr(test_class, f"test_{module.module_name}_{sup_attribute}_{op.name}", test_func)
                elif op == Op.REMOVE:
                    test_func = make_test_function(
                        provider,
                        sub_mod_name,
                        sup_attribute,
                        Op.REMOVE,
                        value=config_dict['examples'][0],
                        parent_module=module
                    )
                    setattr(test_class, f"test_{module.module_name}_{sup_attribute}_{op.name}", test_func)

    else:
        for sup_attribute in provider.supported_attributes:
            module = provider.provides_for
            config_dict = module.configuration_attributes[sup_attribute]
            system_dict.update({sup_attribute: config_dict['examples'][0]})
            for op in config_dict['allowed_operations']:
                if op == Op.SET:
                    test_func = make_test_function(provider, module, sup_attribute, Op.SET, value=config_dict['examples'][0])
                    setattr(test_class, f"test_{module.module_name}_{sup_attribute}_{op.name}", test_func)
                elif op == Op.CLEAR:
                    test_func = make_test_function(provider, module, sup_attribute, Op.CLEAR)
                    setattr(test_class, f"test_{module.module_name}_{sup_attribute}_{op.name}", test_func)
                elif op == Op.ADD:
                    test_func = make_test_function(provider, module, sup_attribute, Op.ADD,
                                                   value=config_dict['examples'][0])
                    setattr(test_class, f"test_{module.module_name}_{sup_attribute}_{op.name}", test_func)
                elif op == Op.DELETE:
                    test_func = make_test_function(provider, module, sup_attribute, Op.DELETE,
                                                   value=config_dict['examples'][0])
                    setattr(test_class, f"test_{module.module_name}_{sup_attribute}_{op.name}", test_func)
                elif op == Op.CREATE:
                    test_func = make_test_function(provider, module, sup_attribute, Op.CREATE,
                                                   value=config_dict['examples'][0])
                    setattr(test_class, f"test_{module.module_name}_{sup_attribute}_{op.name}", test_func)
                elif op == Op.REMOVE:
                    test_func = make_test_function(provider, module, sup_attribute, Op.REMOVE,
                                                   value=config_dict['examples'][0])
                    setattr(test_class, f"test_{module.module_name}_{sup_attribute}_{op.name}", test_func)

