import unittest
from unittest.mock import Mock
from runcible.providers.cumulus.interfaces import CumulusInterfacesProvider
from runcible.modules.interface import InterfaceResources
from runcible.core.need import Need, NeedOperation

device = Mock()
prov = CumulusInterfacesProvider(device, {})


class TestInterfaceNeedsCompletion(unittest.TestCase):
    def test_set_interface_name(self):
        prov.needed_actions.append(Need('swp1',
                                        InterfaceResources.PVID,
                                        operation=NeedOperation.SET,
                                        parent_module='interfaces',
                                        value=10
                                        ))
        prov.fix_needs()
        self.assertEqual([], prov.needed_actions)