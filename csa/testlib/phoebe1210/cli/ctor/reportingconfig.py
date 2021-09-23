#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/reportingconfig.py#1 $

import clictorbase

from sal.containers.yesnodefault import NO, YES

REQUIRED = clictorbase.REQUIRED
DEFAULT = clictorbase.DEFAULT


class reportingconfig(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln('reportingconfig')
        return self

    def mailsetup(self):
        self._query_response('MAILSETUP')
        return reportingconfigMailsetup(self._get_sess())

    def setup(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['enable'] = \
            ['enable Centralized Reporting', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)


class reportingconfigMailsetup(clictorbase.IafCliConfiguratorBase):
    """reportingconfig -> mailsetup"""

    level = 2

    def senderbase(self, timeout=DEFAULT):
        self._query_response('SENDERBASE')
        self._query_response(timeout)
        self._to_the_top(self.level)

    def multiplier(self, multiplier=DEFAULT):
        self._query_response('MULTIPLIER')
        self._query_response(multiplier)
        self._to_the_top(self.level)

    def counters(self, level=DEFAULT):
        self._query_response('COUNTERS')
        self._query_select_list_item(level)
        self._to_the_top(self.level)

    def throttling(self, max_unique_hosts=DEFAULT):
        self._query_response('THROTTLING')
        self._query_response(max_unique_hosts)
        self._to_the_top(self.level)

    def tld(self):
        self._query_response('TLD')
        return reportingconfigMailsetupTld(self._get_sess())

    def legacy(self, enable=DEFAULT):
        self._query_response('LEGACY')
        self._query_response(enable)
        self._to_the_top(self.level)


class reportingconfigMailsetupTld(clictorbase.IafCliConfiguratorBase):
    """reportingconfig -> mailsetup -> tld"""

    level = 3

    def add(self, host_list=REQUIRED):
        self._query_response('ADD')
        self._writeln(host_list)
        self._writeln('.')
        self._to_the_top(self.level)

    def replace(self, host_list=REQUIRED):
        self._query_response('REPLACE')
        self._writeln(host_list)
        self._writeln('.')
        self._to_the_top(self.level)

    def clear(self):
        self._query_response('CLEAR')
        self._to_the_top(self.level)


if __name__ == '__main__':
    import time

    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    rc = reportingconfig(cli_sess)

    rc().mailsetup().senderbase()
    rc().mailsetup().senderbase(timeout=15)

    rc().mailsetup().multiplier()
    rc().mailsetup().multiplier(multiplier=9)

    rc().mailsetup().counters()
    rc().mailsetup().counters(level=1)

    rc().mailsetup().throttling(max_unique_hosts=10)
    rc().mailsetup().throttling()

    rc().mailsetup().tld().add(host_list='com')
    rc().mailsetup().tld().replace(host_list='qa')
    rc().mailsetup().tld().clear()

    rc().mailsetup().legacy()
    rc().mailsetup().legacy(enable=YES)
    rc().mailsetup().legacy(enable=NO)

    rc().mode()
    rc().mode(enable=YES)
    rc().mode(enable=NO)
