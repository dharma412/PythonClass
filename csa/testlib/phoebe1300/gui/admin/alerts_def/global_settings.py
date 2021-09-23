#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/admin/alerts_def/global_settings.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

FROM_ADDR_TO_USE_WHEN_SENDING_ALERTS_RADIO_GROUP = \
    ('From Address to Use When Sending Alerts',
     {'From address user': "//input[@id='from_address_user']",
      'From address default': "//input[@id='from_address_default']"})

FROM_ADDR_TO_USE_WHEN_SENDING_ALERTS_FROM_USER_TEXT = \
    ('From Address to Use When Sending Alerts User Text',
     "//input[@id='address_user_text']")

WAIT_BEFORE_SENDING_A_DUPLICATE_ALERTS_CHECKBOX = \
    ('Wait Before Sending a Duplicate Alert',
     "//input[@id='debounce_enable']")

INITIAL_DEBOUNCE_INTERVAL_INPUT_TEXT = \
    ('Initial Number of Seconds to Wait Before Sending a Duplicate Alert',
     "//input[@name='initial_debounce_interval']")

MAXIMUM_DEBOUNCE_INTERVAL_INPUT_TEXT = \
    ('Maximum Number of Seconds to Wait Before Sending a Duplicate Alert',
     "//input[@name='maximum_debounce_interval']")

IRONPORT_AUTOSUPPORT_ENABLE_CHECKBOX = \
    ('IronPort AutoSupport Enable',
     "//input[@id='autosupport_enable']")

IRONPORT_AUTOSUPPORT_SEND_COPY_CHECKBOX = ('IronPort AutoSupport Send Copy',
                                           "//input[@id='autosupport_all']")


class AlertsGlobalSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_radio_groups(new_value,
                               FROM_ADDR_TO_USE_WHEN_SENDING_ALERTS_RADIO_GROUP)

        self._set_checkboxes(new_value,
                             WAIT_BEFORE_SENDING_A_DUPLICATE_ALERTS_CHECKBOX,
                             IRONPORT_AUTOSUPPORT_ENABLE_CHECKBOX,
                             IRONPORT_AUTOSUPPORT_SEND_COPY_CHECKBOX)

        self._set_edits(new_value,
                        FROM_ADDR_TO_USE_WHEN_SENDING_ALERTS_FROM_USER_TEXT,
                        INITIAL_DEBOUNCE_INTERVAL_INPUT_TEXT,
                        MAXIMUM_DEBOUNCE_INTERVAL_INPUT_TEXT)

    def get(self):
        raise NotImplementedError()
