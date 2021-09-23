#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/sievechar.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
SARF CLI command: sievechar
"""
import clictorbase as ccb

DEBUG = True
DEFAULT = ccb.DEFAULT


class sievechar(ccb.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def setup(self, char=DEFAULT):
        # Valid characters are: -_=+/^#
        self.newlines = 1
        self._query_response('SETUP')
        self._query_response(char)
        self._to_the_top(self.newlines)
