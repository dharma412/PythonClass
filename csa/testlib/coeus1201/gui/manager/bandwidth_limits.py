#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/bandwidth_limits.py#1 $

import re
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

BAND_LIMIT_ON = 'bandwidth_limit_yes'
BAND_LIMIT_OFF = 'bandwidth_limit_no'
DEFAULT_UNIT = 'kbps'


class BandwidthLimits(GuiCommon):
    """Overall Bandwidth Limits settings page interaction class.

    This class designed to interact with GUI elements of
    'Web Security Manager' -> 'Overall Bandwidth Limit' page.
    """

    def get_keyword_names(self):
        return ['bandwidth_limits_edit',]

    def _open_page(self):
        self._navigate_to('Web Security Manager', 'Overall Bandwidth Limits')

    def _fill_bandwidth_limit(self, limit):
        band_limit_loc = 'name=bandwidth_limit'
        self.input_text(band_limit_loc, limit)

    def _toggle_bandwidth_limit(self, bandwidth_limit=None):

        if bandwidth_limit is not None:
            if bandwidth_limit.lower() != 'off':
                self._click_radio_button(BAND_LIMIT_ON)
            else:
                self._click_radio_button(BAND_LIMIT_OFF)

    def _select_bandwidth_limit_unit(self, limit_unit=None):

        units = {'kbps': 'kbps', 'mbps': 'Mbps'}
        limit_unit_select = 'bandwidth_limit_unit'
        if limit_unit:
            limit_unit_option = "label=%s" % (limit_unit,)
            self.select_from_list(limit_unit_select,
                                   units[limit_unit.lower()])

    def bandwidth_limits_edit(self, limit=None):
        """Edit Overall Bandwidth Limits.

        Parameters:
        - `limit`: bandwidth limit. String with limit and unit values
                   separated with whitespace. Valid range is from
                   1 kbps to 512 Mbps. Default unit is 'kbps'.
                   'Off' string to disable limits.

        Example:
        | Bandwidth Limits Edit | limit=10 kbps |
        | Bandwidth Limits Edit | limit=10 mbps |
        | Bandwidth Limits Edit | limit=100 | #default unit is kbps |
        | Bandwidth Limits Edit | limit=off | #off to disable limits |
        """
        if limit is not None:
            self._open_page()
            self._click_edit_settings_button()
            self._toggle_bandwidth_limit(limit.strip())

            if limit.lower() != 'off':
                if len(limit.split()) == 1:
                    limit_value, limit_unit = limit.split()[0], DEFAULT_UNIT
                elif len(limit.split()) == 2:
                    limit_value, limit_unit = limit.split()
                else:
                    raise ValueError("Limit should be a string with space"\
                                     "separated limit value and unit")
                self._fill_bandwidth_limit(limit_value)
                self._select_bandwidth_limit_unit(limit_unit)
            self._click_submit_button(wait=False)
