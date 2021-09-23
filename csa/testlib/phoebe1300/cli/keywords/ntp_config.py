#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/ntp_config.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase
from common.cli import cliexceptions


class NtpConfig(CliKeywordBase):
    """Configure NTP time server."""

    def get_keyword_names(self):
        return ['ntp_config_new',
                'ntp_config_delete',
                'ntp_config_sourceint',
                'ntp_config_get_ntp_info',
                ]

    def ntp_config_new(self, server='time.ironport.com'):
        """Add NTP server.

        ntpconfig > new

        Parameters:
        - `server`: fully qualified hostname or IP address of NTP server to be
        added. Default value: 'time.ironport.com'.

        Examples:
        | NTP Config New |

        | NTP Config New | server='time1.ironport.com' |
        """

        self._cli.ntpconfig().new(server)

    def ntp_config_delete(self, server):
        """Remove NTP server.

        ntpconfig > delete

        Parameters:
        - `server`: name of the NTP server you wish to remove.

        Example:
        | NTP Config Delete | time.ironport.com |
        """

        self._cli.ntpconfig().delete(server)

    def ntp_config_sourceint(self, table='Auto'):
        """Choose the routing table to use.

        ntpconfig > sourceint

        Parameters:
        - `table`: routing table to be used. Available values: 'Auto',
        'Management'. Default value 'Auto'.

        Example:
        | NTP Config Routing Table |

        | NTP Config Routing Table | table=Management |
        """

        self._cli.ntpconfig().sourceint(table)

    def ntp_config_get_ntp_info(self):
        """Get info about configured NTPs.

        Return:
            Return list with currently configured NTPs.

        Example:
        | @{result}= | NTP Config Get NTP Info |
        """

        result = self._cli.ntpconfig().get_ntp_info()
        return result
