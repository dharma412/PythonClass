#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/supportrequeststatus.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

"""
SARF CLI Command: supportrequeststatus
"""

import clictorbase
import re
from sal.containers.yesnodefault import is_yes, YES

class supportrequeststatus(clictorbase.IafCliConfiguratorBase):
    def __call__(self, as_dictionary=YES):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        raw = self._sess.read_until()
        if raw.find('Unknown command') > -1:
            raise clictorbase.IafUnknownCommandError
        if is_yes(as_dictionary):
            support_request_compile = re.compile('(^Support Request)[\s\t]+ (?P<version>.*)[\s\t]+ (?P<last_updated>.*)', re.MULTILINE|re.IGNORECASE)
            status = {'support_request': re.search(support_request_compile, raw).groupdict(),}
            return status
        return raw
