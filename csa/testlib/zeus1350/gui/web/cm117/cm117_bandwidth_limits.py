#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/cm117/cm117_bandwidth_limits.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from coeus1170.gui.manager.bandwidth_limits import BandwidthLimits


class Cm110BandwidthLimits(BandwidthLimits):
    """
    Keywords library for WebUI page Web -> Configuration Master 11.7 -> Overall Bandwidth Limits
    """

    def _open_page(self):
        self._navigate_to('Web', 'Configuration Master 11.7', 'Overall Bandwidth Limits')

    def get_keyword_names(self):
        return ['cm117_bandwidth_limits_edit',
                ]

    def cm117_bandwidth_limits_edit(self, limit=None):
        """Edit Overall Bandwidth Limits from Configuration Master 11.7

        *Parameters*
        - `limit`: bandwidth limit. String with limit and unit values
                    separated with whitespace. Valid range is from
                   1 kbps to 512 Mbps. Default unit is 'kbps'.
                   'Off' string to disable limits.

        *Exceptions*
        - ValueError:Limit should be a string with space separated limit value and unit

        *Examples*
        | CM117 Bandwidth Limits Edit | limit=10 kbps |
        | CM117 Bandwidth Limits Edit | limit=10 mbps |
        | CM117 Bandwidth Limits Edit | limit=100 | #default unit is kbps |
        | CM117 Bandwidth Limits Edit | limit=off | #off to disable limits |
        """
        self.bandwidth_limits_edit(limit=limit)
