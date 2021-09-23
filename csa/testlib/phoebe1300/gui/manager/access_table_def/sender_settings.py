#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/manager/access_table_def/sender_settings.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

SENDER_TYPE_IP_ADDRESS = "//input[@id='sender_type_ip']"
SENDER = ('sender',
          "//input[@name='sender']")
COMMENT = ('comment',
           "//input[@name='comment']")


class SenderSettings(InputsOwner):

    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        if self._listener.lower() == 'inboundmail' and self._method == 'add':
            self.gui._click_radio_button(SENDER_TYPE_IP_ADDRESS)
        self._set_edits(new_value,
                        SENDER,
                        COMMENT)

    @set_speed(0, 'gui')
    def get(self):
        return self._get_values(SENDER,
                                COMMENT)
