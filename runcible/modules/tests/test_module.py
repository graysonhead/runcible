from unittest import TestCase
from runcible.modules.module import Module
from runcible.modules.module_array import ModuleArray
from runcible.core.need import NeedOperation as Op
from runcible.core.errors import RuncibleValidationError


class TestSubModule(Module):
    module_name = "sub_module"
    configuration_attributes = {
        'subattr': {
            'type': str,
            'allowed_operations': [Op.SET],
            'examples': ['hi']
        }
    }


class TestSubMod(Module):
    module_name = 'test_sub_mod'
    configuration_attributes = {
        'name': {
            'type': str,
            'allowed_operations': [Op.CREATE, Op.REMOVE],
            'examples': ['mod1', 'mod2'],
        },
        'test_value': {
            'type': int,
            'allowed_operations': [Op.SET],
            'examples': [1, 2, 3]
        }
    }


class TestSubModuleArray(ModuleArray):
    module_name = "sub_mod_array"
    sub_module = TestSubMod


class TestModule(Module):
    module_name = "test_module"
    configuration_attributes = {
        'test_attribute1': {
            'type': str,
            'allowed_operations': [Op.SET],
            'examples': ['a', 'b', 'c'],
            'description': "Test attribue 1",
            'required': True
        },
        'test_attribute2': {
            'type': int,
            'allowed_operations': [Op.SET],
            'examples': [1, 2, 3],
            'description': "Test attribue 2"
        },
        'sub_module': {
            'type': TestSubModule
        },
        'sub_mod_array': {
            'type': TestSubModuleArray
        }
    }


class TestModuleValidation(TestCase):

    def test_required_check(self):
        with self.assertRaises(RuncibleValidationError):
            TestModule({'test_attribute2': 1})

    def test_type_check(self):
        with self.assertRaises(RuncibleValidationError):
            TestModule({'test_attribute1': 1})

    def test_submodule(self):
        TestModule({'test_attribute1': 'string', 'sub_module': {'subattr': 'hello'}})

    def test_submodule_array(self):
        TestModule({'test_attribute1': 'string', 'sub_mod_array': [{'name': 'sub1', 'test_value': 5}]})


class TestModuleRendering(TestCase):

    def test_basic_render(self):
        mod = TestModule({'test_attribute1': 'test'})
        rendered = mod.render()
        self.assertEqual({'test_attribute1': 'test'}, rendered)

    def test_submodule_render(self):
        mod = TestModule({'test_attribute1': 'test', 'sub_module': {'subattr': 'hello'}})
        rendered = mod.render()
        self.assertEqual({'test_attribute1': 'test', 'sub_module': {'subattr': 'hello'}}, rendered)

    def test_submodule_array_render(self):
        mod = TestModule({'test_attribute1': 'string', 'sub_mod_array': [{'name': 'sub1', 'test_value': 5}]})
        rendered = mod.render()
        self.assertEqual({'test_attribute1': 'string', 'sub_mod_array': [{'name': 'sub1', 'test_value': 5}]}, rendered)