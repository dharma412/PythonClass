#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/authcache.py#1 $
# $Author: uvelayut $
# $DateTime: 2019/08/14 09:58:47 $

"""
CLI command: authcache
"""
from clictorbase import IafCliConfiguratorBase

class authcache(IafCliConfiguratorBase):
    """authcache
        - This cli is used to manipulate authentication cache entries.
          It is ineffective under Forward mode NTLM with no surrogates
    """
    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._restart()
        self._writeln('authcache')
        return self

    def flushall(self):
        self._query_response('FLUSHALL')
        self._query_response('YES')
        self.clearbuf()
        return self._read_until('Choose the operation', timeout=30)

    def listcache(self):
        self._query_response('LIST')
        self._query_response('YES')
        self.clearbuf()
        return self._read_until('Choose the operation', timeout=120)

    def flushuser(self, user=None, realm=None):
        self._query_response('FLUSHUSER')
        self._query_select_list_item(realm)
        self._query_response(user)
        self.clearbuf()
        return self._read_until('Choose the operation', timeout=90)

    def search(self, searchstr=None):
        self._query_response('SEARCH')
        self._query_response(searchstr)
        self._query_response('YES')
        self.clearbuf()
        return self._read_until('Choose the operation', timeout=120)