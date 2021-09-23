#!/usr/bin/env python -tt
#$Id: //prod/main/sarf_centos/testlib/zeus1360/gui/management/administration/smart_license_def/smart_license_settings.py#1 $
#$DateTime: 2020/03/05 19:45:32 $
#$Author: sarukakk $

from common.gui.decorators import go_to_page, set_speed
from common.util.ordered_dict import OrderedDict
from common.gui.inputs_owner import InputsOwner

ROW_MAPPING = OrderedDict(
   [('Mail Handling', 'imh'),
   ('Content Security Management Config Manager', 'iccm_processing'),
   ('Content Security Management Web Reporting', 'c_web_rep_processing'),
   ('Content Security Management Master ISQ', 'master_isq'),
   ('Content Security Management Centralized Tracking', 'c_track_processing'),
   ('Content Security Management Centralized Reporting', 'c_rep_processing'),
   ])

CHECKBOX_MAPPING = OrderedDict()
for row_name_expanded, row_name_short in ROW_MAPPING.iteritems():
        CHECKBOX_MAPPING[row_name_expanded] = "//input[@id='%s']" % (row_name_short)

class SmartLicenseSettings(InputsOwner):
    def _get_registered_inputs(self):
        return CHECKBOX_MAPPING.items()

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_checkboxes(new_value, *CHECKBOX_MAPPING.items())
