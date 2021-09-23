#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/nslookup.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $
"""
IAF2 CLI command nslookup
"""

from sal.containers.yesnodefault import YES, NO
from sal.deprecated.expect import EXACT

import clictorbase

REQUIRED = clictorbase.REQUIRED
DEFAULT = clictorbase.DEFAULT

class MalformedQueryError(clictorbase.IafCliError): pass

class nslookup(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('DNS Malformed Query Error', EXACT):MalformedQueryError,
            })


    def __call__(self, host=REQUIRED, query_type=DEFAULT):
        self._writeln(self.__class__.__name__)

        self._expect([("enter the host or IP address to resolve", EXACT)], timeout=3)
        self._query_response(host)

        self._expect(['Choose the query type:', 'PTR='],
                     timeout=3)
        if self._expectindex == 1:
            return 'PTR=' + ' '.join(self._wait_for_prompt().splitlines()[:-1])
        else:
            self._query_select_list_item(query_type)

        return ' '.join(self._wait_for_prompt().splitlines()[2:-1])
