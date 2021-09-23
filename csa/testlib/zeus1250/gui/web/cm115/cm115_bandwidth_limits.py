#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/cm115/cm115_bandwidth_limits.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from coeus1100.gui.manager.bandwidth_limits import BandwidthLimits

class Cm110BandwidthLimits(BandwidthLimits):

    """
    Keywords library for WebUI page Web -> Configuration Master 11.5 -> Overall Bandwidth Limits
    """

    def _open_page(self):
        self._navigate_to('Web', 'Configuration Master 11.5', 'Overall Bandwidth Limits')

    def get_keyword_names(self):
         return ['cm115_bandwidth_limits_edit',
             ]

    def cm115_bandwidth_limits_edit(self, limit=None):
        """Edit Overall Bandwidth Limits from Configuration Master 11.5

        *Parameters*
        - `limit`: bandwidth limit. String with limit and unit values
                    separated with whitespace. Valid range is from
                   1 kbps to 512 Mbps. Default unit is 'kbps'.
                   'Off' string to disable limits.

        *Exceptions*
        - ValueError:Limit should be a string with space separated limit value and unit

        *Examples*
        | CM115 Bandwidth Limits Edit | limit=10 kbps |
        | CM115 Bandwidth Limits Edit | limit=10 mbps |
        | CM115 Bandwidth Limits Edit | limit=100 | #default unit is kbps |
        | CM115 Bandwidth Limits Edit | limit=off | #off to disable limits |
        """
        self.bandwidth_limits_edit(limit=limit)
