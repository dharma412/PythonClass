#!/usr/bin/env python -tt
#$Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/manager/address_lists_def/address_list_settings.py#1 $
#$DateTime: 2020/01/06 01:25:43 $
#$Author: saurgup5 $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

NAME = ('Name',
        "//input[@name='name']")
DESCRIPTION = ('Description',
               "//textarea[@name='description']")
ADDRESES = ('Addresses',
            "//textarea[@name='addresses']")
ADDR_LIST_SELECT_GROUP = ('List Type',
                          {'Full Email Addresses only':"//*[@id='list_type_email']",
                           'Domains only':"//*[@id='list_type_domain']",
                           'IP Addresses only':"//*[@id='list_type_ip']",
                           'All of the above':"//*[@id='list_type_any']"})


class AddressListSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_radio_groups(new_value,
                               ADDR_LIST_SELECT_GROUP)

        self._set_edits(new_value,
                        NAME,
                        DESCRIPTION,
                        ADDRESES)

    @set_speed(0, 'gui')
    def get(self):
        raise NotImplementedError()
