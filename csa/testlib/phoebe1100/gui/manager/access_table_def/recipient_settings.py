#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/manager/access_table_def/recipient_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

ADDRESS = ('address',
           "//input[@id='rat_address']")
ACTION_COMBO = ('action',
                "//select[@id='rat_action']")
ORDER = ('order',
         "//input[@name='order']")
BYPASS_LDAP_ACCEPT_CHECKBOX = ('bypass_ldap_accept',
                               "//input[@id='bypass_ldap_accept']")
CUS_SMTP_RESP = lambda response: "//input[@id='smtp_response_%s']" % (response,)
SMTP_RESPONSE_RADIOGROUP = ('smtp_response',
                            {True: CUS_SMTP_RESP('yes'),
                             False: CUS_SMTP_RESP('no')})
SMTP_RESPONSE_CODE = ('smtp_response_code',
                      "//input[@id='smtp_response_code']")
SMTP_RESPONSE_TEXT = ('smtp_response_text',
                      "//textarea[@name='smtp_response_text']")
BYPASS_RECV_CONTROL = lambda x: "//input[@id='bypass%s']" % (x,)
BYPASS_RECV_CONTROL_RADIOGROUP = ('bypass',
                                  {True: BYPASS_RECV_CONTROL('1'),
                                   False: BYPASS_RECV_CONTROL('0')})
ALL_ADDRESS = "//table[@class='pairs']//tr" \
              "[.//th[starts-with(text(), 'Recipient Address:')]]/td"
ALL_ORDER = "//table[@class='pairs']//tr[.//th[normalize-space()='Order:']]/td"


class RecipientSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_radio_groups(new_value,
                               SMTP_RESPONSE_RADIOGROUP,
                               BYPASS_RECV_CONTROL_RADIOGROUP)
        self._set_edits(new_value,
                        ORDER,
                        ADDRESS,
                        SMTP_RESPONSE_CODE,
                        SMTP_RESPONSE_TEXT)
        self._set_combos(new_value, ACTION_COMBO)
        self._set_checkboxes(new_value,
                             BYPASS_LDAP_ACCEPT_CHECKBOX)

    @set_speed(0, 'gui')
    def get(self):
        result = self._get_values(SMTP_RESPONSE_CODE,
                                  SMTP_RESPONSE_TEXT,
                                  BYPASS_LDAP_ACCEPT_CHECKBOX)
        if self.gui._is_element_present(ADDRESS[1]):
            result[ADDRESS[0]] = self.gui.get_value(ADDRESS[1])
        else:
            result[ADDRESS[0]] = self.gui.get_text(ALL_ADDRESS)
        if self.gui._is_element_present(ORDER[1]):
            result[ORDER[0]] = self.gui.get_value(ORDER[1])
        else:
            result[ORDER[0]] = self.gui.get_text(ALL_ORDER)
        result[BYPASS_RECV_CONTROL_RADIOGROUP[0]] = \
            self.gui._is_checked(BYPASS_RECV_CONTROL('1'))
        result[SMTP_RESPONSE_RADIOGROUP[0]] = \
            self.gui._is_checked(CUS_SMTP_RESP('yes'))
        return result
