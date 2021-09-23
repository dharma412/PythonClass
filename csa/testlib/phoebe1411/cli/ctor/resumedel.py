#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/resumedel.py#1 $

"""
IAF 2 Command Line Interface (CLI)

command:
    - resumedel
"""
import clictorbase
from sal.exceptions import ConfigError

TIMEOUT = 30

class resumedel(clictorbase.IafCliConfiguratorBase):
    def __call__(self, domains_str='ALL'):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        self._query_response(domains_str)

        no = self._query('Mail delivery resumed',
                         'cannot resume')
        if no == 0:
            self._wait_for_prompt(timeout=TIMEOUT)
            return True
        elif no == 1:
            raise ConfigError, "%s: delivery could not be resumed"\
                               % self.__class__.__name__
        else:
            raise ConfigError, "%s command execution error"\
                               % self.__class__.__name__

