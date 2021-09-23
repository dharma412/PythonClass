#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/admin/users_def/dlp_tracking_priv_settings.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner

PARENT_TABLE = "//table[@class='cols']"
CHECKBOX_XPATH = lambda row: \
    "xpath=//table[@class='cols']/tbody/tr[%s]/td[2]/input" % (row,)

class DlpTrackingPrivSettings(InputsOwner):
    @set_speed(0, 'gui')
    def _get_checkbox_xpaths(self):
        xpaths = {}
        rows = int(self.gui.get_matching_xpath_count('%s//tr' % (PARENT_TABLE,)))
        cols = int(self.gui.get_matching_xpath_count('%s//th' % (PARENT_TABLE,)))

        for row in xrange(0, rows):
            for col in xrange(0, cols):
                try:
                    read_name = self.gui._get_table_cell("xpath=%s.%s.%s"%(PARENT_TABLE, row, col))
                    if read_name.lower() == 'custom roles' or \
                        read_name.lower() == 'user roles' or \
                        read_name.lower() == 'predefined':
                        break
                    xpaths[read_name] = CHECKBOX_XPATH(row+1,)
                except Exception as e:
                    print e
                    continue
        return xpaths

    def _get_registered_inputs(self):
        return self._get_checkbox_xpaths().items()

    @set_speed(0, 'gui')
    def set(self, settings):
        xpaths = self._get_checkbox_xpaths()
        for idx in xpaths.keys():
            if settings.has_key(idx):
                if settings[idx] is True:
                    self.gui.select_checkbox(xpaths[idx])
                else:
                    self.gui.unselect_checkbox(xpaths[idx])
