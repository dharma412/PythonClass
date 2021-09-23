#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/wipe_data.py
# $DateTime: 2020/05/28 03:18:30 $ $Author: mrmohank $

from common.cli.clicommon import CliKeywordBase

class WipeData(CliKeywordBase):
    """
    cli -> wipedata
    """
    def get_keyword_names(self):
        return [
                'wipedata_status',
                'wipedata_coredump',
                ]

    def wipedata_status(self):
        """Display status of last command run.

        wipedata > status

        *Example:*
        | ${wipestatus} | Wipedata Status |
        | Log | ${wipestatus} |
        """
        return self._cli.wipedata().status()

    def wipedata_coredump(self):
        """Wipe core files on disk.

        wipedata > coredump

        *Example:*
        | ${wipestatus} | Wipedata Coredump |
        | Log | ${wipestatus} |
        """
        return self._cli.wipedata().coredump()
