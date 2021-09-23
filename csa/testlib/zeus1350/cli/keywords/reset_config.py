#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/reset_config.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class ResetConfig(CliKeywordBase):
    """Restore the factory configuration defaults."""

    def get_keyword_names(self):
        return ['reset_config', ]

    def reset_config(self, confirm='yes'):
        """Reset Config.

        Use this keyword to restore the factory configuration defaults.

        Parameters:
        - `confirm`: confirm the reset of all configuration values. 'yes',
          'no' or 'default' to use default value.

        Exceptions:
        - `ConfigError`: in case machine has not been suspended.

        Example:
        | Reset Config |
        | Reset Config | no |
        | Reset Config | yes |
        """

        self._cli.resetconfig()
