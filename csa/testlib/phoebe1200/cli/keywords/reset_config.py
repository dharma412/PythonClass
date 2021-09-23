#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/reset_config.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class ResetConfig(CliKeywordBase):
    """Restore the factory configuration defaults."""

    def get_keyword_names(self):
        return ['reset_config', ]

    def reset_config(self, timeout=900):
        """Reset Config.

        Use this keyword to restore the factory configuration defaults.

        *Parameters*:
        - `timeout`: Optional parameter that is used only in case we reset the DUT that is in the FIPS mode. Defaults to 900s.

        Exceptions:
        - `ConfigError`: in case machine has not been suspended.

        Example:
        | Reset Config |
        """
        self._cli.resetconfig(self.dut, self.dut_version, timeout=timeout)
        self.start_cli_session_if_not_open()
