#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/networktuning.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $
"""
    IAF 2 CLI ctor - networktuning
"""
import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, \
                IafCliError, IafIpHostnameError, IafUnknownOptionError, \
                REQUIRED, DEFAULT
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import YES, NO
DEBUG = True
class DuplicateEntry(IafCliError): pass
class UnknownOptionError(IafCliError): pass
class networktuning(clictorbase.IafCliConfiguratorBase):
    newlines = 2

    def __call__(self):
        self._restart()
        self._writeln('networktuning')
        return self

    def send_space(self, input_dict=None, send_space=''):
        self._query_response('SENDSPACE')
        self._query('Enter the new value of sendspace')
        self._query_response(send_space)
        self._to_the_top(1)

    def recv_space(self, input_dict=None, recv_space=''):
        self._query_response('RECVSPACE')
        self._query('Enter the new value of recvspace')
        self._query_response(recv_space)
        self._to_the_top(1)

    def send_auto(self, input_dict=None, sendbuf_auto=''):
        self._query_response('SEND_AUTO')
        self._query('enable the sendbuf_auto')
        self._query_response(sendbuf_auto)
        self._to_the_top(1)

    def recv_auto(self, input_dict=None, recvbuf_auto=''):
        self._query_response('RECV_AUTO')
        self._query('enable the recvbuf_auto')
        self._query_response(recvbuf_auto)
        self._to_the_top(1)

    def mbuf_cluster_count(self, input_dict=None, nmbclusters=''):
        self._query_response('MBUF_CLUSTER_COUNT')
        self._query('Enter the new value of nmbclusters')
        self._query_response(nmbclusters)
        self._to_the_top(1)

    def send_buf_max(self, input_dict=None, sendbuf_max=''):
        self._query_response('SENDBUF_MAX')
        self._query('Enter the new value of sendbuf_max')
        self._query_response(sendbuf_max)
        self._to_the_top(1)

    def recv_buf_max(self, input_dict=None, recvbuf_max=''):
        self._query_response('RECVBUF_MAX')
        self._query('Enter the new value of recvbuf_max')
        self._query_response(recvbuf_max)
        self._to_the_top(1)

    def clean_fib_1(self, input_dict=None, route_value=''):
        self._info("DEBUG***")
        self._query_response('CLEAN_FIB_1')
        self._query('Add default Management')
        self._query_response(route_value)
        self._to_the_top(1)
