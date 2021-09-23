#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/showrecipients.py#1 $ $DateTime: 2019/09/18 01:46:35 $  $Author: sarukakk $

import re

from clictorbase import IafCliConfiguratorBase, DEFAULT, \
    IafCliCtorNotImplementedError

START_OF_GOODPUT = 'Recipient'


class showrecipients(IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self, how, recipient_host, envelop_from, issensitive,
                 raw_output):

        self._writeln('showrecipients')
        idx = self._query_select_list_item(how)

        if idx == 1:
            self._expect("enter the hostname", timeout=5)
            self._writeln(recipient_host)

        if idx == 2:
            self._expect("enter the Envelope", timeout=5)
            self._writeln(envelop_from)
            self._query_response(issensitive)

        out = self._wait_for_prompt()
        if raw_output:
            return out
        return self._normalize_result(out)

    def _normalize_result(self, data):

        # Result list
        pattern = re.compile('(\s{2,})')
        start_line = 0
        result = []
        lines = data.split('\n')
        for i in range(0, len(lines) - 1):
            if START_OF_GOODPUT in lines[i]:
                start_line = i
                continue
            if start_line and lines[i][:-1] != '':
                result.append(lines[i][:-1])

        return result
