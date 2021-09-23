#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/reset_config.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase
from common.util.unset_https import UnsetHttps
import common.Variables

class ResetConfig(CliKeywordBase):
    """Restore the factory configuration defaults."""

    def get_keyword_names(self):
        return [
            'reset_config',
        ]

    def reset_config(self, reset_network='yes'):
        """Reset Config.

        Use this keyword to restore the factory configuration defaults.
        Parameters:
        - `reset_network`: Either 'yes' or 'no'. Indicates whether network settings
        should be reset.

        Example:
        | Reset Config |
        | Reset Config | reset_network=no |
        """
        reset_network = self._process_yes_no(reset_network)
        self._cli.resetconfig(reset_network)
        variables = common.Variables.get_variables()
        if variables.has_key("${DUT_PROTOCOL}"):
            if variables["${DUT_PROTOCOL}"] == 'http':
                UnsetHttps(self.dut, self.dut_version).unset_https()

