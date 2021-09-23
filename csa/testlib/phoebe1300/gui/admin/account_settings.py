#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/admin/account_settings.py#2 $
# $DateTime: 2019/09/20 06:28:26 $
# $Author: saurgup5 $

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
from common.gui.guiexceptions import GuiValueError

from account_settings_def.account_profiles import AccountProfiles
from account_settings_def.chained_profiles import ChainedProfiles
from account_settings_def.domain_mappings import DomainMappings
from account_settings_def.remediation_settings import RemediationSettings

PAGE_PATH = ('System Administration', 'Account Settings')

# Account profile xpaths
CREATE_ACCOUNT_PROFILE_BUTTON = "//input[@value='Create Account Profile']"
ACCOUNT_PROFILE_TABLE = "//table[@class='cols']"
ACCOUNT_PROFILE_EDIT_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                                         (ACCOUNT_PROFILE_TABLE, name)
ACCOUNT_PROFILE_DELETE_LINK = lambda name: "%s//td[normalize-space()='%s']" \
                                           "/following-sibling::td[3]/img" % \
                                           (ACCOUNT_PROFILE_TABLE, name)
ACCOUNT_PROFILE_TEST_BUTTON = "xpath=//*[@id='form']/input[6]"

# Chained profile xpaths
CREATE_CHAINED_PROFILES_BUTTON = "//input[@value='Create Chained Profile..']"
CHAINED_PROFILE_TABLE = "//table[@class='cols']"
CHAINED_PROFILE_EDIT_LINK = lambda name: "%s//a[normalize-space()='%s']" % \
                                         (CHAINED_PROFILE_TABLE, name)
CHAINED_PROFILE_DELETE_LINK = lambda name: "%s//td[normalize-space()='%s']" \
                                           "/following-sibling::td[3]/img" % \
                                           (CHAINED_PROFILE_TABLE, name)

# Domain mapping xpaths
DOMAIN_MAPPING_TABLE = "//table[@class='cols']"
CREATE_DOMAIN_MAPPING_BUTTON = "//input[@value='Create Domain Mapping']"
DOMAIN_MAPPING_EDIT_LINK = lambda name: "xpath=(%s//a[normalize-space()='%s'])[2]" % \
                                        (DOMAIN_MAPPING_TABLE, name)
DOMAIN_MAPPING_DELETE_LINK = lambda name: "%s//td[contains(text(), '%s')]" \
                                          "/following-sibling::td[1]/img" % \
                                          (DOMAIN_MAPPING_TABLE, name)

# Mailbox remediation xpaths
MAILBOX_REMEDIATION_ENABLE_BUTTON = "//input[@value='Enable...']"
MAILBOX_REMEDIATION_EDIT_BUTTON = "//input[@value='Edit Settings...']"
MAILBOX_REMEDIATION_ENABLE_CHECKBOX = "//input[@id='mailbox_enabled']"


class AccountSettings(GuiCommon):
    """Keywords for Cisco Email Security Appliance ->
       System Administration -> Account Settings page
    """

    def get_keyword_names(self):
        return [
            'account_settings_account_profile_create',
            'account_settings_account_profile_edit',
            'account_settings_account_profile_delete',
            'account_settings_account_profile_test_connection',
            'account_settings_chained_profile_create',
            'account_settings_chained_profile_edit',
            'account_settings_chained_profile_delete',
            'account_settings_domain_mapping_create',
            'account_settings_domain_mapping_edit',
            'account_settings_domain_mapping_delete',
            'account_settings_mailbox_remediation_enable',
            'account_settings_mailbox_remediation_disable',
            'account_settings_mailbox_remediation_is_enabled',
            'account_settings_mailbox_remediation_edit_settings',
            'account_settings_mailbox_remediation_get_details',
        ]

    @go_to_page(PAGE_PATH)
    def account_settings_account_profile_create(self, settings={}):
        """
        Keyword to create an account profile

        Parameters:
        `settings`: A dictionary containings below keys
            Profile Name: Account profile's name
            Description: Account profile's description
            Profile Type: Account profile type. on_prem | hybrid

            Below parameters are only valid when *Profile Type* is set to hybrid.
            Client ID: Application/client id.
            Tenant ID: Tenant id.
            Thumbprint: Thumbprint.
            Certificate Private Key: Private key. PEM format.
            Designate as Primary Profile: Designate as primary account profile. Yes | No

            Below parameters are only valid when *Profile Type* is set to on_prem.
            Username: Username for authentication.
            Password: Password for authenticaiont.
            Host: Hostname or IP address of the AD host.

        Examples:
        | ${settings}= | Create Dictionary                      |
        | ... | Profile Name  | ${ON_PREM_ACCOUNT_PRIFILE}      |
        | ... | Description   | test on-prem account profile    |
        | ... | Profile Type  | on_prem                         |
        | ... | Username      | ${DUT_ADMIN}                    |
        | ... | Password      | ${DUT_ADMIN_PASSWORD}           |
        | ... | Host          | ${DUT}                          |
        | Account Settings Account Profile Create | ${settings} |

        """
        self._click_element(CREATE_ACCOUNT_PROFILE_BUTTON)
        controller = self._get_account_profile_controller()
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def account_settings_account_profile_edit(self, profile_name, settings={}):
        """
        Keyword to edit an account profile

        Parameters:
        `settings`: A dictionary containings below keys
            Description: Account profile's description
            Profile Type: Account profile type. on_prem | hybrid

            Below parameters are only valid when *Profile Type* is set to hybrid.
            Client ID: Application/client id.
            Tenant ID: Tenant id.
            Thumbprint: Thumbprint.
            Certificate Private Key: Private key. PEM format.
            Designate as Primary Profile: Designate as primary account profile. Yes | No

            Below parameters are only valid when *Profile Type* is set to on_prem.
            Username: Username for authentication.
            Password: Password for authenticaiont.
            Host: Hostname or IP address of the AD host.

        Examples:
        | ${settings}= | Create Dictionary                              |
        | ... | Description              |  edited test account profile |
        | ... | Profile Type             |  hybrid                      |
        | ... | Client ID                |  ${CLIENT_ID}                |
        | ... | Tenant ID                |  ${TENANT_ID}                |
        | ... | Thumbprint               |  ${THUMBPRINT}               |
        | ... | Certificate Private Key  |  ${PRIVATE_KEY}              |
        | Account Settings Account Profile Edit                         |
        | ... | ${ON_PREM_ACCOUNT_PRIFILE} | ${settings}                |
        """
        if self._is_element_present(ACCOUNT_PROFILE_EDIT_LINK(profile_name)):
            self._click_element(ACCOUNT_PROFILE_EDIT_LINK(profile_name))
        else:
            raise ValueError('Account profile named "%s" is not found' % profile_name)
        controller = self._get_account_profile_controller()
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def account_settings_account_profile_delete(self, profile_name):
        """
        Keyword to delete an account profile

        Parameters:
        `profile_name`: Name of the profile to be deleted.

        Examples:
        | Account Settings Account Profile Delete  | ${ON_PREM_ACCOUNT_PRIFILE} |
        """
        if self._is_element_present(ACCOUNT_PROFILE_DELETE_LINK(profile_name)):
            self._click_element(ACCOUNT_PROFILE_DELETE_LINK(profile_name), dont_wait=True)
            self._click_continue_button('Delete')
        else:
            raise ValueError('Account profile named "%s" is not found' % profile_name)

    @go_to_page(PAGE_PATH)
    def account_settings_account_profile_test_connection(self, profile_name, settings={}):
        """
        Keyword to test connection for an account profile.

        Parameters:
        `profile_name`: Name of the profile for which testing need to be done.
        `settings`: A dictionary containing below parameter(s)
            Email Address: Email address for testing.

        Examples:
        | ${settings}= | Create Dictionary | Email Address | ${DUT_ADMIN}@cisco.com |
        | ${results}=  | Account Settings Account Profile Test Connection           |
        | ... | ${HYBRID_ACCOUNT_PROFILE} | ${settings}                             |
        Log  ${results}
        """
        if self._is_element_present(ACCOUNT_PROFILE_EDIT_LINK(profile_name)):
            self._click_element(ACCOUNT_PROFILE_EDIT_LINK(profile_name))
        else:
            raise ValueError('Account profile named "%s" is not found' % profile_name)
        self.click_button(ACCOUNT_PROFILE_TEST_BUTTON, "don't wait")
        controller = self._get_account_profile_controller()
        return controller.test(settings)

    @go_to_page(PAGE_PATH)
    def account_settings_chained_profile_create(self, settings={}):
        """
        Keyword to create a chained profile

        Parameters:
        `settings`: A dictionary containings below keys
            Profile Name: Chained profile's name.
            Description: Chained profile's description.
            Mar Profiles: List of MAR profiles to be included.

        Examples:
        | ${mar_profiles}= | Create List                        |
        | ... | ${ON_PREM_ACCOUNT_PRIFILE}                      |
        | ... | ${HYBRID_ACCOUNT_PROFILE}                       |
        | ${settings}= | Create Dictionary                      |
        | ... | Profile Name  | ${CHAINED_PROFILE}              |
        | ... | Description   | test chained profile            |
        | ... | Mar Profiles  | ${mar_profiles}                 |
        | Account Settings Chained Profile Create | ${settings} |
        """
        self._click_element(CREATE_CHAINED_PROFILES_BUTTON)
        controller = self._get_chained_profile_controller()
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def account_settings_chained_profile_edit(self, profile_name, settings={}):
        """
        Keyword to edit a chained profile

        Parameters:
        `settings`: A dictionary containings below keys
            Profile Name: Chained profile's name.
            Description: Chained profile's description.
            Mar Profile Settings: A list of mar profiles settings.
              Allowed format:
                profile1:action:<profile2>

                Allowed values for action: add | alter | delete
                profile2 is mandatory only when action is set to alter

                eg:
                    1. Add a new MAR profile:
                       ${mar_profile_edit_settings}=  Create List  ${new_profile}:add:
                    2. Delete a MAR profile:
                       ${mar_profile_delete_settings}=  Create List  ${profile}:delete:
                    3. Change a MAR profile:
                       ${mar_profile_edit_settings}=  Create List  ${profile}:alter:${new_profile}
                    4. Add a new MAR profile and change & delete an existing MAR profile:
                       ${mar_profile_edit_settings}=  Create List
                       ...  ${new_profile}:add:
                       ...  ${profile1}:delete:
                       ...  ${profile2}:alter:${new_profile2}

        Examples:
        | ${mar_profile_edit_settings} | Create List |
        | ... | ${mar_profile1}:alter:${mar_profile2}                               |
        | ${settings}= | Create Dictionary                                          |
        | ... | Profile Name            | ${CHAINED_PROFILE}_edited                 |
        | ... | Description             | edited test chained profile               |
        | ... | Mar Profile Settings    | ${mar_profile_edit_settings}              |
        | Account Settings Chained Profile Edit | ${CHAINED_PROFILE} | ${settings}  |
        """
        if self._is_element_present(CHAINED_PROFILE_EDIT_LINK(profile_name)):
            self._click_element(CHAINED_PROFILE_EDIT_LINK(profile_name))
        else:
            raise ValueError('Chained profile named "%s" is not found' % profile_name)
        controller = self._get_chained_profile_controller()
        controller.edit(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def account_settings_chained_profile_delete(self, profile_name):
        """
        Keyword to delete an chained profile

        Parameters:
        `profile_name`: Name of the profile to be deleted.

        Examples:
        | Account Settings Chained Profile Delete | ${CHAINED_PROFILE} |
        """
        if self._is_element_present(CHAINED_PROFILE_DELETE_LINK(profile_name)):
            self._click_element(CHAINED_PROFILE_DELETE_LINK(profile_name), dont_wait=True)
            self._click_continue_button('Delete')
        else:
            raise ValueError('Chained profile named "%s" is not found' % profile_name)

    @go_to_page(PAGE_PATH)
    def account_settings_domain_mapping_create(self, settings={}):
        """
        Keyword to create domain mapping.

        Parameters:
        `settings`: A dictionary containings below keys
            Domain Name: Domain to name to map
            Mapped Profile: Profile name to which above domain will be mapped to.
                            Can be account or chained profile name.

        Examples:
        | ${settings}= | Create Dictionary                      |
        | ... | Domain Name     |  ${DOMAIN}                    |
        | ... | Mapped Profile  |  ${CHAINED_PROFILE}           |
        | Account Settings Domain Mapping Create | ${settings}  |
        """
        self._click_element(CREATE_DOMAIN_MAPPING_BUTTON)
        controller = self._get_domain_mapping_controller()
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def account_settings_domain_mapping_edit(self, settings={}):
        """
        Keyword to edit domain mapping.

        Parameters:
        `settings`: A dictionary containings below keys
            Domain Name: Domain to name to map
            Mapped Profile: Profile name which needs to be edited.
                            Can be account or chained profile name.
            New Profile To Map: New profile name to which above domain will be mapped to.
                                Can be account or chained profile name.

        Examples:
        | ${settings}= | Create Dictionary                    |
        | ... | Domain Name        |  ${DOMAIN}               |
        | ... | Mapped Profile     |  ${CHAINED_PROFILE}      |
        | ... | New Profile To Map |  ${NEW_CHAINED_PROFILE}  |
        | Account Settings Domain Mapping Edit | ${settings}  |
        """
        if self._is_element_present(DOMAIN_MAPPING_EDIT_LINK(settings['Mapped Profile'])):
            self._click_element(DOMAIN_MAPPING_EDIT_LINK(settings['Mapped Profile']))
        else:
            raise ValueError('Domain mapping profile named "%s" is not found' % settings['Mapped Profile'])
        controller = self._get_domain_mapping_controller()
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def account_settings_domain_mapping_delete(self, domain_name):
        """
        Keyword to delete domain mapping.

        Parameters:
        `domain_name`: Name of the domain to be deleted.

        Examples:
        | Account Settings Domain Mapping Delete | ${DOMAIN} |
        """
        if self._is_element_present(DOMAIN_MAPPING_DELETE_LINK(domain_name)):
            self._click_element(DOMAIN_MAPPING_DELETE_LINK(domain_name), dont_wait=True)
            self._click_continue_button('Delete')
        else:
            raise ValueError('Domain mapping for profile named "%s" is not found' % domain_name)

    @go_to_page(PAGE_PATH)
    def account_settings_mailbox_remediation_enable(self, settings={}):
        """
        Keyword to enable mailbox remediation.

        Parameters:
        `settings`: (Optional) A dictionary containings below keys
            Maximum number of attempts: Value between 3 to 5.
            Timeout for Hybrid Setup: Value between 30 to 60.
            Timeout for On Premise Setup: Value between 30 to 60.

        Examples:
        | Account Settings Mailbox Remediation Enable |

        | ${settings}= | Create Dictionary                          |
        | ... | Maximum number of attempts   | 4                    |
        | ... | Timeout for Hybrid Setup     | 40                   |
        | ... | Timeout for On Premise Setup | 50                   |
        | Account Settings Mailbox Remediation Enable | ${settings} |
        """
        self._click_element(MAILBOX_REMEDIATION_ENABLE_BUTTON)
        self._click_element(MAILBOX_REMEDIATION_ENABLE_CHECKBOX, type='checkbox')
        controller = self._get_remediation_settings_controller()
        controller.set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def account_settings_mailbox_remediation_disable(self):
        """
        Keyword to disable mailbox remediation.

        Parameters: None

        Examples:
        | Account Settings Mailbox Remediation Disable |
        """
        self._click_element(MAILBOX_REMEDIATION_EDIT_BUTTON)
        self._click_element(MAILBOX_REMEDIATION_ENABLE_CHECKBOX, type='checkbox', action='unselect')
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def account_settings_mailbox_remediation_is_enabled(self):
        """
        Keyword to check if mailbox remediation is enabled or not.

        Parameters: None

        Examples:
        | ${account_settings_enabled}= | Account Settings Mailbox Remediation Is Enabled |
        | Should Be True               | ${account_settings_enabled}                     |
        """
        return self._is_element_present(MAILBOX_REMEDIATION_EDIT_BUTTON)

    @go_to_page(PAGE_PATH)
    def account_settings_mailbox_remediation_get_details(self):
        """
        Keyword to get mailbox remediation settings

        Parameters: None

        Examples:
        | ${settings}= | Account Settings Mailbox Remediation Get Details                           |
        | ${maximum_attempts}=   | Get From Dictionary | ${settings}  Maximum number of attempts    |
        | ${hybrid_timeout}=     | Get From Dictionary | ${settings}  Hybrid Setup Timeout          |
        | ${onprem_timeout}=     | Get From Dictionary | ${settings}  On Premise Setup Timeout      |

        | Should Be Equal As Integers | ${maximum_attempts}   | 3          |
        | Should Be Equal As Strings  | ${hybrid_timeout}     | 30 seconds |
        | Should Be Equal As Strings  | ${onprem_timeout}     | 30 seconds |
        """
        controller = self._get_remediation_settings_controller()
        return controller.get()

    @go_to_page(PAGE_PATH)
    def account_settings_mailbox_remediation_edit_settings(self, settings={}):
        """
        Keyword to edit mailbox remediation settings.

        Parameters:
        `settings`: A dictionary containings below keys
            Maximum number of attempts: Value between 3 to 5.
            Timeout for Hybrid Setup: Value between 30 to 60.
            Timeout for On Premise Setup: Value between 30 to 60.

        Examples:
        | Account Settings Mailbox Remediation Enable |

        | ${settings}= | Create Dictionary                          |
        | ... | Maximum number of attempts   | 5                    |
        | ... | Timeout for Hybrid Setup     | 60                   |
        | ... | Timeout for On Premise Setup | 60                   |
        | Account Settings Mailbox Remediation Edit   | ${settings} |
        """
        self._click_element(MAILBOX_REMEDIATION_EDIT_BUTTON)
        controller = self._get_remediation_settings_controller()
        controller.set(settings)
        self._click_submit_button()

    # Helper methods
    def _get_account_profile_controller(self):
        if not hasattr(self, '_account_profile_controller'):
            self._account_profile_controller = AccountProfiles(self)
        return self._account_profile_controller

    def _get_chained_profile_controller(self):
        if not hasattr(self, '_chained_profile_controller'):
            self._chained_profile_controller = ChainedProfiles(self)
        return self._chained_profile_controller

    def _get_domain_mapping_controller(self):
        if not hasattr(self, '_domain_mapping_controller'):
            self._domain_mapping_controller = DomainMappings(self)
        return self._domain_mapping_controller

    def _get_remediation_settings_controller(self):
        if not hasattr(self, '_remediation_settings_controller'):
            self._remediation_settings_controller = RemediationSettings(self)
        return self._remediation_settings_controller

    def _click_element(self, locator, dont_wait=False, type='button', action='select'):
        if self._is_element_present(locator):
            if type.lower() == 'button':
                self.click_button(locator, dont_wait)
            elif type.lower() == 'checkbox':
                if action.lower() == 'select':
                    self._select_unselect_checkbox(locator, True)
                else:
                    self._select_unselect_checkbox(locator, False)
            else:
                raise GuiValueError("Unknown locator type - %s" % type)
        else:
            raise GuiValueError("Element with xpth %s not found" % locator)
