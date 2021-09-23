#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/admin/log_subscriptions_def/subscriptions_global_settings.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

SYSTEM_METRICS_FREQUENCY = ('System Metrics Frequency',
                            "//input[@name='system_measurements_frequency']")
MSG_ID_HEADERS_IN_MAIL_LOGS_CHECKBOX = ('Message-ID Headers in Mail Logs',
                                        "//input[@id='log_message_id']")
ORIGINAL_SUBJ_HEADER_OF_MSG_CHECKBOX = ('Original Subject Header of Each Message',
                                        "//input[@id='log_orig_subj']")
REMOTE_RESPONSE_TEXT_CHECKBOX = ('Remote Response Text in Mail Logs',
                                 "//input[@id='log_remote_response']")
HEADERS = ('List of Headers to Record in the Log Files',
           "//textarea[@name='customer_headers']")


class SubscriptionsGlobalSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_edits(new_value,
                        SYSTEM_METRICS_FREQUENCY,
                        HEADERS)
        self._set_checkboxes(new_value,
                             MSG_ID_HEADERS_IN_MAIL_LOGS_CHECKBOX,
                             ORIGINAL_SUBJ_HEADER_OF_MSG_CHECKBOX,
                             REMOTE_RESPONSE_TEXT_CHECKBOX)

    def get(self):
        raise NotImplementedError()
