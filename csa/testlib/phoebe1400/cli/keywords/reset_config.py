#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase
import time

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
        maxvalue = 30
        for count in range(maxvalue):
            time.sleep(1)
            try:
                self.start_cli_session_if_not_open(password='ironport')
                break
            except Exception as error:
                self._debug('ERROR:%s' %error)

            if count == maxvalue:
                self._debug('ERROR: MAX Retry Reached:%s' % error)
                raise error
