#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/admin/account_settings_def/domain_mappings.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

DOMAIN_MAPPING_DOMAIN_NAMES = ('Domain Name', "//textarea[@name='domain_map']")
DOMAIN_MAPPING_MAPPED_PROFILE = ('Mapped Profile', "//select[@name='profile_for_domain']")
DOMAIN_MAPPING_MAPPED_EDIT_PROFILE = ('New Profile To Map', "//select[@name='profile_for_domain']")

class DomainMappings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_combos(new_value, DOMAIN_MAPPING_MAPPED_PROFILE,
                         DOMAIN_MAPPING_MAPPED_EDIT_PROFILE)
        self._set_edits(new_value, DOMAIN_MAPPING_DOMAIN_NAMES)
