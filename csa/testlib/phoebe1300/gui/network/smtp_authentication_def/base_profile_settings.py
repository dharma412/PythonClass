#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/network/smtp_authentication_def/base_profile_settings.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.gui.inputs_owner import InputsOwner, get_object_inputs_pairs

NEXT_BUTTON = "//input[@name='action:Next']"
FINISH_BUTTON = NEXT_BUTTON


class BaseProfileAddSettings(InputsOwner):
    NAME = ('Name', "//input[@name='profile_id']")
    TYPE_RADIO_GROUP = ('Type',
                        {'forward': "//input[@id='profile_fwd']",
                         'outgoing': "//input[@id='profile_out']",
                         'ldap': "//input[@id='profile_ldap']",
                         'certificate': "//input[@id='profile_cert']"})

    def _get_registered_inputs(self):
        return get_object_inputs_pairs(self)

    def set(self, new_value):
        self._set_edits(new_value,
                        self.NAME)
        self._set_radio_groups(new_value,
                               self.TYPE_RADIO_GROUP)

        self.gui.click_button(NEXT_BUTTON)

    def finish(self):
        self.gui.click_button(FINISH_BUTTON)
        self.gui._check_action_result()
