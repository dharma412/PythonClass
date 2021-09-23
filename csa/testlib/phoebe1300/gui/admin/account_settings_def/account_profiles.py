#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/admin/account_settings_def/account_profiles.py#1 $
# $DateTime: 2019/09/12 22:09:21 $
# $Author: saurgup5 $

from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

PROFILE_NAME = ('Profile Name', "//input[@id='profile_name']")
DESCRIPTION = ('Description', "//textarea[@id='profile_desc']")
PROFILE_TYPE = ('Profile Type', "//select[@id='profile_type']")
CLIENT_ID = ('Client ID', "//input[@id='client_id']")
TENANT_ID = ('Tenant ID', "//input[@id='tenant_id']")
THUMBPRINT = ('Thumbprint', "//input[@id='thumbprint']")
CERTIFICATE_PRIVATE_KEY = ('Certificate Private Key',
                           "//input[@id='mar_certificate_pair']")
DESIGNATE_AS_PRIMARY_PROFILE = ('Designate as Primary Profile',
                                {'Yes': "//input[@id='primary_profile_yes']",
                                 'No': "//input[@id='primary_profile_no']"})
USERNAME = ('Username', "//input[@id='username']")
PASSWORD = ('Password', "//input[@id='password']")
HOST = ('Host', "//input[@id='host']")

ACCOUNT_PROFILE_TEST_EMAIL_ADDRESS = ('Email Address', "//input[@id='mail_id']")
ACCOUNT_PROFILE_TEST_RESULTS = "//div[@id='test_results']"
ACCOUNT_PROFILE_TEST_CONNECTION_BUTTON = "//input[@value='Test Connection']"
ACCOUNT_PROFILE_TEST_DONE_BUTTON = "//button[@id='yui-gen23-button']"


class AccountProfiles(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def set(self, new_value):
        self._set_combos(new_value, PROFILE_TYPE)
        self._set_edits(new_value,
                        PROFILE_NAME,
                        DESCRIPTION,
                        CLIENT_ID,
                        TENANT_ID,
                        THUMBPRINT,
                        CERTIFICATE_PRIVATE_KEY,
                        USERNAME,
                        PASSWORD,
                        HOST)
        self._set_radio_groups(
            new_value,
            DESIGNATE_AS_PRIMARY_PROFILE)

    def test(self, new_value):
        self._set_edits(new_value, ACCOUNT_PROFILE_TEST_EMAIL_ADDRESS)
        self.gui.click_button(ACCOUNT_PROFILE_TEST_CONNECTION_BUTTON, "don't wait")
        self.gui._wait_for_text(ACCOUNT_PROFILE_TEST_RESULTS, 'Connection')
        results = self.gui._get_text(ACCOUNT_PROFILE_TEST_RESULTS)
        self.gui.click_button(ACCOUNT_PROFILE_TEST_DONE_BUTTON, "don't wait")
        return results
