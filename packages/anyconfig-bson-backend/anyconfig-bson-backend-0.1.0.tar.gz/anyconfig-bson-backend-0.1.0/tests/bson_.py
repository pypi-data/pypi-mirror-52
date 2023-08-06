#
# Copyright (C) 2015 - 2018 Satoru SATOH <ssato @ redhat.com>
# Copyright (C) 2017 Red Hat, Inc.
# License: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
from __future__ import absolute_import

import anyconfig_bson_backend as TT
import bson
import tests.common as TBC


class HasParserTrait(TBC.HasParserTrait):

    psr = TT.Parser()
    cnf = TBC.CNF_2
    cnf_s = bson.BSON.encode(cnf)


class Test_10(TBC.Test_10_dumps_and_loads, HasParserTrait):

    # Can't if bson.has_c():
    if not bson.has_c():
        load_options = dict(as_class=dict)
        dump_options = dict(check_keys=True)
        empty_patterns = ['']


class Test_20(TBC.Test_20_dump_and_load, HasParserTrait):

    pass

# vim:sw=4:ts=4:et:
