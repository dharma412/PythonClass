#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/set_time.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class SetTime(CliKeywordBase):
    """
       Provides keywords to get and set ESA time
    """

    def get_keyword_names(self):
        return ['set_time']

    def set_time(self, timeval=None, shutdown_ntp='y'):
        """
        This is used to get or set the system time.
        If timeval parameter is None, it returns the current time on ESA else
        the value of timeval is set as the ESA system time.
        The time entered must be in the timezone of the machine you are setting.
        The change is immediate, there is no need to run commit.

        *Parameters*:
        - `timeval`: time in "MM/DD/YYYY HH:MM:SS" format. Default is None.
          So by default returns the current time on ESA.
        - `shutdown_ntp`: specify whether to shut down NTP.
          Either 'yes' or 'no'. Defaulted to 'yes'.

        *Return*:
            If timeval parameter is None, returns current time on ESA
            as a string value.

        *Examples*:
        | ${cur_time}= | Set Time |
        | Set Time | 01/10/2000 12:00:00 |
        | Set Time | 01/10/2000 12:00:00 | shutdown_ntp=no |
        """
        if not timeval:
            return self._cli.settime()
        else:
            return self._cli.settime(timeval=timeval, shutdown_ntp=shutdown_ntp)
