import unittest
import mock
from unittest.mock import MagicMock, Mock
from runcible.providers.cumulus.system import CumulusSystemProvider
from runcible.modules.system import System
from runcible.core.test_utilities import append_operation_test_cases
system_dict = {
    "hostname": "test"
}




device = Mock()
prov = CumulusSystemProvider(device, {})


class TestNeedCompletion(unittest.TestCase):
    longMessage = True


append_operation_test_cases(prov, system_dict, TestNeedCompletion)
