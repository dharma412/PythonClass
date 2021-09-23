#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/mailconfig.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

"""
IAF 2 CLI command: mailconfig
"""

import clictorbase
import socket

from sal.containers.yesnodefault import YES, NO


class mailconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self, email='test@test.qa', option=1):
        self._sess.writeln('mailconfig')
        self._query_response(email)
        self._query_response(option, timeout=10)
        self._wait_for_prompt()
