from unittest import TestCase
from runcible.core.need import Need, NeedOperation as Op


class TestNeedRendering(TestCase):

    def test_basic_render(self):
        n = Need('em1', 'ipv4_address', Op.SET, value="value")
        rendered = n.get_formatted_string()
        self.assertEqual('em1.ipv4_address.SET: value', rendered)

    def test_render_onechild(self):
        n = Need('module', 'attribute', Op.DELETE, value="value", parent_modules=['parent1'])
        rendered = n.get_formatted_string()
        self.assertEqual('parent1.module.attribute.DELETE: value', rendered)

    def test_render_twochildren(self):
        n = Need('module', 'attribute', Op.DELETE, value="value", parent_modules=['parent1', 'parent2'])
        rendered = n.get_formatted_string()
        self.assertEqual('parent1.parent2.module.attribute.DELETE: value', rendered)