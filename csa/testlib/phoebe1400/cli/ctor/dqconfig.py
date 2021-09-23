#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/dqconfig.py#1 $
# $DateTime: 2020/01/17 04:04:23 $
# $Author: aminath $

"""ESA Command Line Interface (CLI): dqconfig
"""

import functools
import re
from sal.containers.yesnodefault import YES, NO
from clictorbase import IafCliConfiguratorBase, IafCliFeatureNotEnabled
from sal.exceptions import TimeoutError

def check_cpq_is_enabled(func):
    @functools.wraps(func)
    def decorator(self, *args, **kwargs):
        expected_message1 = 'Choose the operation you want to perform'
        expected_message2 = 'Delayed Quarantine feature is not enabled'
        expected_message3 = 'Delayed Quarantine would be available only ' \
                           'when centralized quarantine'
        try:
            self._expect([expected_message1,
                                expected_message2,
                                expected_message3],
                                timeout=5)
            if self._expectindex == 0:
                self._is_enabled = True
            elif self._expectindex == 1:
                self._is_enabled = False
            else:
                raise IafCliFeatureNotEnabled(
                        'ERROR: Centralized Quarantine is NOT enabled. ' \
                        'Please enable Centralized Quarantine before ' \
                        'executing dqconfig command')
        except TimeoutError as e:
            self._debug('Expected message did not appear in CLI session')
        return func(self, *args, **kwargs)
    return decorator

class dqconfig(IafCliConfiguratorBase):
    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self.clearbuf()
        self._writeln('dqconfig')
        return self

    @check_cpq_is_enabled
    def is_enabled(self):
        self._to_the_top(1)
        return True if self._is_enabled == 1 else False

    @check_cpq_is_enabled
    def enable(self):
        if self._is_enabled:
            self._info("Delayed Quarantine is already enabled")
        else:
            self._query_response('YES')
        self._to_the_top(1)

    @check_cpq_is_enabled
    def disable(self):
        if self._is_enabled:
            self._query_response('DISABLEDQ')
            self._query_response('YES')
        else:
            self._info("Delayed Quarantine check is already disabled")
        self._to_the_top(1)

    @check_cpq_is_enabled
    def list_mids(self):
        if self._is_enabled:
            self._query_response('LISTMIDS')
            self._to_the_top(1)
            output = self.getbuf()
            if output:
                mid_list = re.search(r'MIDs in delayed quarantine:\s+\[(.*)\]', output)
                if mid_list:
                    return mid_list.group(1).split(',')
                else:
                    return []
            else:
                self._warn('Empty output for LISTMIDS command')
        else:
            self._warn('Delayed Quarantine is not enabled')
            self._to_the_top(1)

    @check_cpq_is_enabled
    def release_messages(self):
        if self._is_enabled:
            self._query_response('RELEASEMESSAGES')
        else:
            self._warn('Delayed Quarantine is not enabled')
        self._to_the_top(1)

    @check_cpq_is_enabled
    def modify_retention_time(self, retention_time):
        if self._is_enabled:
            self._query_response('MODIFYRETENTIONTIME')
            self._query_response(retention_time)
        else:
            self._warn('Delayed Quarantine is not enabled')
        self._to_the_top(1)
