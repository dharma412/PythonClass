#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/admin/ldap_def/ldap_global_settings.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs


INTERFACE_COMBO = ('interface',
                   "//select[@name='interface']")
CERTIFICATE_COMBO = ('certificate',
                     "//select[@name='certificate']")

VALIDATE_LDAP_CERTIFICATE_RADIO_GROUP = ('Validate LDAP Server Certificate',
                      {'Yes': "//input[@id='ldap_certificate_verify_yes']",
                       'No': "//input[@id='ldap_certificate_verify_no']"})

class LDAPGlobalSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_combos(new_value,
                         INTERFACE_COMBO,
                         CERTIFICATE_COMBO)
        self._set_radio_groups(
                        new_value,
                        VALIDATE_LDAP_CERTIFICATE_RADIO_GROUP)

    def get(self):
        raise NotImplementedError()


