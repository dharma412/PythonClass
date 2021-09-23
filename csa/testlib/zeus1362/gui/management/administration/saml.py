# $Id: //prod/main/sarf_centos/testlib/zeus1362/gui/management/administration/saml.py#1 $
# $DateTime: 2020/06/10 22:29:20 $
# $Author: sarukakk $

import time
import copy
import common.gui.guiexceptions as guiexceptions
from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon
from common.util.sarftime import CountDownTimer
from saml_def.sp_idp_settings import IdentityProviderSettings, ServiceProviderSettings

PAGE_PATH = ('Management','System Administration', 'SAML')
CUSTOMER_SP_ADD_BUTTON = "//input[@id='user_add' and @value='Add Service Provider...']"
CUSTOMER_IDP_ADD_BUTTON = "//input[@id='user_add' and @value='Add Identity Provider...']"
CUSTOMER_TABLE = '//table[@id="user_profile"]'
CUSTOMER_EDIT_LINK = lambda name: "%s//a[normalize-space()='%s']" % (CUSTOMER_TABLE, name)
CUSTOMER_DELETE_BUTTON = lambda name: "%s//td[.//a[normalize-space()='%s']]" \
                        "/following-sibling::td/img[@title='Delete...']" % (CUSTOMER_TABLE, name)
CUSTOMER_IDP_VIEW_METADATA_BUTTON = '//input[@id="user_idp_metadata"]'
CUSTOMER_DOWNLOAD_SP_METADATA = '//input[@id="user_export_sp_metadata"]'
#DevOps xpath variables
DEVOPS_SP_ADD_BUTTON = "//input[@id='devops_add' and @value='Add Service Provider...']"
DEVOPS_IDP_ADD_BUTTON = "//input[@id='devops_add' and @value='Add Identity Provider...']"
DEVOPS_TABLE = '//table[@id="devops_profile"]'
DEVOPS_EDIT_LINK = lambda name: "%s//a[normalize-space()='%s']" % (DEVOPS_TABLE, name)
DEVOPS_DELETE_BUTTON = lambda name: "%s//td[.//a[normalize-space()='%s']]" \
                        "/following-sibling::td/img[@title='Delete...']" % (DEVOPS_TABLE, name)
DEVOPS_IDP_VIEW_METADATA_BUTTON = '//input[@id="devops_idp_metadata"]'
DEVOPS_DOWNLOAD_SP_METADATA = '//input[@id="devops_export_sp_metadata"]'

#EUQ xpath variables
EUQ_SP_ADD_BUTTON = "//input[@id='euq_add' and @value='Add Service Provider...']"
EUQ_IDP_ADD_BUTTON = "//input[@id='euq_add' and @value='Add Identity Provider...']"
EUQ_PROFILE_TABLE= '//table[@id="euq_profile"]'
EUQ_PROFILE_EDIT_LINK= lambda name: "%s//a[normalize-space()='%s']" % (EUQ_PROFILE_TABLE, name)
EUQ_DOWNLOAD_SP_METADATA_BUTTON = '//input[@id="euq_export_sp_metadata"]'
EUQ_IDP_VIEW_METADATA_BUTTON = '//input[@id="euq_idp_metadata"]'
EUQ_DELETE_BUTTON= lambda name: "%s//td[.//a[normalize-space()='%s']]" \
                      "/following-sibling::td/img[@title='Delete...']" % (EUQ_PROFILE_TABLE, name)


class Saml(GuiCommon):

    """Keywords for System Administration -> SAML"""

    def get_keyword_names(self):
        return [
            'saml_add_sp_and_idp',
            'saml_edit_sp_and_idp',
            'saml_download_sp_metadata',
            'saml_delete_sp_idp',
            'saml_view_idp_metadata',
            'saml_get_details',
            'saml_add_sp_and_idp_for_euq',
            'saml_edit_euq_sp_and_idp_profile',
            'saml_download_euq_sp_metadata',
            'saml_view_euq_idp_metadata',
            'saml_get_euq_details',
            'saml_delete_euq_profiles'
            ]

    def _wait_for_page(self, title_part, timeout_sec=10):
        timer = CountDownTimer(timeout_sec).start()
        while timer.is_active():
            titles = self.get_window_titles()
            for title in titles:
                if title.find(title_part) >= 0:
                    return title
            time.sleep(1)
        raise guiexceptions.GuiPageNotFoundError(
                'Page title containing "%s" has not been found'\
                ' within %d seconds timeout' % (title_part, timeout_sec))

    @set_speed(0.5)
    def _saml_add_sp(self, profile_name, settings):
        sp_settings = copy.copy(settings)
        remove_elem = ['Configuration Mode', 'Import IDP Metadata', 'SSO URL', 'IDP Profile Name', 'IDP Entity ID', \
                       'Certificate']
        for element_remove in remove_elem:
            if element_remove in sp_settings:
                sp_settings.pop(element_remove)
        if not 'SP Profile Name' in sp_settings:
            sp_settings.update({'SP Profile Name': profile_name})
        self.sp_settings_controller = ServiceProviderSettings(self)
        self.sp_settings_controller.set(sp_settings)
        self._click_submit_button()

    @set_speed(0.5)
    def _saml_add_idp(self, profile_name, settings):
        idp_settings = copy.copy(settings)
        remove_elem = ['Organization URL', 'Organization Display Name', 'SP Entity ID', \
                       'Organization Technical Contact','Certificate Passphrase', 'Sign Requests', 'Private Key', \
                       'Assertion Consumer URL', 'SP Profile Name','SP Certificate', 'Organization Name', \
                       'Sign Assertions','Certificate Upload Action', 'PKCS Certificate',  \
                       'PKCS Certificate Passphrase']
        for element_remove in remove_elem:
            if element_remove in idp_settings:
                idp_settings.pop(element_remove)
        if not 'IDP Profile Name' in idp_settings:
            idp_settings.update({'IDP Profile Name': profile_name})
        self.id_settings_controller = IdentityProviderSettings(self)
        self.id_settings_controller.set(idp_settings)
        self._click_submit_button()

    @set_speed(0.5)
    def _check_saml_locator_and_click(self, role, customer_locator, devops_locator,  customer_error_msg, \
                                      devops_error_msg, dont_wait=False):
        if role.lower()=='admin':
            if not self._is_element_present(customer_locator):
                raise guiexceptions.ConfigError(customer_error_msg)
            if dont_wait:
                self.click_button(customer_locator, 'don\'t wait')
            else:
                self.click_button(customer_locator)
        elif role.lower()=='devops':
            if not self._is_element_present(devops_locator):
                raise guiexceptions.ConfigError(devops_error_msg)
            if dont_wait:
                self.click_button(devops_locator, 'don\'t wait')
            else:
                self.click_button(devops_locator)
        else:
            raise guiexceptions.ConfigError('Wrong User role given')

    @go_to_page(PAGE_PATH)
    def saml_add_sp_and_idp(self, sp_name, idp_name, settings = {}):
        """ Adds a Customer or DevOps's Service provider profile and Identity Provider with given settings.

        *Parameters:*
        - `sp_name`: Service provider's profile name.
        - `idp_name`: Identity provider's profile name.
        - `settings`: A dictionary which items can be:
        | User Role | This value could be either devops or admin. By default admin.|
        | SP Entity ID | The Service Provider Entity ID is used to uniquely identify a
        service provider. The format of the Service Provider Entity ID is typically a URI |
        | Assertion Consumer URL | The URL to where the Identity Provider should send the
        SAML assertion after authentication has successfully completed.|
        | Certificate Upload Action | We can Choose 'Upload Certificate Key' or 'Upload PKCS Certificate'.
	    If we choose Upload Certificate Key we should use SP Certificate, Private Key
        and Certificate Passphrase parameters. . If we Choose Upload PKCS Certificate we should use
	    PKCS Certificate and PKCS Certificate Passphrase |
        | SP Certificate | Service provider's certificate |
        | Private Key | Service provider's private key |
        | Certificate Passphrase | Password of Service provider's certificate|
        | PKCS Certificate | PKCS certificate file path |
        | PKCS Certificate Passphrase | PKCS certificate password |
        | Sign Requests | Whether to sign SAML requests or not. ${True}/${False} |
        | Sign Assertions | Whether to sign SAML assertions or not. ${True}/${False} |
        | Organization Name | Name of the origanization |
        | Organization Display Name | Name to display for the above configured organization |
        | Organization URL | URL of the the above configured organization |
        | Organization Technical Contact | Point of technical contact of the above configured organization|
        | IDP Entity ID | The Service Provider Entity ID is used to uniquely identify the identity
        | Configuration Mode | Configure Keys Manually or Import IDP Metadata |
        | SSO URL | The URL to which SP should send SAML Auth requests. |
        | Certificate | Identity providers certificate in PEM format. |

        *Examples:*
        | ${settings}=  | Create Dictionary     |
        | ... | User Role                       | admin |
        | ... | SP Entity ID                    | test_sp |
        | ... | Name ID Format                  | urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress |
        | ... | Assertion Consumer URL          | http://${DUT}:80 |
        | ... | Certificate Upload Action       | Upload Certificate Key |
        | ... | SP Certificate                  | ${cert_file} |
        | ... | Private Key                     | ${cert_key} |
        | ... | Certificate Passphrase          | ironport |
        | ... | Sign Requests                   | ${True} |
        | ... | Sign Assertions                 | ${False} |
        | ... | Organization Name               | Test Organization |
        | ... | Organization Display Name       | testORG |
        | ... | Organization URL                | http://torg.org/test |
        | ... | Organization Technical Contact  | %{USER}@cisco.com |
        | ... | Configuration Mode              | Import IDP Metadata |
        | ... | Import IDP Metadata             | ${idp_metadata} |  #String contain IDP meta data
        | SAML ADD SP AND IDP                   | sp_name | idp_name | ${settings} |
        """
        local_settings = copy.copy(settings)
        if local_settings.has_key('User Role'):
            user_role = local_settings.get('User Role')
            local_settings.pop('User Role')
        else:
            user_role = 'admin'
        if not local_settings.has_key('Certificate Upload Action'):
            local_settings['Certificate Upload Action'] = 'Upload Certificate Key'
        # fix to work with SP and IDP...
        self._check_saml_locator_and_click(user_role, CUSTOMER_SP_ADD_BUTTON, DEVOPS_SP_ADD_BUTTON, \
                                 'Could not find "Add Service Provider..." button for admin user', \
                                 'Could not find "Add Identity Provider..." button for devops user')
        self._saml_add_sp(sp_name, local_settings)
        self._check_saml_locator_and_click(user_role, CUSTOMER_IDP_ADD_BUTTON, DEVOPS_IDP_ADD_BUTTON, \
            'Could not find "Add Service Identity Provider..." button for admin user', \
            'Could not find "Add Service Identity Provider..." button for devops user')
        self._saml_add_idp(idp_name, local_settings)

    @go_to_page(PAGE_PATH)
    def saml_edit_sp_and_idp(self, sp_name, idp_name, settings = {}):
        """ Edits a Customer or DevOps's Service provider  and Identity Provider profile with given settings.

        *Parameters:*
        - `sp_name`: Service provider's profile name.
        - `idp_name`: Identity provider's profile name.
        - `settings`: A dictionary which items can be:
        | User Role | This value could be either devops or admin. By default admin.|
        | SP Profile Name | The new Service provider name |
        | SP Entity ID | The Service Provider Entity ID is used to uniquely identify a
        service provider. The format of the Service Provider Entity ID is typically a URI |
        | Assertion Consumer URL | The URL to where the Identity Provider should send the
        SAML assertion after authentication has successfully completed.|
        | Certificate Upload Action | We can Choose 'Upload Certificate Key' or 'Upload PKCS Certificate'.
	    If we choose Upload Certificate Key we should use SP Certificate, Private Key
        and Certificate Passphrase parameters. . If we Choose Upload PKCS Certificate we should use
	    PKCS Certificate and PKCS Certificate Passphrase |
        | SP Certificate | Service provider's certificate |
        | Private Key | Service provider's private key |
        | Certificate Passphrase | Password of Service provider's certificate|
        | PKCS Certificate | PKCS certificate file path |
        | PKCS Certificate Passphrase | PKCS certificate password |
        | Sign Requests | Whether to sign SAML requests or not. ${True}/${False} |
        | Sign Assertions | Whether to sign SAML assertions or not. ${True}/${False} |
        | Organization Name | Name of the origanization |
        | Organization Display Name | Name to display for the above configured organization |
        | Organization URL | URL of the the above configured organization |
        | Organization Technical Contact | Point of technical contact of the above configured organization|
        | IDP Profile Name | The new Identity Provider name |
        | IDP Entity ID | The Service Provider Entity ID is used to uniquely identify the identity
        | Configuration Mode | Configure Keys Manually or Import IDP Metadata |
        | SSO URL | The URL to which SP should send SAML Auth requests. |
        | Certificate | Identity providers certificate in PEM format. |

        *Examples:*
        | ${settings}=  | Create Dictionary     |
        | ... | User Role                       | devops |
        | ... | SP Profile Name                 | new_sp_value |
        | ... | SP Entity ID                    | test_sp |
        | ... | Name ID Format                  | urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress |
        | ... | Assertion Consumer URL          | http://${DUT}:80 |
        | ... | Certificate Upload Action       | Upload Certificate Key |
        | ... | SP Certificate                  | ${cert_file} |
        | ... | Private Key                     | ${cert_key} |
        | ... | Certificate Passphrase          | ironport |
        | ... | Sign Requests                   | ${True} |
        | ... | Sign Assertions                 | ${False} |
        | ... | Organization Name               | Test Organization |
        | ... | Organization Display Name       | testORG |
        | ... | Organization URL                | http://torg.org/test |
        | ... | Organization Technical Contact  | %{USER}@cisco.com |
        | ... | IDP Profile Name                | new_idp_name |
        | ... | Configuration Mode              | Import IDP Metadata |
        | ... | Import IDP Metadata             | ${idp_metadata} |  #String contain IDP meta data
        | SAML EDIT SP AND IDP                  | sp_name | idp_name | ${settings} |
        """
        local_settings = copy.copy(settings)
        if local_settings.has_key('User Role'):
            user_role = local_settings.get('User Role')
            local_settings.pop('User Role')
        else:
            user_role = 'admin'
        if not local_settings.has_key('Certificate Upload Action'):
            local_settings['Certificate Upload Action'] = 'Upload Certificate Key'
        self._check_saml_locator_and_click(user_role, CUSTOMER_EDIT_LINK(sp_name), DEVOPS_EDIT_LINK(sp_name), \
                                 'Service Provider or Identity Provider profile named "%s" does not exist or it is \
                                 not editable for admin user' % (sp_name,), \
                                 'Service Provider or Identity Provider profile named "%s" does not exist or it is \
                                 not editable for devops user' % (sp_name,))
        self._saml_add_sp(sp_name, local_settings)
        self._check_saml_locator_and_click(user_role, CUSTOMER_EDIT_LINK(idp_name), \
                                           DEVOPS_EDIT_LINK(idp_name), \
                                 'Service Provider or Identity Provider profile named "%s" does not exist or it is \
                                 not editable for admin user' % (idp_name,), \
                                 'Service Provider or Identity Provider profile named "%s" does not exist or it is \
                                 not editable for devops user' % (idp_name,))
        self._saml_add_idp(idp_name, local_settings)

    @go_to_page(PAGE_PATH)
    def saml_download_sp_metadata(self, user_role='admin'):
        """ Downloads the customer or DevOps's Service provider's metadata to the local system.

        Below steps before calling
        These are required to suppress system level browser popup during download.

        Close All Browsers
        Selenium Close
        ${firefox_prefs_browser.download.folderList}=  Set Variable  2
        ${firefox_prefs_browser.download.dir}=  Set Variable  %{SARF_HOME}/tmp/
        ${firefox_prefs_browser.helperApps.neverAsk.openFile}=  Set Variable  text/xml
        ${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}=  Set Variable  text/xml
        Selenium Login

        *Parameters:*
        - `user_role`: This value could be either devops or admin. By default admin.

        *Return:*
        - None

        *Example:*
        | Close All Browsers                                      |
        | Selenium Close                                          |
        | ${firefox_prefs_browser.download.folderList}=           | Set Variable | 2 |
        | ${firefox_prefs_browser.download.dir}=                  | Set Variable | %{SARF_HOME}/tmp/ |
        | ${firefox_prefs_browser.helperApps.neverAsk.openFile}   | Set Variable | text/xml |
        | ${firefox_prefs_browser.helperApps.neverAsk.saveToDisk} | Set Variable | text/xml |
        | SAML Download Sp Metadata                   |  admin    |
        """

        self._check_saml_locator_and_click(user_role.lower(), CUSTOMER_DOWNLOAD_SP_METADATA, \
                                           DEVOPS_DOWNLOAD_SP_METADATA, \
                                           'admin user "Download Metadata" button not found for Service Provider',\
                                           'devops user "Download Metadata" button not found for Service Provider', \
                                           dont_wait=True)

    @go_to_page(PAGE_PATH)
    def saml_delete_sp_idp(self, **args):
        """ Deletes a given customer or DevOps's Service provider and Identity provider profile.

        *Parameters:*
        - `sp_name`: Service Proivder name.
        - `idp_name`: Identity Provider name.
        - `user_role`: This value could be either devops or admin. By default admin.

        *Return:*
        - None

        *Example:*
        | SAML DELETE SP IDP | sp_name=test_sp | idp_name=testidp | user_role=devops |
        | SAML DELETE SP IDP | sp_name=test_sp |
        | SAML DELETE SP IDP | idp_name=testidp | user_role=devops |
        | SAML DELETE SP IDP | sp_name=test_sp | idp_name=testidp |

        """
        kwargs = args
        idp_name = kwargs.get('idp_name')
        sp_name = kwargs.get('sp_name')
        if kwargs.get('user_role')== None:
            user_role = 'admin'
        else:
            user_role = kwargs.get('user_role')
        if sp_name:
            self._check_saml_locator_and_click(user_role.lower(),
                                               CUSTOMER_DELETE_BUTTON(sp_name), \
                                               DEVOPS_DELETE_BUTTON(sp_name),\
                                               'Service Proivder or Identity provider profile named "%s" does not exist \
                                               or cannot be deleted for admin user' % (sp_name), \
                                               'Service Proivder or Identity provider profile named "%s" does not exist\
                                               or cannot be deleted for devops user' % (sp_name), dont_wait=True)
        self._click_continue_button()
        if idp_name:
            self._check_saml_locator_and_click(user_role.lower(),
                                               CUSTOMER_DELETE_BUTTON(idp_name), \
                                               DEVOPS_DELETE_BUTTON(idp_name), \
                                               'Service Proivder or Identity provider profile named "%s" does not exist \
                                               or cannot be deleted for admin user' % (idp_name), \
                                               'Service Proivder or Identity provider profile named "%s" does not exist\
                                               or cannot be deleted for devops user' % (idp_name), dont_wait=True)
        self._click_continue_button()

    @go_to_page(PAGE_PATH)
    def saml_view_idp_metadata(self, user_role='admin'):
        """ Views the customer or DevOps's configured Identity providers metadata.

        *Parameters:*
        - `user_role`: This value could be either devops or admin. By default admin.

        *Return:*
        - Returns the configured Identity providers metadata (XML content) in string format.
        """
        self._check_saml_locator_and_click(user_role.lower(), CUSTOMER_IDP_VIEW_METADATA_BUTTON,\
                                          DEVOPS_IDP_VIEW_METADATA_BUTTON,\
                                          '"View Metadata" button not found for Identity Provider for admin user',\
                                          '"View Metadata" button not found for Identity Provider for devops user', \
                                          dont_wait=True)

        idp_metadata_preview_page = self._wait_for_page('Preview')
        self.select_window(idp_metadata_preview_page)
        idp_metadata = self.get_text("//table[@class='pairs']/tbody/tr")
        self.close_window()
        self.select_window('main')
        return idp_metadata

    @set_speed(0)
    def _saml_get_table_details(self, profile):
        """
        :param table: sp|idp based on the table values will be return
        ved.
        :return: result dictionary
        """
        result = {}
        if profile == 'user_sp_profile' or profile == 'user_idp_profile':
            new_profile = 'user_profile'
            if  self._is_element_present(CUSTOMER_SP_ADD_BUTTON) or \
                    self._is_element_present(CUSTOMER_IDP_ADD_BUTTON):
                raise guiexceptions.GuiValueError('Table not found..')
        elif profile == 'devops_sp_profile' or profile == 'devops_idp_profile':
            new_profile = 'devops_profile'
            if  self._is_element_present(DEVOPS_SP_ADD_BUTTON) or \
                    self._is_element_present(DEVOPS_IDP_ADD_BUTTON):
                raise guiexceptions.GuiValueError('Table not found..')
        else:
            new_profile = profile
        KEYS_TABLE = "//*[@id='%s']" %(new_profile)
        SP_HEADER_NAMES = "%s/tbody/tr[2]/th" % (KEYS_TABLE,)
        IDP_HEADER_NAMES = "%s/tbody/tr[5]/th" % (KEYS_TABLE,)
        CELL_BY_IDX = lambda row_idx, col_idx: "%s/tbody/tr[%d]/td[%d]" % \
                                               (KEYS_TABLE, row_idx, col_idx)
        if 'sp' in profile:
            row_index = [3]
            headers_count = int(self.get_matching_xpath_count(SP_HEADER_NAMES))
            HEADER_BY_IDX = lambda idx: "%s[%d]" % (SP_HEADER_NAMES, idx)
        if 'idp' in profile:
            row_index = [6]
            headers_count = int(self.get_matching_xpath_count(IDP_HEADER_NAMES))
            HEADER_BY_IDX = lambda idx: "%s[%d]" % (IDP_HEADER_NAMES, idx)
        for col_idx in xrange(1, headers_count):
            for row_idx in row_index:
                result[self.get_text(HEADER_BY_IDX(col_idx)).strip()] = \
                    self.get_text(CELL_BY_IDX(row_idx, col_idx)).strip()
        return result

    @go_to_page(PAGE_PATH)
    def saml_get_details(self, profile):
        """
        Keyword to get the saml table details
        :param profile: user_sp_profile |user_idp_profile | devops_sp_profile | devops_idp_profile
        :return: saml_details
        """
        saml_details = {}
        if 'idp' in profile:
            saml_details['Identity Provider Settings'] = self._saml_get_table_details(profile)
        else:
            saml_details['Service Provider Settings']  = self._saml_get_table_details(profile)
        return saml_details


    @go_to_page(PAGE_PATH)
    def saml_add_sp_and_idp_for_euq(self, sp_name, idp_name, settings = {}):
        """ Adds a Customer Service provider profile and Identity Provider for euq  with given settings.

        *Parameters:*
        - `sp_name`: Service provider's profile name.
        - `idp_name`: Identity provider's profile name.
        - `settings`: A dictionary which items can be:
        | User Role |  By default admin.|
        | SP Entity ID | The Service Provider Entity ID is used to uniquely identify a
        service provider. The format of the Service Provider Entity ID is typically a URI |
        | Assertion Consumer URL | The URL to where the Identity Provider should send the
        SAML assertion after authentication has successfully completed.|
        | Certificate Upload Action | We can Choose 'Upload Certificate Key' or 'Upload PKCS Certificate'.
            If we choose Upload Certificate Key we should use SP Certificate, Private Key
        and Certificate Passphrase parameters. . If we Choose Upload PKCS Certificate we should use
            PKCS Certificate and PKCS Certificate Passphrase |
        | SP Certificate | Service provider's certificate |
        | Private Key | Service provider's private key |
        | Certificate Passphrase | Password of Service provider's certificate|
        | PKCS Certificate | PKCS certificate file path |
        | PKCS Certificate Passphrase | PKCS certificate password |
        | Sign Requests | Whether to sign SAML requests or not. ${True}/${False} |
        | Sign Assertions | Whether to sign SAML assertions or not. ${True}/${False} |
        | Organization Name | Name of the origanization |
        | Organization Display Name | Name to display for the above configured organization |
        | Organization URL | URL of the the above configured organization |
        | Organization Technical Contact | Point of technical contact of the above configured organization|
        | IDP Entity ID | The Service Provider Entity ID is used to uniquely identify the identity
        | Configuration Mode | Configure Keys Manually or Import IDP Metadata |


        *Examples:*
        | ${settings}=  | Create Dictionary     |
        | ... | User Role                       | admin |
        | ... | SP Entity ID                    | test_sp |
        | ... | Name ID Format                  | urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress |
        | ... | Assertion Consumer URL          | http://${DUT}:83 |
        | ... | Certificate Upload Action       | Upload Certificate Key |
        | ... | SP Certificate                  | ${cert_file} |
        | ... | Private Key                     | ${cert_key} |
        | ... | Certificate Passphrase          | ironport |
        | ... | Sign Requests                   | ${True} |
        | ... | Sign Assertions                 | ${False} |
        | ... | Organization Name               | Test Organization |
        | ... | Organization Display Name       | testORG |
        | ... | Organization URL                | http://torg.org/test |
        | ... | Organization Technical Contact  | %{USER}@cisco.com |
        | ... | Configuration Mode              | Import IDP Metadata |
        | ... | Import IDP Metadata             | ${idp_metadata} |  #String contain IDP meta data
        | SAML ADD SP AND IDP FOR EUQ           | sp_name | idp_name | ${settings} |
        """
        local_settings = copy.copy(settings)
        if local_settings.has_key('User Role'):
            user_role = local_settings.get('User Role')
            local_settings.pop('User Role')
        else:
            user_role = 'admin'

        if not local_settings.has_key('Certificate Upload Action'):
            local_settings['Certificate Upload Action'] = 'Upload Certificate Key'

        self._check_saml_locator_and_click(user_role, EUQ_SP_ADD_BUTTON,None,\
              'Could not find "EUQ Add Service Provider..." button for admin user',\
               None)
        self._saml_add_sp(sp_name, local_settings)

        self._check_saml_locator_and_click(user_role, EUQ_IDP_ADD_BUTTON,None,\
            'Could not find "Add Service Identity Provider..." button for admin user',\
            None)
        self._saml_add_idp(idp_name, local_settings)

    @go_to_page(PAGE_PATH)
    def saml_edit_euq_sp_and_idp_profile(self, sp_name, idp_name, settings = {}):
        """ Edits EUQ Service provider  and Identity Provider profile with given settings.

        *Parameters:*
        - `sp_name`: Service provider's profile name.
        - `idp_name`: Identity provider's profile name.
        - `settings`: A dictionary which items can be:
        | User Role | By default admin.|
        | SP Profile Name | The new Service provider name |
        | SP Entity ID | The Service Provider Entity ID is used to uniquely identify a
        service provider. The format of the Service Provider Entity ID is typically a URI |
        | Assertion Consumer URL | The URL to where the Identity Provider should send the
        SAML assertion after authentication has successfully completed.|
        | Certificate Upload Action | We can Choose 'Upload Certificate Key' or 'Upload PKCS Certificate'.
            If we choose Upload Certificate Key we should use SP Certificate, Private Key
        and Certificate Passphrase parameters. . If we Choose Upload PKCS Certificate we should use
            PKCS Certificate and PKCS Certificate Passphrase |
        | SP Certificate | Service provider's certificate |
        | Private Key | Service provider's private key |
        | Certificate Passphrase | Password of Service provider's certificate|
        | PKCS Certificate | PKCS certificate file path |
        | PKCS Certificate Passphrase | PKCS certificate password |
        | Sign Requests | Whether to sign SAML requests or not. ${True}/${False} |
        | Sign Assertions | Whether to sign SAML assertions or not. ${True}/${False} |
        | Organization Name | Name of the origanization |
        | Organization Display Name | Name to display for the above configured organization |
        | Organization URL | URL of the the above configured organization |
        | Organization Technical Contact | Point of technical contact of the above configured organization|
        | IDP Profile Name | The new Identity Provider name |
        | IDP Entity ID | The Service Provider Entity ID is used to uniquely identify the identity
        | Configuration Mode | Configure Keys Manually or Import IDP Metadata |
        | SSO URL | The URL to which SP should send SAML Auth requests. |
        | Certificate | Identity providers certificate in PEM format. |

        *Examples:*
        | ${settings}=  | Create Dictionary     |
        | ... | User Role                       | admin |
        | ... | SP Profile Name                 | new_sp_value |
        | ... | SP Entity ID                    | test_sp |
        | ... | Name ID Format                  | urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress |
        | ... | Assertion Consumer URL          | http://${DUT}:80 |
        | ... | Certificate Upload Action       | Upload Certificate Key |
        | ... | SP Certificate                  | ${cert_file} |
        | ... | Private Key                     | ${cert_key} |
        | ... | Certificate Passphrase          | ironport |
        | ... | Sign Requests                   | ${True} |
        | ... | Sign Assertions                 | ${False} |
        | ... | Organization Name               | Test Organization |
        | ... | Organization Display Name       | testORG |
        | ... | Organization URL                | http://torg.org/test |
        | ... | Organization Technical Contact  | %{USER}@cisco.com |
        | ... | IDP Profile Name                | new_idp_name |
        | ... | Configuration Mode              | Import IDP Metadata |
        | ... | Import IDP Metadata             | ${idp_metadata} |  #String contain IDP meta data
        | SAML EDIT EUQ SP AND IDP PROFILE      | sp_name | idp_name | ${settings} |
        """
        local_settings = copy.copy(settings)
        if local_settings.has_key('User Role'):
            user_role = local_settings.get('User Role')
            local_settings.pop('User Role')
        else:
            user_role = 'admin'

        if not local_settings.has_key('Certificate Upload Action'):
            local_settings['Certificate Upload Action'] = 'Upload Certificate Key'
        self._check_saml_locator_and_click(user_role, EUQ_PROFILE_EDIT_LINK(sp_name), None, \
                                 'Service Provider or Identity Provider profile named "%s" does not exist or it is \
                                 not editable for admin user' % (sp_name,), None)
        self._saml_add_sp(sp_name, local_settings)
        self._check_saml_locator_and_click(user_role, EUQ_PROFILE_EDIT_LINK(idp_name),None, \
                                 'Service Provider or Identity Provider profile named "%s" does not exist or it is \
                                 not editable for admin user' % (idp_name,),None)
        self._saml_add_idp(idp_name, local_settings)

    @go_to_page(PAGE_PATH)
    def saml_view_euq_idp_metadata(self, user_role='admin'):
        """ Views the EUQs configured Identity providers metadata.

        *Parameters:*
        - `user_role`:By default admin.

        *Return:*
        - Returns the configured Identity providers metadata (XML content) in string format.
        """
        self._check_saml_locator_and_click(user_role.lower(), EUQ_IDP_VIEW_METADATA_BUTTON,None,\
                                          '"View Metadata" button not found for Identity Provider for admin user',\
                                          None,dont_wait=True)

        idp_metadata_preview_page = self._wait_for_page('Preview')
        self.select_window(idp_metadata_preview_page)
        idp_metadata = self.get_text("//table[@class='pairs']/tbody/tr")
        self.close_window()
        self.select_window('main')
        return idp_metadata

    @go_to_page(PAGE_PATH)
    def saml_download_euq_sp_metadata(self, user_role='admin'):
        """ Downloads the EUQ Service provider's metadata to the local system.

        Below steps before calling
        These are required to suppress system level browser popup during download.

        Close All Browsers
        Selenium Close
        ${firefox_prefs_browser.download.folderList}=  Set Variable  2
        ${firefox_prefs_browser.download.dir}=  Set Variable  %{SARF_HOME}/tmp/
        ${firefox_prefs_browser.helperApps.neverAsk.openFile}=  Set Variable  text/xml
        ${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}=  Set Variable  text/xml
        Selenium Login

        *Parameters:*
        - `user_role`: This value could be either devops or admin. By default admin.

        *Return:*
        - None

        *Example:*
        | Close All Browsers                                      |
        | Selenium Close                                          |
        | ${firefox_prefs_browser.download.folderList}=           | Set Variable | 2 |
        | ${firefox_prefs_browser.download.dir}=                  | Set Variable | %{SARF_HOME}/tmp/ |
        | ${firefox_prefs_browser.helperApps.neverAsk.openFile}   | Set Variable | text/xml |
        | ${firefox_prefs_browser.helperApps.neverAsk.saveToDisk} | Set Variable | text/xml |
        | SAML Download EUQ Sp Metadata                   |  admin    |
        """

    @set_speed(0)
    def _saml_get_euq_table_details(self, profile):
        """
        :param table: sp|idp based on the table values will be return
        ved.
        :return: result dictionary
        """
        result = {}
        if profile == 'euq_sp_profile' or profile == 'euq_idp_profile':
            new_profile = 'euq_profile'
            if  self._is_element_present(EUQ_SP_ADD_BUTTON) or \
                    self._is_element_present(EUQ_IDP_ADD_BUTTON):
                raise guiexceptions.GuiValueError('Table not found..')
        else:
            new_profile = profile
        KEYS_TABLE = "//*[@id='%s']" %(new_profile)
        SP_HEADER_NAMES = "%s/tbody/tr[2]/th" % (KEYS_TABLE,)
        IDP_HEADER_NAMES = "%s/tbody/tr[5]/th" % (KEYS_TABLE,)
        CELL_BY_IDX = lambda row_idx, col_idx: "%s/tbody/tr[%d]/td[%d]" % \
                                               (KEYS_TABLE, row_idx, col_idx)
        if 'sp' in profile:
            row_index = [3]
            headers_count = int(self.get_matching_xpath_count(SP_HEADER_NAMES))
            HEADER_BY_IDX = lambda idx: "%s[%d]" % (SP_HEADER_NAMES, idx)
        if 'idp' in profile:
            row_index = [6]
            headers_count = int(self.get_matching_xpath_count(IDP_HEADER_NAMES))
            HEADER_BY_IDX = lambda idx: "%s[%d]" % (IDP_HEADER_NAMES, idx)
        for col_idx in xrange(1, headers_count):
            for row_idx in row_index:
                result[self.get_text(HEADER_BY_IDX(col_idx)).strip()] = \
                    self.get_text(CELL_BY_IDX(row_idx, col_idx)).strip()
        return result

    @go_to_page(PAGE_PATH)
    def saml_get_euq_details(self, profile):
        """
        Keyword to get the saml euq table details
        :param profile: euq_sp_profile |euq_idp_profile
        :return: saml_euq_details
        """
        saml_euq_details = {}
        if 'idp' in profile:
            saml_euq_details['Identity Provider Settings'] = self._saml_get_euq_table_details(profile)
        else:
            saml_euq_details['Service Provider Settings']  = self._saml_get_euq_table_details(profile)
        return saml_euq_details


    @go_to_page(PAGE_PATH)
    def saml_delete_euq_profiles(self, sp_name = None, idp_name = None):
        """ Deletes a given Service provider and Identity provider profile.

        *Parameters:*
        - `sp_name`: Service Proivder name.
        - `idp_name`: Identity Provider name.

        *Return:*
        - None

        *Example:*
        | SAML DELETE EUQ PROFILES | sp_name=test_sp | idp_name=testidp |
        | SAML DELETE EUQ PROFILES | sp_name=test_sp |
        | SAML DELETE EUQ PROFILES | idp_name=testidp|

        """

        if sp_name:
           if not self._is_element_present(EUQ_DELETE_BUTTON(sp_name)):
              raise guiexceptions.ConfigError('EUQ Service Proivder profile named "%s" does not exist or cannot be deleted'% (sp_name))
           else:
              self.click_element(EUQ_DELETE_BUTTON(sp_name))
              self._click_continue_button()
        if idp_name:
           if not self._is_element_present(EUQ_DELETE_BUTTON(idp_name)):
              raise guiexceptions.ConfigError('EUQ Identity Proivder profile named "%s" does not exist or cannot be deleted'% (idp_name))
           else:
              self.click_element(EUQ_DELETE_BUTTON(idp_name))
              self._click_continue_button()

