from django.utils import unittest


class AttributeDictMixin(object):
    """Adds attribute access to mappings.

    >>> d.key -> d[key]
    """

    def __getattr__(self, key):
        """`d.key -> d[key]`"""
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" % (
                    self.__class__.__name__, key))

    def __setattr__(self, key, value):
        """`d[key] = value -> d.key = value`"""
        self[key] = value


class AttributeDict(dict, AttributeDictMixin):
    pass


class NginxConfTest(unittest.TestCase):

    def setUp(self):
        self.settings = AttributeDictMixin({
            '': '',
            '': '',
        })



