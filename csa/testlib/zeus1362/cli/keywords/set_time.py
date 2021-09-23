#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/set_time.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class SetTime(CliKeywordBase):
    """Manually set the system clock.  Will disable NTP if it is enabled.
    The change is immediate, there is no need to run commit.
    """

    def get_keyword_names(self):
        return [
                'set_time_get',
                'set_time_set'
               ]

    def set_time_get(self):
        """Get current time on SMA.

        Example:
        | ${cur_time} | Set Time Get |

        Return:
            String value. Current time on SMA.
        """

        return self._cli.settime()

    def set_time_set(self, timeval, shutdown_ntp='y'):
        """Manually set the system clock.  The time entered must be in the
           timezone of the machine you are setting.

        Parameters:
           - `timeval`: time in "MM/DD/YYYY HH:MM:SS" format (including quotes).
           - `shutdown_ntp`: specify whether to shut down NTP.  Either 'y'
                             or 'n'.  Defaulted to 'y'.

        Examples:
        | Set Time Set | 01/10/2000 12:00:00 |
        | Set Time Set | 01/10/2000 12:00:00 | shutdown_ntp=n |
        """
        return self._cli.settime(timeval=timeval, shutdown_ntp=shutdown_ntp)
