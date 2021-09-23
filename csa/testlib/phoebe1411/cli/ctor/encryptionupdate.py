#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/encryptionupdate.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

"""
SARF CLI command: encryptionupdate
"""
import clictorbase
from sal.deprecated.expect import EXACT

class encryptionupdate(clictorbase.IafCliConfiguratorBase):
    """
    Possible response:
        1. PXE Encryption not enabled. Engine not updated.
        2. Requesting update of PXE Engine.
    """
    def __call__(self):
        pats = [
            ("PXE Encryption not enabled. Engine not updated.", EXACT),
            ("Requesting update of PXE Engine.", EXACT),
        ]
        self._sess.clearbuf()
        self._writeln(self.__class__.__name__)
        raw = self._expect(pats, timeout=15)
        self._wait_for_prompt()
        return raw.string