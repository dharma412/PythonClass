#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/manager/dmarc_def/dmarc_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import re

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

BYPASS_ADDRESS_COMBO = ('Specific senders bypass address list',
                        "//select[@id='bypass_address_list']")
BYPASS_HEADERS = ('Bypass verification for messages with headers',
                  "//input[@id='bypass_headers']")

REPORT_SCHEDULE = ('Schedule for report generation', None)
HOURS_COMBO = "//select[@name='time_picker_hours']"
MINUTES_COMBO = "//select[@name='time_picker_minutes']"
PERIOD_COMBO = "//select[@name='time_picker_period']"
SHCEDULE_STR_PATTERN = r'(?P<hours>[0-9]{1,2})\s*:\s*(?P<minutes>[0-9]{1,2})' \
                       '\s+(?P<period>[a-zA-Z]{2})'

REPORT_ENTITY = ('Entity generating reports',
                 "//input[@name='report_entity']")
REPORT_CONTACTS = ('Additional contact information',
                   "//input[@name='report_contacts']")
COPY_REPORTS = ('Send copy of all aggregate reports to',
                "//input[@name='copy_reports']")
ERROR_REPORTS_CHECKBOX = ('Send delivery error reports',
                          "//input[@name='error_reports']")


class DMARCSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def _set_schedule(self, schedule_str):
        match = re.search(SHCEDULE_STR_PATTERN, schedule_str)
        if not match:
            raise ValueError('Incorrect schedule string format "{0}". Acceptable ' \
                             'format is "HH:MM AM/PM"'.format(schedule_str))
        map(lambda x: self.gui.select_from_list(x[0], x[1]),
            [(HOURS_COMBO, '{0:02d}'.format(int(match.group('hours')))),
             (MINUTES_COMBO, '{0:02d}'.format(int(match.group('minutes')))),
             (PERIOD_COMBO, '{0}'.format(match.group('period').upper()))])

    def _get_schedule(self):
        values = map(self.gui.get_value, (HOURS_COMBO, MINUTES_COMBO, PERIOD_COMBO))
        return '{0}:{1} {2}'.format(*values).upper()

    def set(self, new_value):
        if not self.gui._is_text_present('No address lists are currently defined'):
            self._set_combos(new_value,
                             BYPASS_ADDRESS_COMBO)
        self._set_edits(new_value,
                        BYPASS_HEADERS,
                        REPORT_ENTITY,
                        REPORT_CONTACTS,
                        COPY_REPORTS)
        self._set_checkboxes(new_value,
                             ERROR_REPORTS_CHECKBOX)
        if REPORT_SCHEDULE[0] in new_value:
            self._set_schedule(new_value[REPORT_SCHEDULE[0]])

    def get(self):
        result = self._get_checkboxes(ERROR_REPORTS_CHECKBOX)
        result.update(self._get_values(BYPASS_ADDRESS_COMBO,
                                       BYPASS_HEADERS,
                                       REPORT_ENTITY,
                                       REPORT_CONTACTS,
                                       COPY_REPORTS))
        result[REPORT_SCHEDULE[0]] = self._get_schedule()
        return result
