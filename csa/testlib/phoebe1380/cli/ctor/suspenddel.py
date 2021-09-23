#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/suspenddel.py#1 $

"""
IAF Command Line Interface (CLI)

command:
    - suspenddel
"""
import clictorbase

class suspenddel(clictorbase.IafCliConfiguratorBase):
    def __call__(self, delay='', domains_str='ALL'):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        self._query_response(delay)
        if delay:
            timeout = int(delay) + 5
        else:
            timeout = 35
        self._query_response(domains_str)
        return self._wait_for_prompt(timeout=timeout)
