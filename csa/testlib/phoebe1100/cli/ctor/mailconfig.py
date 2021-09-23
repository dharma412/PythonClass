#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/mailconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

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
