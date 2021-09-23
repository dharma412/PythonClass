#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/management/administration/users_def/extauth_devops_settings.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

AUTH_TYPE_COMBO = ('Authentication Type',
                   "//select[@id='ext_auth']")
GROUP_MAPPING = ('Group Mapping', {})
GROUP_MAPPING_ADD_BUTTON = "//input[@id='ldap_groups_mapping_domtable_AddRow']"
GROUP_MAPPING_CONTAINER = "//tbody[@id='ldap_groups_mapping_rowContainer']"
# indexes starts from 1
GROUP_MAPPING_EXT_GROUP_NAME = lambda index: \
    "%s/tr[%d]//input[contains(@id, '[group_name]')]" % (GROUP_MAPPING_CONTAINER,
                                                         index)
GROUP_MAPPING_LOCAL_GROUP_NAME_COMBO = lambda index: \
    "%s/tr[%d]//select[contains(@id, '[role]')]" % (GROUP_MAPPING_CONTAINER,
                                                    index)
GROUP_MAPPING_DELETE_BUTTON = lambda index: \
    "%s/tr[%d]//img[@title='Delete...']" % (GROUP_MAPPING_CONTAINER, index)

# SAML
SAML_EXT_AUTH_ATTRIBUTE_MAP = ('External Authentication Attribute Name Map',
                               "//textarea[@id='extauth_group_attribute']")
CUSTOMIZE_STRING_DEVOPS = ('Customize Strings to View Devops SSO Login',
                           "//textarea[@id='sso_toggle_string']")


class ExtAuthDevopsSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, settings):
        self._set_edits(settings, SAML_EXT_AUTH_ATTRIBUTE_MAP, CUSTOMIZE_STRING_DEVOPS)
        self._set_group_mapping(settings)

    def _set_group_mapping(self, settings):
        if settings.has_key(GROUP_MAPPING[0]):
            # clear list
            while self.gui._is_element_present(GROUP_MAPPING_DELETE_BUTTON(2)):
                self.gui.click_button(GROUP_MAPPING_DELETE_BUTTON(2), 'don\'t wait')
            pairs_to_set = settings[GROUP_MAPPING[0]]
            for index, pair in zip(range(1, len(pairs_to_set) + 1), pairs_to_set.items()):
                if index > 1:
                    self.gui.click_button(GROUP_MAPPING_ADD_BUTTON, 'don\'t wait')
                ext_group, local_group = pair
                self.gui.input_text(GROUP_MAPPING_EXT_GROUP_NAME(index), ext_group)
                self.gui.select_from_list(GROUP_MAPPING_LOCAL_GROUP_NAME_COMBO(index),
                                          local_group)

    def get(self):
        raise NotImplementedError()
