#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/options/slbl_admin_def/recipient_settings.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

RECIPIENT_ADDRESS = ('Address',
                     "//input[@id='address']")
SENDER_LIST = ('Sender List',
               "//textarea[@id='address_list']")


# RECIPIENT_ADDRESS = ('Address',
#                     "//input[contains(@name,'recipient_text')]")
# SENDER_LIST = ('Sender List',
#               "//input[contains(@name,'search_terms')]")

class RecipientSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(1, 'gui')
    def set(self, new_value):
        self._set_edits(new_value,
                        RECIPIENT_ADDRESS,
                        SENDER_LIST)

    @set_speed(1, 'gui')
    def get(self):
        return self._get_values(RECIPIENT_ADDRESS,
                                SENDER_LIST)
