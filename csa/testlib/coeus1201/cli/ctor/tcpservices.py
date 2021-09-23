#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/tcpservices.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import clictorbase
from sal.exceptions import ConfigError

class tcpservices(clictorbase.IafCliConfiguratorBase):
    """
    Display information about open TCP/IP services.
    """
    def __call__(self, option=None):
        options = [ 'system', 'features', 'info']
        if option is not None:
            if option not in options:
                raise ConfigError, 'Uknown option - %s' % option
        self.clearbuf
        result = ''
        cmd = "tcpservices"
        if option is not None:
            cmd = ' '.join([cmd, option])
        self._writeln(cmd)

        # Removing input (first 2 lines) and final prompt (last line)
        lines = self._wait_for_prompt().split("\n")
        for number in range(2,len(lines) - 1):
            result += lines[number]

        return result
