# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
from django.core.exceptions import ImproperlyConfigured

from django.test import TestCase
from mock import patch, MagicMock
from django_appregistration import MultiTypePartRegistry, SingleTypePartRegistry

try:
    from django.test import override_settings
except ImportError:
    from django.test.utils import override_settings

__author__ = 'Tim Schneider <tim.schneider@northbridge-development.de>'
__copyright__ = "Copyright 2016, Northbridge Development Konrad & Schneider GbR"
__credits__ = ["Tim Schneider", ]
__maintainer__ = "Tim Schneider"
__email__ = "mail@northbridge-development.de"
__status__ = "Development"

logger = logging.getLogger(__name__)


class MultiTypePartRegistryTestCase(TestCase):
    def tearDown(self):
        MultiTypePartRegistry.reset()
        MultiTypePartRegistry.part_class = None
        MultiTypePartRegistry.ignore_django_namespace = True
        MultiTypePartRegistry.call_function_subpath = None

    def test_reset(self):
        MultiTypePartRegistry.loaded = True
        MultiTypePartRegistry.types = {'type': []}

        MultiTypePartRegistry.reset()

        self.assertFalse(MultiTypePartRegistry.loaded)
        self.assertDictEqual(MultiTypePartRegistry.types, {})

    @patch('django_appregistration.settings.INSTALLED_APPS', ['django.test.app', 'app1', 'app2.django.test'])
    def test__checked_apps(self):
        MultiTypePartRegistry.ignore_django_namespace = False
        self.assertListEqual(
            MultiTypePartRegistry._checked_apps(),
            ['django.test.app', 'app1', 'app2.django.test'],
        )

        MultiTypePartRegistry.ignore_django_namespace = True
        self.assertListEqual(
            MultiTypePartRegistry._checked_apps(),
            ['app1', 'app2.django.test'],
        )

    def test_add_item(self):
        class Test(object):
            pass
        MultiTypePartRegistry.part_class = Test

        self.assertRaises(ValueError, MultiTypePartRegistry.add_item, '', object())

        test = Test()
        MultiTypePartRegistry.add_item('Test', test)
        MultiTypePartRegistry.add_item('Test', test)
        MultiTypePartRegistry.add_item('Test2', test)

        self.assertDictEqual(
            MultiTypePartRegistry.types,
            {
                'Test': [test, test],
                'Test2': [test],
            }
        )

    def test_load(self):
        lock_mock = MagicMock()
        MultiTypePartRegistry.lock = lock_mock

        # no part_class defined
        self.assertRaisesMessage(
            ImproperlyConfigured,
            'Please specify a base class for the parts that are to be loaded',
            MultiTypePartRegistry.load
        )

        MultiTypePartRegistry.part_class = object

        # no subpath defined
        self.assertRaisesMessage(
            ImproperlyConfigured,
            'Please specify a python sub path for the function that is to be called',
            MultiTypePartRegistry.load
        )

        MultiTypePartRegistry.call_function_subpath = 'subpath.load'

        with patch('django_appregistration.MultiTypePartRegistry._checked_apps') as _checked_apps:

            # should not find the module and therefore raise an import error
            _checked_apps.return_value=['non_existent']
            MultiTypePartRegistry.load()
            self.assertTrue(MultiTypePartRegistry.loaded)
            self.assertDictEqual(MultiTypePartRegistry.types, {})
            _checked_apps.assert_called_once_with()
            _checked_apps.reset_mock()
            MultiTypePartRegistry.reset()

            # should find the module but does not have the function
            _checked_apps.return_value=['django_appregistration.tests']
            MultiTypePartRegistry.load()
            self.assertTrue(MultiTypePartRegistry.loaded)
            self.assertDictEqual(MultiTypePartRegistry.types, {})
            _checked_apps.assert_called_once_with()
            _checked_apps.reset_mock()
            MultiTypePartRegistry.reset()

            with patch('django_appregistration.tests.subpath') as subpath:
                # finds the module but load is not callable
                subpath.load = object()
                MultiTypePartRegistry.load()
                self.assertTrue(MultiTypePartRegistry.loaded)
                self.assertDictEqual(MultiTypePartRegistry.types, {})
                _checked_apps.assert_called_once_with()
                _checked_apps.reset_mock()
                MultiTypePartRegistry.reset()

                subpath.load = MagicMock()
                MultiTypePartRegistry.load()
                self.assertTrue(MultiTypePartRegistry.loaded)
                self.assertDictEqual(MultiTypePartRegistry.types, {})
                subpath.load.assert_called_once_with(MultiTypePartRegistry)
                _checked_apps.assert_called_once_with()
                _checked_apps.reset_mock()
                MultiTypePartRegistry.reset()

            # already loaded
            MultiTypePartRegistry.loaded=True
            MultiTypePartRegistry.load()
            self.assertDictEqual(MultiTypePartRegistry.types, {})
            self.assertEqual(_checked_apps.call_count, 0)
            _checked_apps.reset_mock()

    @patch('django_appregistration.MultiTypePartRegistry.load')
    @patch('django_appregistration.MultiTypePartRegistry.sort_parts', return_value=[])
    def test_get(self, sort_parts, load):
        MultiTypePartRegistry.types = {
            'exists': [1,2,3]
        }
        # type not in types
        ret = MultiTypePartRegistry.get('not_existent')
        self.assertListEqual(ret, [])
        load.assert_called_once_with()
        sort_parts.assert_called_once_with([])
        load.reset_mock()
        sort_parts.reset_mock()

        # type exists
        ret = MultiTypePartRegistry.get('exists')
        self.assertListEqual(ret, [])
        load.assert_called_once_with()
        sort_parts.assert_called_once_with([1,2,3])
        load.reset_mock()
        sort_parts.reset_mock()

    def test_sort_parts(self):
        l = [object()]
        self.assertEqual(MultiTypePartRegistry.sort_parts(l), l)

class SingleTypePartRegistryTestCase(TestCase):
    @patch('django_appregistration.MultiTypePartRegistry.add_item')
    def test_add_item(self, add_item):
        id_obj = object()
        SingleTypePartRegistry.add_item(id_obj)
        add_item.assert_called_once_with('', id_obj)

    @patch('django_appregistration.MultiTypePartRegistry.get', return_value='return')
    def test_get(self, get):
        ret = SingleTypePartRegistry.get()
        self.assertEqual(ret, 'return')
        get.assert_called_once_with('')



