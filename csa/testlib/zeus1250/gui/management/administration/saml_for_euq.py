#!/usr/bin/env python

# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/management/administration/saml_for_euq.py#3 $
# $DateTime: 2019/06/07 02:45:52 $
# $Author: sarukakk $


from common.gui.guicommon import GuiCommon

IDP_EDIT_SETTINGS_BUTTON = 'xpath='
SP_EDIT_SETTINGS_BUTTON = 'xpath='


class SamlForEUQ(GuiCommon):

    """Keywords for Management Appliance -> System Administration -> SAML for EUQ"""

    def get_keyword_names(self):
        return [
            'saml_edit_ipd_settings',
            'saml_edit_sp_settings',
            'saml_get_idp_settings',
            'saml_get_sp_settings'
            ]

    def _open_page(self):
        self._navigate_to('Management', 'System Administration', 'SAML for EUQ')


    def saml_edit_ipd_settings(self, idp_name, ipd_entity_id, idl_url):
        """Edit Identity Provider Settings.

        Parameters:
        - `idp_name`:
        - `ipd_entity_id` :
        - `idl_url`:


        Examples:
        |  |  |

        """
        self._open_page()

        self.click_button(IDP_EDIT_SETTINGS_BUTTON)

        self._fill_ipd_attributes(idp_name, ipd_entity_id, idl_url)

        self._click_submit_button()

    def saml_edit_sp_settings(self, sp_entity_id, sp_assertion_url, sp_ipd_in_use,
            sp_cert, sp_organization, sp_contact):
        """Edit Service Provider Settings.

        Parameters:
        - `sp_entity_id`:
        - `sp_assertion_url`:
        - `sp_ipd_in_use`:
        - `sp_cert`:
        - `sp_organization`:
        - `sp_contact`:

        Examples:
        |   |   |
        """
        self._open_page()

        self.click_button(SP_EDIT_SETTINGS_BUTTON)

        self._fill_sd_attributes(idp_name, ipd_entity_id, idl_url)

        self._click_submit_button()

    def saml_get_idp_settings(self):
        self._open_page()

        pass

    def saml_get_sp_settings(self):
        self._open_page()

        pass
