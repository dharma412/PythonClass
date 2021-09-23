#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/ntp_config.py#1 $

from common.cli.clicommon import CliKeywordBase
from common.cli import cliexceptions

class NtpConfig(CliKeywordBase):
    """Configure NTP time server."""

    def get_keyword_names(self):
        return ['ntp_config_new',
                'ntp_config_delete',
                'ntp_config_routing_table',
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
        - `server`: number of the NTP server you wish to remove.

        Example:
        | NTP Config Delete | 1 |
        """

        if not server.strip().isdigit() or int(server.strip()) == 0:
            raise cliexceptions.ConfigError(
                'Value must be a number greater than zero.')
        self._cli.ntpconfig().delete(server)

    def ntp_config_routing_table(self, table='Data'):
        """Choose the routing table to use.

        ntpconfig > routing table

        Parameters:
        - `table`: routing table to be used. Available values: 'Data',
        'Management'. Default value 'Data'.

        Example:
        | NTP Config Routing Table |

        | NTP Config Routing Table | table=Management |
        """

        self._cli.ntpconfig().routingtable(table)

    def ntp_config_get_ntp_info(self):
        """Get info about configured NTPs.

        Example:
        | ${result}= | NTP Config Get NTP Info |
        | Log | ${result} |
        """

        output = self._cli.ntpconfig().get_ntp_info()
        return output
