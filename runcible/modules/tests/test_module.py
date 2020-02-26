from unittest import TestCase
from runcible.modules.module import Module
from runcible.core.need import NeedOperation as Op
from runcible.core.errors import RuncibleValidationError


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
        }
    }


class TestModuleValidation(TestCase):

    def test_required_check(self):
        with self.assertRaises(RuncibleValidationError):
            TestModule({'test_attribute2': 1})

    def test_type_check(self):
        with self.assertRaises(RuncibleValidationError):
            TestModule({'test_attribute1': 1})