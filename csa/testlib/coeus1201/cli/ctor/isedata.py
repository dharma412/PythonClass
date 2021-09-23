#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/isedata.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import clictorbase
from clictorbase import IafCliConfiguratorBase

class isedata(clictorbase.IafCliConfiguratorBase):
    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def cache_clear(self):
        self.clearbuf()
        self._expect('Choose the operation')
        self._writeln('CACHE')
        self._expect('Choose the operation')
        self._writeln('CLEAR')
        self._expect('Are you sure')
        self._writeln('Y')
        self._to_the_top(3)
        return self.getbuf()

    def cache_show(self):
        self._expect('Choose the operation')
        self._writeln('CACHE')
        self._expect('Choose the operation')
        self.clearbuf()
        self._writeln('SHOW')
        self._to_the_top(3)
        return self.getbuf()

    def sgts(self):
        self._expect('Choose the operation')
        self.clearbuf()
        self._writeln('SGTS')
        self._to_the_top(2)
        return self.getbuf()

    def checkip(self, ip_address):
        self.clearbuf()
        self._expect('Choose the operation')
        self._writeln('CACHE')
        self._expect('Choose the operation')
        self._writeln('CHECKIP')
        self._expect('Enter an IP address')
        self._writeln(ip_address)
        self._to_the_top(3)
        return self.getbuf()

