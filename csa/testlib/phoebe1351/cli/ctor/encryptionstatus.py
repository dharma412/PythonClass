#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/encryptionstatus.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

"""
SARF CLI Command: encryptionstatus
"""

import clictorbase
import re
from sal.containers.yesnodefault import is_yes, YES

class encryptionstatus(clictorbase.IafCliConfiguratorBase):
    def __call__(self, as_dictionary=YES):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        raw = self._sess.read_until()
        if raw.find('Unknown command') > -1:
            raise clictorbase.IafUnknownCommandError
        if is_yes(as_dictionary):
            pxe_eng_compile = re.compile('(^PXE Engine)[\s\t]+ (?P<version>.*)[\s\t]+ (?P<last_updated>.*)', re.MULTILINE|re.IGNORECASE)
            domain_mapping_compile = re.compile('(^Domain Mappings File)[\s\t]+ (?P<version>.*)[\s\t]+ (?P<last_updated>.*)', re.MULTILINE|re.IGNORECASE)
            status = {'pxe_engine': re.search(pxe_eng_compile, raw).groupdict(),
                      'domain_mapping':re.search(domain_mapping_compile, raw).groupdict(),}
            return status
        return raw

