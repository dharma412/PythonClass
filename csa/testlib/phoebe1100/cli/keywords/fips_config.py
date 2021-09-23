#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/fips_config.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class FipsConfig(CliKeywordBase):
    """Change FIPS configuration.
    """

    def get_keyword_names(self):
        return ['fips_config',
                'fips_config_is_enabled']

    def fips_config(self, action, always_encrypt='yes', timeout=900):
        """Change current FIPS mode.
        Will pass silently if already disabled/enabled.

        *Warning:*
        - This keyword will restart your appliance if
        current FIPS mode differs from passed 'action'
        value. Then this will wait automatically until
        the appliance reboots and restarts CLI session.
        Do not forget to take care about GUI session
        restart if necessary

        - Care should be taken while changing only the encryption option.
        If Fips is already enabled, should disable it first and then
        re-enable with the required encryption option.

        *Parameters:*
        - `action`: 'enable' to enable and 'disable' to disable FIPS
        - `always_encrypt`: Either 'yes' or 'no'. Default is 'yes'
        Whether to enable encryption to sensitive data in configuration file
        - `timeout`: maximum number of seconds to wait until appliance
        reboots

        *Exceptions:*
        - `ValueError`: if action parameter has incorrect value
        - `ConfigError`: if the system has failed to reboot after
        mode change
        - `TimeoutError`: if the system has failed to close all
        opened connection before reboot

        *Return:*
        Current FIPS status (before the status has been changed with current command).
        Boolean: True - if FIPS was enabled, False - if FIPS was disabled.

        *Examples:*
        | ${was_enabled}= | FIPS Config | Enable |

        | ${was_enabled}= | FIPS Config | Disable |

        | ${was_enabled}= | FIPS Config | Enable | timeout=600 |

        | ${was_enabled}= | FIPS Config | Enable | always_encrypt=no | timeout=600 |

        | ${was_enabled}= | FIPS Config | Enable | always_encrypt=yes | timeout=600 |
        """
        action = str(action.lower())
        if action in ('enable', 'disable'):
            dest_method = getattr(self._cli.fipsconfig(), action)
            res = dest_method(self.dut, self.dut_version, action, always_encrypt, int(timeout))
            self.start_cli_session_if_not_open()
            return res
        else:
            raise ValueError('action should be either "disable" or "enable". ' \
                             'Given: %s' % (action,))

    def fips_config_is_enabled(self):
        """Get current FIPS feature status

        *Return:*
        ${True} or ${False} depending on current FIPS feature state

        *Examples:*
        | ${fips_state}= | FIPS Config Is Enabled |
        """
        return self._cli.fipsconfig().is_enabled()
