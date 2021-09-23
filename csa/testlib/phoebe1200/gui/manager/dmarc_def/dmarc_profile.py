#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/manager/dmarc_def/dmarc_profile.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

PROFILE_NAME = ('Profile Name',
                "//input[@id='profile_name']")
REJECT_ACTION_RADIOGROUP = ('Message action when DMARC policy is reject',
                            {'No Action': "//input[@id='reject_action_none']",
                             'Quarantine': "//input[@id='reject_action_quarantine']",
                             'Reject': "//input[@id='reject_action_reject']"})
REJECT_QUARANTINE_TO_COMBO = ('Reject Policy Quarantine Name',
                              "//select[@id='reject_quarantine_to']")
REJECT_SMTP_CODE = ('Reject SMTP Code',
                    "//input[@id='reject_smtp_code']")
REJECT_SMTP_RESPONSE = ('Reject SMTP Response',
                        "//input[@id='reject_smtp_response']")
QUARANTINE_ACTION_RADIOGROUP = ('Message action when DMARC policy is quarantine',
                                {'No Action': "//input[@id='quarantine_action_none']",
                                 'Quarantine': "//input[@id='reject_action_quarantine']"})
QUARANTINE_QUARANTINE_TO_COMBO = ('Quarantine Policy Quarantine Name',
                                  "//select[@id='quarantine_quarantine_to']")
TEMP_FAILURE_MESSAGE_ACTION_RADIOGROUP = \
    ('Message action in case of temporary failure',
     {'Accept': "//input[@id='temp_failure_action_accept']",
      'Reject': "//input[@id='temp_failure_action_reject']"})
TEMP_FAILURE_REJECT_SMTP_CODE = ('Temporary Failure SMTP Code',
                                 "//input[@id='temp_failure_reject_smtp_code']")
TEMP_FAILURE_REJECT_SMTP_RESPONSE = \
    ('Temporary Failure SMTP Response',
     "//input[@id='temp_failure_reject_smtp_response']")
PERM_FAILURE_MESSAGE_ACTION_RADIOGROUP = \
    ('Message action in case of permanent failure',
     {'Accept': "//input[@id='perm_failure_action_accept']",
      'Reject': "//input[@id='perm_failure_action_reject']"})
PERM_FAILURE_REJECT_SMTP_CODE = ('Permanent Failure SMTP Code',
                                 "//input[@id='perm_failure_reject_smtp_code']")
PERM_FAILURE_REJECT_SMTP_RESPONSE = ('Permanent Failure SMTP Response',
                                     "//input[@id='perm_failure_reject_smtp_response']")


class DMARCProfile(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_radio_groups(new_value,
                               REJECT_ACTION_RADIOGROUP,
                               QUARANTINE_ACTION_RADIOGROUP,
                               TEMP_FAILURE_MESSAGE_ACTION_RADIOGROUP,
                               PERM_FAILURE_MESSAGE_ACTION_RADIOGROUP)
        self._set_combos(new_value,
                         REJECT_QUARANTINE_TO_COMBO,
                         QUARANTINE_QUARANTINE_TO_COMBO)
        self._set_edits(new_value,
                        PROFILE_NAME,
                        REJECT_SMTP_CODE,
                        REJECT_SMTP_RESPONSE,
                        TEMP_FAILURE_REJECT_SMTP_CODE,
                        TEMP_FAILURE_REJECT_SMTP_RESPONSE,
                        PERM_FAILURE_REJECT_SMTP_CODE,
                        PERM_FAILURE_REJECT_SMTP_RESPONSE)
