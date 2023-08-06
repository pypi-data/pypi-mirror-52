"""Tests for defcon.plugins.base."""
import uuid
from django import test

from defcon.plugins import base


class PluginsTests(test.TestCase):
    """Test the plugins."""

    def test_plugin(self):
        """Test that we can build plugins."""
        class _FakePlugin(base.Plugin):
            """Fake class for testing."""

            def __init__(self, settings):
                """Fake __init__."""
                super(_FakePlugin, self).__init__(settings)

            @property
            def short_name(self):
                return 'fake'

            @property
            def name(self):
                return 'fake'

            def statuses(self):
                """Fake statuses."""
                return []

        # Can we instantiate it ?
        p = _FakePlugin({})
        p.statuses()


class StatusTests(test.TestCase):
    """Test that we can build statuses."""

    def test_basic(self):
        """Test that we can create statuses."""
        s = base.Status('Test status', 5, 'http://github.com/iksaif/defcon',
                        description='This is a test')
        expected = {
            'defcon': 5, 'title': 'Test status',
            'description': 'This is a test',
            'link': 'http://github.com/iksaif/defcon',
            'id': uuid.UUID('971adc54-d615-59b7-a797-2b8167153174'),
            'time_start': None,
            'time_end': None,
        }

        self.assertEqual(dict(s), expected)
