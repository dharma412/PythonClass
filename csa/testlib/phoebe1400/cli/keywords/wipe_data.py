#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/wipe_data.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

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
