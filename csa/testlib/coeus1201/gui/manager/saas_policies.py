#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/saas_policies.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.gui.guicommon import GuiCommon
from common.gui import guiexceptions

POLICY = lambda name: "//strong[contains(text(),'{name}')]".format(name=name)

class SaasPolicies(GuiCommon):
    """SaaS Application Authentication Policies page interaction class.

    This class designed to interact with GUI elements of Web Security Manager ->
    SaaS Policies page. Use keywords, listed below, to configure SaaS
    Applications Authentication Policies.

    Before configuring SaaS Policies, make sure that WSA is configured as
    Identity Provider for SaaS and at least one Authentication Realm has been
    created.
    """

    _name_column = 1
    _table_id = "//table[@class='cols']"
    _attr_mapping_table_id = "//tbody[@id='attribute_mapping_rowContainer']"

    _sp_id_formats = ['X509SubjectName',
                      'Kerberos',
                      'Unspecified',
                      'Entity',
                      'Transient',
                      'EmailAddress',
                      'WindowsDomainNameQualifiedName']

    _saml_username_mappings = ['No mapping',
                               'LDAP query',
                               'Fixed Rule mapping']

    _auth_contexts = ['SecureRemotePassword',
                      'InternetProtocolPassword',
                      'AuthenticatedTelephony',
                      'Unspecified',
                      'PreviousSession',
                      'MobileTwoFactorUnregistered',
                      'MobileTwoFactorContract',
                      'Kerberos',
                      'Public Key - XMLDSig',
                      'MobileOneFactorContract',
                      'Public Key - X.509',
                      'MobileOneFactorUnregistered',
                      'TLSClient',
                      'Automatic',
                      'SoftwarePKI',
                      'PasswordProtectedTransport',
                      'Public Key - SPKI',
                      'Password',
                      'Smartcard',
                      'PersonalTelephony',
                      'InternetProtocol',
                      'Telephony',
                      'Public Key - PGP',
                      'SmartcardPKI',
                      'NomadTelephony',
                      'TimeSyncToken']

    def get_keyword_names(self):
        return ['saas_policies_enable_saas_application',
                'saas_policies_disable_saas_application',
                'saas_policies_add_saas_application',
                'saas_policies_edit_saas_application',
                'saas_policies_edit_saas_application_user_and_groups',
                'saas_policies_delete_saas_application',
                'saas_policies_get_list',
                ]

    def _open_page(self):
        """Open 'SaaS Policies' page """

        self._navigate_to('Web Security Manager', 'SaaS Policies')

    def _click_add_application_button(self):
        """Click 'Add Application...' button"""

        add_button = "//input[@value='Add Application...']"
        self.click_button(add_button)

    def _get_table_row_index(self, name, table_id, column):
        """fetches table row index by name"""

        table_rows = int(self.get_matching_xpath_count("%s//tr" \
                                                       % (table_id,)))
        for i in xrange(2, table_rows + 1):
            item_name = self.get_text("%s//tr[%s]//td[%s]" % \
                        (table_id, i, column)).split(' \n')[0]
            if item_name == name:
                return i
        return None

    def _click_next_button(self):
        """Click on Next button"""
        self.click_button("//input[@value='Next']")

    def _click_delete_application(self, name):
        """Click on 'Delete' sign."""
        DELETE_CHECKBOX = "/ancestor::tr[1]//img[contains(@src, 'trash.gif')]"
        self.click_element(POLICY(name)+DELETE_CHECKBOX, "don't wait")

        self.click_button("//button[text()='Delete']")

    def _is_app_enabled(self, name):
        """Checks whether application is enabled"""
        POLICY_DISABLED = POLICY(name) + \
            "/ancestor::td[1]/span[contains(text(), '(disabled)')]"

        return not self._is_visible(POLICY_DISABLED)

    def _click_edit_application(self, name):
        """Click on application name to edit application settings"""

        self.click_element(POLICY(name))

    def _click_import_button(self):
        """Click 'Import' button"""

        import_button = "//input[@id='import_button']"
        self.click_button(import_button)
        self._check_action_result()

    def _enable_saas_application_checkbox(self):
        """Set enabling checkbox to checked state"""

        saas_application_checkbox = "//input[@id='enabled']"
        self.select_checkbox(saas_application_checkbox)

    def _disable_saas_application_checkbox(self):
        """Set enabling checkbox to unchecked state"""

        saas_application_checkbox = "//input[@id='enabled']"
        self.unselect_checkbox(saas_application_checkbox)

    def _check_configuration_avaliability(self):
        """Gets attention messages if SaaS Policy configuration is not
        available"""

        result = self.get_text("//*[@id='action-results-title']")
        msg = self.get_text("//*[@id='action-results-message']")

        if result == "Attention":
            e = guiexceptions.ConfigError(msg)
            raise e

        self._check_feature_status('saas_id_provider')

    def _click_on_all_authenticated_users_link(self, name):
        """Click on all authenticated users link"""

        cell_id = "//strong[normalize-space() = '%s']/../../../td[3]/a" \
        % (name,)
        self.click_element(cell_id)

    def _select_authentication_prompt(self, saas_sso_authentication_prompt):
        """Select SaaS SSO Authentication Prompt"""
        radio_map = {
            'prompt' : "//input [@id='no_need_saas_auth_id']",
            'auto'   : "//input [@id='need_saas_auth_id']",
            }
        prompt = saas_sso_authentication_prompt.lower()
        if (prompt in radio_map.keys()):
            self._click_radio_button(radio_map[prompt])
        else:
            raise guiexceptions.ConfigError(
                'Invalid saas_sso_authentication_prompt ' + prompt +
                ' should be in ' + str(radio_map))

    def _fill_metadata(self, sp_metadata):
        """input Metadata for Service Provider"""

        if len(sp_metadata) == 3:
            # manual keys configuration
            self._click_radio_button('id=metadata_not_uploaded')

            # iput name ID
            self.input_text("//input[@id='entity_id']", sp_metadata[0])

            # select name ID format. if it is empty string, coeus75 default
            # value will be used.
            if sp_metadata[1] is not None:
                if sp_metadata[1].strip() not in self._sp_id_formats:
                    raise guiexceptions.ConfigError(
                            'Service Provider Name ID Format Error')
                self.select_from_list('id=nameid_format',
                            '%s' % sp_metadata[1])

            # input Assertion Consumer Service URL
            self.input_text("//*[@id='acs_location']", sp_metadata[2])

        elif len(sp_metadata) == 1:
            # upload metadata from file
            self._click_radio_button('id=metadata_uploaded')

            # input path to metadata file
            self.choose_file("//input[@id='metadata_xml_id']",
                            sp_metadata[0])

            # press Import key
            self._click_import_button()
            self._check_action_result()
        else:
            raise guiexceptions.ConfigError(
                  'Service Provider Metadata Format Error')

    def _select_saml_username_mapping(self, saml_username_mapping):
        """Select SAML Username Mapping"""

        _format, expression = saml_username_mapping
        if _format in self._saml_username_mappings:
            self.select_from_list('id=name_id_mapping',
                                  '%s' % _format)
            if _format != 'No mapping':
                if expression is not None:
                    self.input_text("//input[@id='name_id_expression']",
                                expression)
                else:
                    raise guiexceptions.ConfigError(
                     'Expression Name is missing in SAML Username Mapping')

    def _delete_attribute_mapping(self):
        """Delete previously defined mappings"""

        table_rows = int(self.get_matching_xpath_count('%s//tr' \
                                            % (self._attr_mapping_table_id,)))

        for i in xrange(1, table_rows):
            cell_id = "%s//tr[@id='attribute_mapping_row%s']" \
                "//td[@id='itable-delete_row%s']/img" % \
                (self._attr_mapping_table_id, i, i)
            self.click_element(cell_id, "don't wait")

    def _fill_saml_attribute_mapping(self, saml_attribute_mapping):
        """Input SAML Attribute Mapping"""

        for i in xrange(len(saml_attribute_mapping)):
            saml_a, ldap_a = self._convert_semicolon_separated_string_to_tuple(
                                    saml_attribute_mapping[i])
            self.input_text(
                "//input[@id='attribute_mapping[%s][attribute_key]']" % i,
                saml_a)
            self.input_text(
                "//input[@id='attribute_mapping[%s][attribute_value]']" % i,
                ldap_a)
            if i != (len(saml_attribute_mapping) - 1):
                self.click_button(
                    "//input[@id='attribute_mapping_domtable_AddRow']",
                    "don't wait")

    def _select_authentication_context(self, authentication_context):
        """Select Authentication Context"""

        if authentication_context in self._auth_contexts:
            self.select_from_list('id=authn_context',
                              '%s' % authentication_context)
        else:
            raise guiexceptions.ConfigError(
                        'Authentication Context option error')

    def saas_policies_enable_saas_application(self, name):
        """Enable SaaS Application Authentication Policy.

        Use this method to enable previously disabled SaaS Application
        Authentication Policy.

        :Parameters:
        - `name`: The name of SaaS Application Authentication Policy to be
        enabled. String. Mandatory.

        Exceptions:
        - GuiControlNotFoundError:xxx

        Example:
        | Saas Policies Enable Application | myAppName |
        """

        self._open_page()
        status = self._is_app_enabled(name)
        # enable if disabled. otherwise do nothing
        if not status:
            self._click_edit_application(name)
            self._enable_saas_application_checkbox()
            self._click_submit_button()
            self._click_next_button()

    def saas_policies_disable_saas_application(self, name):
        """Disable SaaS Application Authentication Policy.

        Use this method to disable SaaS Application Authentication Policy.

        *Parameters*
        - `name`: The name of SaaS Application Authentication Policy to be
        disabled. String. Mandatory.

        *Example*
        | Saas Policies Disable Application | myAppName |
        """

        self._open_page()
        status = self._is_app_enabled(name)
        # disable if enabled. otherwise do nothing
        if status:
            self._click_edit_application(name)
            self._disable_saas_application_checkbox()
            self._click_submit_button()

    def saas_policies_add_saas_application(self,
                                           name,
                                           sp_metadata,
                                           description=None,
                                           auth_realm=None,
                                           saas_sso_authentication_prompt=None,
                                           saml_username_mapping=None,
                                           saml_attribute_mapping=None,
                                           authentication_context=None
                                           ):
        """Add SaaS Application.

        Use this method to create a SaaS Application Authentication Policy.

        *Parameters*
        - `name`: name to identify the SaaS application for this
        policy group. String. Mandatory.
        - `sp_metadata`: metadata that describes the service provider referenced
        in this policy group. List. Should contain 1 or 3 elements. 1 element if
        you want to upload a metadata file provided by the SaaS application. In
        This case list element represents path to metadata file. Otherwise 3
        elements of the list contain the following values:
        _Service Provider Entity ID_ - (typically string in URI format) the SaaS
        application uses to identify itself as a service provider.
        _Name ID Format_ - format the appliance should use to identify users in
        the SAML assertion it sends to service providers. Possible values:
        'X509SubjectName', 'Kerberos', 'Unspecified', 'Entity', 'Transient',
        'EmailAddress', 'WindowsDomainNameQualifiedName'.
        Default value: 'X509SubjectName'.
        _Assertion Consumer Service Location_ - string that contains URL to
        where the Web Security appliance should send the SAML assertion it
        creates.
        - `description`: description for this SaaS application. String. Optional.
        - `auth_realm`: contains authentication realm or authentication
        sequence the Web Proxy should use to authenticate users
        accessing this SaaS application. String. Optional. Default value:
        `All Realms`.
        - `saas_sso_authentication_prompt`: choose whether to allow users to
        transparently sign into the SaaS application using their local
        authentication credentials, or to always prompt users for their
        credentials when accessing the SaaS application. String.
        Either `Prompt` or 'Transparently' or "Automatically". First value used
        by default.
        - `saml_username_mapping`: Specify how the Web Proxy should represent user
        names to the service provider in the SAML assertion. List with 2
        elements. First element represents one of methods:  'No mapping',
        'LDAP query', 'Fixed Rule mapping'. Second element used when method is
        'LDAP query' or 'Fixed Rule mapping'. It represents expression used
        with selected method.
        - `saml_attribute_mapping`: information about the internal users from the
        LDAP authentication server if required by the SaaS application. List
        with strings that contain pairs of values separated by semicolon. (LDAP
        attribute mapped to a SAML attribute). Optional.
        - `authentication_context`: contains one of values:
        'SecureRemotePassword', 'InternetProtocolPassword',
        'AuthenticatedTelephony', 'Unspecified', 'PreviousSession',
        'MobileTwoFactorUnregistered', 'MobileTwoFactorContract', 'Kerberos',
        'Public Key - XMLDSig', 'MobileOneFactorContract', 'Public Key - X.509',
        'MobileOneFactorUnregistered', 'TLSClient', 'Automatic', 'SoftwarePKI',
        'PasswordProtectedTransport', 'Public Key - SPKI', 'Password',
        'Smartcard', 'PersonalTelephony', 'InternetProtocol', 'Telephony',
        'Public Key - PGP', 'SmartcardPKI', 'NomadTelephony', 'TimeSyncToken'.
        Default: 'Automatic'.

        Exceptions:
        - ConfigError: In order to add or edit SaaS applications, you must create at least one authentication realm
        - ConfigError: SaaS SSO Authentication Prompt settings error
        - ConfigError: Service Provider Name ID Format Error
        - ConfigError: Service Provider Metadata Format Error
        - ConfigError: Expression Name is missing in SAML Username Mapping
        - ConfigError: Authentication Context option error'
        - ValueError: Invalid argument. Please use semicolon separated string

        *Exceptions*
        - ConfigError: In order to add or edit SaaS applications, you must create at least one authentication realm
        - ConfigError: SaaS SSO Authentication Prompt settings error
        - ConfigError: Service Provider Name ID Format Error
        - ConfigError: Service Provider Metadata Format Error
        - ConfigError: Expression Name is missing in SAML Username Mapping
        - ConfigError: Authentication Context option error'
        - ValueError: Invalid argument. Please use semicolon separated string

        *Example*
        | @{METADATA} | test.com | Entity | https://host.com |
        | @{SAML_USERNAME_MAPPING} | Fixed Rule mapping | %s@example.com |
        | @{SAML_ATTR_MAPPING} | saml: ldap |
        | Saas Policies Add Saas Application | myAppPolicy |
        | ... | ${METADATA} |
        | ... | description=test saas app |
        | ... | auth_realm=test |
        | ... | saas_sso_authentication_prompt=Transparently sign in SaaS users |
        | ... | saml_username_mapping=${SAML_USERNAME_MAPPING} |
        | ... | saml_attribute_mapping=${SAML_ATTR_MAPPING} |
        | ... | authentication_context=TimeSyncToken |
        """
        self._open_page()

        # check if SaaS is preconfigured
        self._check_configuration_avaliability()

        self._click_add_application_button()
        self.input_text("//input[@id='id']", name)

        if sp_metadata is not None:
            self._fill_metadata(sp_metadata)

        # fill description if it is specified
        if description is not None:
            self.input_text("//textarea[@id='description']", description)

        # select Auth Realm if specified
        if auth_realm is not None:
            self.select_from_list('id=auth_sequence',
                                  '%s' % auth_realm)

        # select SaaS SSO Authentication Prompt settings
        # by default it is 'Always prompt SaaS users for proxy authentication'
        if saas_sso_authentication_prompt is not None:
            self._select_authentication_prompt(saas_sso_authentication_prompt)

        # select SAML Username Mapping if specified
        # default value: No mapping
        if saml_username_mapping is not None:
            self._select_saml_username_mapping(saml_username_mapping)

        # input SAML Attribute Mapping
        if saml_attribute_mapping is not None:
            self._fill_saml_attribute_mapping(saml_attribute_mapping)

        # select Authentication Context.
        # default value: Automatic
        if authentication_context is not None:
            self._select_authentication_context(authentication_context)

        # submit
        self._click_submit_button()

        self._click_next_button()

    def saas_policies_edit_saas_application(self,
                                            name,
                                            sp_metadata,
                                            description=None,
                                            auth_realm=None,
                                            saas_sso_authentication_prompt=None,
                                            saml_username_mapping=None,
                                            saml_attribute_mapping=None,
                                            authentication_context=None
                                            ):
        """Edit SaaS Application.

        Use this method to edit a SaaS Application Authentication Policy.

        *Parameters*
        - `name`: name to identify the SaaS application. String. Mandatory.
        - `sp_metadata`: metadata that describes the service provider referenced
        in this policy group. List. Should contain 1 or 3 elements. 1 element if
        you want to upload a metadata file provided by the SaaS application. In
        This case list element represents path to metadata file. Otherwise 3
        elements of the list contain the following values:
        _Service Provider Entity ID_ - (typically string in URI format) the SaaS
        application uses to identify itself as a service provider.
        _Name ID Format_ - format the appliance should use to identify users in
        the SAML assertion it sends to service providers. Possible values:
        'X509SubjectName', 'Kerberos', 'Unspecified', 'Entity', 'Transient',
        'EmailAddress', 'WindowsDomainNameQualifiedName'.
        _Assertion Consumer Service Location_ - string that contains URL to
        where the Web Security appliance should send the SAML assertion it
        creates.
        - `description`: description for this SaaS application. String.
        - `auth_realm`: contains authentication realm or authentication
        sequence the Web Proxy should use to authenticate users
        accessing this SaaS application. String. Optional.
        - `saas_sso_authentication_prompt`: choose whether to allow users to
        transparently sign into the SaaS application using their local
        authentication credentials, or to always prompt users for their
        credentials when accessing the SaaS application. String.
        Either `Prompt` or 'Transparently' or 'Automatically'.
        - `saml_username_mapping`: Specify how the Web Proxy should represent user
        names to the service provider in the SAML assertion. List with 2
        elements. First element represents one of methods:  'No mapping',
        'LDAP query', 'Fixed Rule mapping'. Second element used when method is
        'LDAP query' or 'Fixed Rule mapping'. It represents expression used
        with selected method.
        - `saml_attribute_mapping`: information about the internal users from the
        LDAP authentication server if required by the SaaS application. List
        with strings that contain pairs of values separated by semicolon. (LDAP
        attribute mapped to a SAML attribute). Optional.
        - `authentication_context`: contains one of values:
        'SecureRemotePassword', 'InternetProtocolPassword',
        'AuthenticatedTelephony', 'Unspecified', 'PreviousSession',
        'MobileTwoFactorUnregistered', 'MobileTwoFactorContract', 'Kerberos',
        'Public Key - XMLDSig', 'MobileOneFactorContract', 'Public Key - X.509',
        'MobileOneFactorUnregistered', 'TLSClient', 'Automatic', 'SoftwarePKI',
        'PasswordProtectedTransport', 'Public Key - SPKI', 'Password',
        'Smartcard', 'PersonalTelephony', 'InternetProtocol', 'Telephony',
        'Public Key - PGP', 'SmartcardPKI', 'NomadTelephony', 'TimeSyncToken'.

        Example:
        | @{ALT_METADATA} | %{SARF_HOME}/variables/sp_metadata.xml |
        | @{ALT_SAML_USERNAME_MAPPING} | LDAP query | <user>@<domain>.com. |
        | @{ALT_SAML_ATTR_MAPPING} | aaa: bbb | ccc: ddd |

        Exceptions:
        - ConfigError: In order to add or edit SaaS applications, you must create at least one authentication realm
        - ConfigError: SaaS SSO Authentication Prompt settings error
        - ConfigError: Service Provider Name ID Format Error
        - ConfigError: Service Provider Metadata Format Error
        - ConfigError: Expression Name is missing in SAML Username Mapping
        - ConfigError: Authentication Context option error'
        - ValueError: Invalid argument. Please use semicolon separated string

        | Saas Policies Edit Saas Application | myAppPolicy |
        | ... | ${ALT_METADATA} |
        | ... | description=test saas app |
        | ... | auth_realm=test |
        | ... | saas_sso_authentication_prompt=Transparently sign in SaaS users |
        | ... | saml_username_mapping=${ALT_SAML_USERNAME_MAPPING} |
        | ... | saml_attribute_mapping=${ALT_SAML_ATTR_MAPPING} |
        | ... | authentication_context=TimeSyncToken |
        """
        self._open_page()

        # get app policy status
        is_enabled = self._is_app_enabled(name)

        self._click_edit_application(name)

        # if disabled enable it first.
        if not is_enabled:
            self._enable_saas_application_checkbox()

        if sp_metadata is not None:
            self._fill_metadata(sp_metadata)

        # fill description if it is specified
        if description is not None:
            self.input_text("//textarea[@id='description']", description)

        # select Auth Realm if specified
        if auth_realm is not None:
            self.select_from_list('id=auth_sequence',
                                  '%s' % auth_realm)

        # select SaaS SSO Authentication Prompt settings
        if saas_sso_authentication_prompt is not None:
            self._select_authentication_prompt(saas_sso_authentication_prompt)

        # select SAML Username Mapping if specified
        if saml_username_mapping is not None:
            self._select_saml_username_mapping(saml_username_mapping)

        # input SAML Attribute Mapping
        if saml_attribute_mapping is not None:
            self._delete_attribute_mapping()
            self._fill_saml_attribute_mapping(saml_attribute_mapping)

        # select Authentication Context.
        if authentication_context is not None:
            self._select_authentication_context(authentication_context)

        # submit
        self._click_submit_button()

        self._click_next_button()

    def saas_policies_delete_saas_application(self, name):
        """Delete SaaS Application.

        Use this method to delete SaaS Application Authentication Policy.

        :Parameters:
        - `name`: The name of SaaS Application to be deleted. String.
        Mandatory.

        Exceptions:
        - GuiControlNotFoundError:xxx

        Example:
        | Saas Policies Delete Saas Application | myAppName |
        """

        self._open_page()
        self._click_delete_application(name)

    def saas_policies_get_list(self):
        """Gets a list of policies.

        Parameters:
        None

        Example:
        | @{ListResult} | SaaS Policies Get List |
        """
        ENTRY_POLICIES = lambda row, col:\
            '//table[@class=\'cols\']/tbody/tr[%s]/td[%d]' % (str(row), col)

        self._info('saas_policies_get_list')
        self._open_page()

        entries = {}
        num_of_entries = int(self.get_matching_xpath_count(ENTRY_POLICIES('*', 1))) + 2
        for row in xrange(2, num_of_entries):
            name = self.get_text(ENTRY_POLICIES(row, 1))
            description = self.get_text(ENTRY_POLICIES(row, 2))
            users = self.get_text(ENTRY_POLICIES(row, 3))
            url = self.get_text(ENTRY_POLICIES(row, 4))
            entries[name] = [description, users, url]
        return entries

    def _convert_semicolon_separated_string_to_tuple(self, user_input):
        if isinstance(user_input, (str, unicode)):
            user_input = tuple([item.strip() for item in user_input.split(':')])
        else:
            raise ValueError('Invalid argument. Please use semicolon' + \
                             ' separated string.')
        return user_input
    def saas_policies_edit_saas_application_user_and_groups(self,
        name=None,
        user=None,
        select_all=None,
        groups_add=None,
        groups_remove=None,
        ):
        """Saas Policies Edit Saas Application User And Groups

        Parameters:

        - `name`: Name of SaaS Application to be edited.
        - `user`: Authorized Users
        - `select_all`: yes or no. If yes, select all authenticated users
           if no, select group and users
        - `groups_add` - list of groups to be added
        - `groups_remove` - list of groups to be removed

        Examples:
        | Saas Policies Edit Saas Application User And Groups |
        | ... | name=myRealm    |
        | ... | user=rtestuser, user2, user3  |
        | ... | select_all=no |
        | ... | groups_add=AD1\\Account Operators, AD1\\Allowed RODC Password Replication Group |
        | ... | groups_remove=AD1\\Account Operators |

        | Saas Policies Edit Saas Application User And Groups |
        | ... | name=myRealm    |
        | ... | select_all=yes |
        """
        if not name:
            raise ValueError('Invalid argument.You have to specify value' + \
                             'for name argument.')
        if user == 'all': # for backward compatibility
            user = None
            select_all = 'yes'
        elif user:
            select_all = 'no'
        self._open_page()
        self._check_configuration_avaliability()
        self._click_on_all_authenticated_users_link(name=name)
        self._select_all(select_all)
        self._select_users(user)
        self._select_groups(groups_add, groups_remove)
        self._click_submit_button()

    def _select_all(self, select_all):
        RADIO_MAP = {
            "yes" : "//* [@id='all_auth']",
            "no"  : "//* [@id='selected_auth']",
        }

        if select_all:
            if select_all in RADIO_MAP.keys():
                self._wait_until_element_is_present(RADIO_MAP[select_all], 5)
                self._click_radio_button(RADIO_MAP[select_all])
            else:
                self._warn('Invalid parameter select_all=' + str(select_all) +\
                ' should be in ' + str(RADIO_MAP.keys()))

    def _select_users(self, user):
        USERS_LINK = "//* [@id='auth_users_link']"
        USERS_FIELD = "//* [@id='members_username']"
        if user:
            if self._is_visible(USERS_LINK):
                self.click_element(USERS_LINK)
                self.wait_until_page_loaded(timeout=30)
                self.input_text(USERS_FIELD, user)
                self._click_done_button()
            else:
                self._warn("Can't enter users because link " + USERS_LINK + \
                    " is not visible")

    def _select_groups(self, groups_add, groups_remove):
        GROUPS_LINK = "//* [@id='auth_groups_link']"
        if (groups_add or groups_remove):
            if self._is_visible(GROUPS_LINK):
                self.click_element(GROUPS_LINK)
                self.wait_until_page_loaded()
                self._handle_groups('add', groups_add)
                self._handle_groups('remove', groups_remove)
                self._click_done_button()
            else:
                self._warn("Can't enter groups because link " + GROUPS_LINK + \
                    " is not visible")

    def _handle_groups(self, action, groups):
        _timeout = 10
        _map = {
            "add": ("//select [@id='auth_group_list']",
                    "//input [@id='add_member_button']"),
            "remove": ("//select [@id='members_auth_group']",
                       "//input [@id='remove_member_button']"),
        }
        if groups:
            lis = [mem.strip() for mem in groups.split(',')]
            self.select_from_list(_map[action][0], *lis)
            self.click_element(_map[action][1], "don't wait")
