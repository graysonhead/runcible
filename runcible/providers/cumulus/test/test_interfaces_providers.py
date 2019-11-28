import unittest
from unittest.mock import Mock
from runcible.providers.cumulus.interfaces import CumulusInterfacesProvider
from runcible.core.test_utilities import append_operation_test_cases

system_dict = {}
device = Mock()
prov = CumulusInterfacesProvider(device, {})


class TestInterfaceNeedCompletion(unittest.TestCase):
    longMessage=True

append_operation_test_cases(prov, system_dict, TestInterfaceNeedCompletion)