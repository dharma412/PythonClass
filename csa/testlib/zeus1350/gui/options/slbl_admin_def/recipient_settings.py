# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/options/slbl_admin_def/recipient_settings.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

RECIPIENT_ADDRESS = ('Address',
                     "//input[@name='address']")
SENDER_LIST = ('Sender List',
               "//textarea[@id='address_list']")


class RecipientSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_edits(new_value,
                        RECIPIENT_ADDRESS,
                        SENDER_LIST)

    @set_speed(0, 'gui')
    def get(self):
        return self._get_values(RECIPIENT_ADDRESS,
                                SENDER_LIST)
