#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/sievechar.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

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
        self.newlines=1
        self._query_response('SETUP')
        self._query_response(char)
        self._to_the_top(self.newlines)