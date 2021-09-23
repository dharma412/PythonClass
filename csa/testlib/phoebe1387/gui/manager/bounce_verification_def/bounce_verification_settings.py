#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/bounce_verification_def/bounce_verification_settings.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs


INVALID_MSG_ACTION_RADIO_GROUP = ('Action when invalid bounce message received',
        {'Reject': "//input[@id='bad_bounce_action_id']",
         'Add custom header and deliver': "//input[@id='tag_action_id']"})
HEADER_NAME = ('Header Name',
               "//input[@id='header_name_id']")
HEADER_CONTENT = ('Header Content',
                  "//input[@id='header_value_id']")
SMART_EXCEPTIONS_CHECKBOX = ('Smart Exceptions to tagging',
                             "//input[@id='inbound_outbound_heuristics']")


class BVSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_radio_groups(new_value,
                               INVALID_MSG_ACTION_RADIO_GROUP)
        self._set_edits(new_value,
                        HEADER_NAME,
                        HEADER_CONTENT)
        self._set_checkboxes(new_value,
                             SMART_EXCEPTIONS_CHECKBOX)

    @set_speed(0, 'gui')
    def get(self):
        result = {}
        result.update(self._get_radio_groups(INVALID_MSG_ACTION_RADIO_GROUP))
        result.update(self._get_checkboxes(SMART_EXCEPTIONS_CHECKBOX))
        if self.gui._is_checked(\
           INVALID_MSG_ACTION_RADIO_GROUP[1]['Add custom header and deliver']):
            result.update(self._get_values(HEADER_NAME, HEADER_CONTENT))
        return result
