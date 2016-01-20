# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
from django.core.exceptions import ImproperlyConfigured

from django.test import TestCase
from mock import patch, MagicMock
from django_appregistration import MultiListPartRegistry, SingleListPartRegistry

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
        MultiListPartRegistry.reset()
        MultiListPartRegistry.part_class = None
        MultiListPartRegistry.ignore_django_namespace = True
        MultiListPartRegistry.call_function_subpath = None

    def test_reset(self):
        MultiListPartRegistry.loaded = True
        MultiListPartRegistry.lists = {'type': []}

        MultiListPartRegistry.reset()

        self.assertFalse(MultiListPartRegistry.loaded)
        self.assertDictEqual(MultiListPartRegistry.lists, {})

    @patch('django_appregistration.settings.INSTALLED_APPS', ['django.test.app', 'app1', 'app2.django.test'])
    def test__checked_apps(self):
        MultiListPartRegistry.ignore_django_namespace = False
        self.assertListEqual(
            MultiListPartRegistry._checked_apps(),
            ['django.test.app', 'app1', 'app2.django.test'],
        )

        MultiListPartRegistry.ignore_django_namespace = True
        self.assertListEqual(
            MultiListPartRegistry._checked_apps(),
            ['app1', 'app2.django.test'],
        )

    def test_add_part(self):
        class Test(object):
            pass
        MultiListPartRegistry.part_class = Test

        self.assertRaises(ValueError, MultiListPartRegistry.add_part, '', object())

        test = Test()
        MultiListPartRegistry.add_part('Test', test)
        MultiListPartRegistry.add_part('Test', test)
        MultiListPartRegistry.add_part('Test2', test)

        self.assertDictEqual(
            MultiListPartRegistry.lists,
            {
                'Test': [test, test],
                'Test2': [test],
            }
        )

    def test_load(self):
        lock_mock = MagicMock()
        MultiListPartRegistry.lock = lock_mock

        # no part_class defined
        self.assertRaisesMessage(
            ImproperlyConfigured,
            'Please specify a base class for the parts that are to be loaded',
            MultiListPartRegistry.load
        )

        MultiListPartRegistry.part_class = object

        # no subpath defined
        self.assertRaisesMessage(
            ImproperlyConfigured,
            'Please specify a python sub path for the function that is to be called',
            MultiListPartRegistry.load
        )

        MultiListPartRegistry.call_function_subpath = 'subpath.load'

        with patch('django_appregistration.MultiListPartRegistry._checked_apps') as _checked_apps:

            # should not find the module and therefore raise an import error
            _checked_apps.return_value=['non_existent']
            MultiListPartRegistry.load()
            self.assertTrue(MultiListPartRegistry.loaded)
            self.assertDictEqual(MultiListPartRegistry.lists, {})
            _checked_apps.assert_called_once_with()
            _checked_apps.reset_mock()
            MultiListPartRegistry.reset()

            # should find the module but does not have the function
            _checked_apps.return_value=['django_appregistration.tests']
            MultiListPartRegistry.load()
            self.assertTrue(MultiListPartRegistry.loaded)
            self.assertDictEqual(MultiListPartRegistry.lists, {})
            _checked_apps.assert_called_once_with()
            _checked_apps.reset_mock()
            MultiListPartRegistry.reset()

            with patch('django_appregistration.tests.subpath') as subpath:
                # finds the module but load is not callable
                subpath.load = object()
                MultiListPartRegistry.load()
                self.assertTrue(MultiListPartRegistry.loaded)
                self.assertDictEqual(MultiListPartRegistry.lists, {})
                _checked_apps.assert_called_once_with()
                _checked_apps.reset_mock()
                MultiListPartRegistry.reset()

                subpath.load = MagicMock()
                MultiListPartRegistry.load()
                self.assertTrue(MultiListPartRegistry.loaded)
                self.assertDictEqual(MultiListPartRegistry.lists, {})
                subpath.load.assert_called_once_with(MultiListPartRegistry)
                _checked_apps.assert_called_once_with()
                _checked_apps.reset_mock()
                MultiListPartRegistry.reset()

            # already loaded
            MultiListPartRegistry.loaded=True
            MultiListPartRegistry.load()
            self.assertDictEqual(MultiListPartRegistry.lists, {})
            self.assertEqual(_checked_apps.call_count, 0)
            _checked_apps.reset_mock()

    @patch('django_appregistration.MultiListPartRegistry.load')
    @patch('django_appregistration.MultiListPartRegistry.sort_parts', return_value=[])
    def test_get(self, sort_parts, load):
        MultiListPartRegistry.lists = {
            'exists': [1,2,3]
        }
        # type not in types
        ret = MultiListPartRegistry.get('not_existent')
        self.assertListEqual(ret, [])
        load.assert_called_once_with()
        sort_parts.assert_called_once_with([])
        load.reset_mock()
        sort_parts.reset_mock()

        # type exists
        ret = MultiListPartRegistry.get('exists')
        self.assertListEqual(ret, [])
        load.assert_called_once_with()
        sort_parts.assert_called_once_with([1,2,3])
        load.reset_mock()
        sort_parts.reset_mock()

    def test_sort_parts(self):
        l = [object()]
        self.assertEqual(MultiListPartRegistry.sort_parts(l), l)

class SingleTypePartRegistryTestCase(TestCase):
    @patch('django_appregistration.MultiListPartRegistry.add_part')
    def test_add_part(self, add_part):
        id_obj = object()
        SingleListPartRegistry.add_part(id_obj)
        add_part.assert_called_once_with('', id_obj)

    @patch('django_appregistration.MultiListPartRegistry.get', return_value='return')
    def test_get(self, get):
        ret = SingleListPartRegistry.get()
        self.assertEqual(ret, 'return')
        get.assert_called_once_with('')



