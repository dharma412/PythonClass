#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/wipe_data.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

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
