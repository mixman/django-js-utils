from django.conf import settings
from django.test import TestCase

from django_js_utils import conf_jsutils
from django_js_utils.utils import PatternsParser

from collections import OrderedDict

class NoUrlName(TestCase):
    def test_urls(self):
        parser = PatternsParser()
        parser.parse(settings.ROOT_URLCONF)
        self.assertEquals(parser.patterns,
                OrderedDict([
                    ('index', '/index'),
                    ('computer-license-detail', '/api/computer/<id>/license/<field_pk>'),
                    ('model-view', '/model/<model>/<id>')]))

    def test_urls_prefix_exclude(self):
        parser = PatternsParser()
        with self.settings(URLS_EXCLUDE_PREFIX=['^api/']):
            parser.parse(settings.ROOT_URLCONF)
            self.assertEquals(parser.patterns,
                OrderedDict([('index', '/index'),
                    ('model-view', '/model/<model>/<id>')]))

    def test_urls_pattern_exclude(self):
        parser = PatternsParser()
        with self.settings(URLS_EXCLUDE_PATTERN=['index','model']):
            parser.parse(settings.ROOT_URLCONF)
            self.assertEquals(parser.patterns,
                OrderedDict([
                    ('computer-license-detail', '/api/computer/<id>/license/<field_pk>'),]))

    def test_urls_prefix_include(self):
        parser = PatternsParser()
        with self.settings(URLS_INCLUDE_PREFIX=['^$']):
            parser.parse(settings.ROOT_URLCONF)
            self.assertEquals(parser.patterns,
                OrderedDict([('index', '/index'),
                    ('model-view', '/model/<model>/<id>')]))

    def test_urls_prefix_include_named(self):
        parser = PatternsParser()
        with self.settings(URLS_INCLUDE_PREFIX=['^api']):
            parser.parse(settings.ROOT_URLCONF)
            self.assertEquals(parser.patterns,
                OrderedDict([('computer-license-detail', '/api/computer/<id>/license/<field_pk>')]))

    def test_urls_pattern_include(self):
        parser = PatternsParser()
        with self.settings(URLS_INCLUDE_PATTERN=['^model']):
            parser.parse(settings.ROOT_URLCONF)
            self.assertEquals(parser.patterns,
                OrderedDict([('model-view', '/model/<model>/<id>')]))
