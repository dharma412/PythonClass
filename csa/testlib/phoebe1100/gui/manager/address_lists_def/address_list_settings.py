#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/manager/address_lists_def/address_list_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

NAME = ('Name',
        "//input[@name='name']")
DESCRIPTION = ('Description',
               "//textarea[@name='description']")
ADDRESES = ('Addresses',
            "//textarea[@name='addresses']")
ALLOW_FULL_EMAIL_CHECKBOX = ('Allow only full Email Addresses',
                             "//input[@id='is_email_type']")


class AddressListSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_checkboxes(new_value,
                             ALLOW_FULL_EMAIL_CHECKBOX)
        self._set_edits(new_value,
                        NAME,
                        DESCRIPTION,
                        ADDRESES)

    @set_speed(0, 'gui')
    def get(self):
        raise NotImplementedError()
