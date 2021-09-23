#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/quotaquery.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import sys

import clictorbase
import sal.containers.yesnodefault as yesnodefault
from clictorbase import IafCliConfiguratorBase,IafCliError, \
                        REQUIRED, DEFAULT
from sal.deprecated.expect import REGEX, EXACT
import sal.containers.yesnodefault as yesnodefault

DEBUG = True

class quotaquery(clictorbase.IafCliConfiguratorBase):
    """quotaquery
    """
    newlines = 1

    def __call__(self):
        self._writeln('quotaquery')
        return self

    def reset(self, search_str=REQUIRED):
        self._query_response('RESET')
        try:
            self._query_response(search_str)
            return self._to_the_top(self.newlines)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.interrupt()
            raise exc_type, exc_value, exc_traceback

    def resetall(self):
        self._query_response('RESETALL')
        try:
            self._query_response('YES')
            return self._to_the_top(self.newlines)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.interrupt()
            raise exc_type, exc_value, exc_traceback

    def search(self, search_str=REQUIRED):
        self._query_response('SEARCH')
        try:
            self._query_response(search_str)
            return self._to_the_top(self.newlines)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.interrupt()
            raise exc_type, exc_value, exc_traceback
