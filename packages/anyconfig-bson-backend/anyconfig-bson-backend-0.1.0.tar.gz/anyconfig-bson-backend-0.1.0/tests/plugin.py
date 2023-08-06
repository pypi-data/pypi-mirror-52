#
# Copyright (C) 2018 Satoru SATOH <satoru.satoh @ gmail.com>
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name
from __future__ import absolute_import, print_function

import os.path
import os
import pkg_resources
import unittest

import anyconfig
import anyconfig.backends

from tests.common import dicts_equal


_CURDIR = os.path.dirname(__file__)
_CNF_0 = {u'a': 0,
          u'b': u'bbb',
          u'c': 5,
          u'sect0': {u'd': [u'x', u'y', u'z']}}


class Test(unittest.TestCase):

    conf_path = os.path.join(_CURDIR, "0.bson")

    def test_20_load(self):
        try:
            cnf = anyconfig.load(self.conf_path)
        except anyconfig.UnknownFileTypeError:
            for entry in pkg_resources.iter_entry_points("anyconfig_backends"):
                print("%r" % entry)
                psr = entry.load()
                print("%r" % psr)
                print("type=%r, exts=%r" % (psr.type(), psr.extensions()))

            print("all types=%r" % anyconfig.list_types())
            raise

        self.assertTrue(dicts_equal(cnf, _CNF_0))

# vim:sw=4:ts=4:et:
