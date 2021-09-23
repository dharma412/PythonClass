#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/admin/ldap_def/ldap_global_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

INTERFACE_COMBO = ('interface',
                   "//select[@name='interface']")
CERTIFICATE_COMBO = ('certificate',
                     "//select[@name='certificate']")


class LDAPGlobalSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_combos(new_value,
                         INTERFACE_COMBO,
                         CERTIFICATE_COMBO)

    def get(self):
        raise NotImplementedError()
