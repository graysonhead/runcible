import unittest
from unittest.mock import MagicMock, Mock
from runcible.providers.cumulus.ntp_client import CumulusNtpClientProvider
from runcible.core.need import Need, NeedOperation as Op
from runcible.core.test_utilities import append_operation_test_cases

system_dict = {}

device = Mock()
prov = CumulusNtpClientProvider(device, {'servers': ['pool.ntp.org']})


class TestNtpClientNeedCompletion(unittest.TestCase):
    longMessage = True

append_operation_test_cases(prov, system_dict, TestNtpClientNeedCompletion)