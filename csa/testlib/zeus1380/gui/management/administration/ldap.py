#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/gui/management/administration/ldap.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $


import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import (GuiCommon, Wait)


ADD_LDAP_SERVER_BUTTON = "//input[@value='Add LDAP Server Profile...']"
DELETE_ROW_BUTTON = lambda index: "//div//tr[%s]//img[@alt='Delete...']" %\
    (index,)
ADD_ROW_BUTTON = "//input[@value='Add Row']"

# LDAP Profiles table
LDAP_PROFILES_TABLE_CELL = lambda row, column:\
    "//table[@class='cols']/tbody/tr[%s]/td[%s]" % (row, column)
LDAP_PROFILES_TABLE_NAME_CELL = lambda row:\
    LDAP_PROFILES_TABLE_CELL(row, 1) + '/a'
LDAP_PROFILES_TABLE_DELETE_CELL = lambda row:\
    LDAP_PROFILES_TABLE_CELL(row, 5) + '/img'

# LDAP Server attributes section
LDAP_PROFILE_NAME_TEXTBOX = 'LDAPServerName'
LDAP_HOSTNAME_TEXTBOX = 'hostname'
LDAP_ANONYMOUS_AUTH_RADIOBUTTON = 'authtype_anon'
LDAP_PASS_AUTH_RADIOBUTTON = 'authtype_pass'
LDAP_AUTH_USER_TEXTBOX = 'auth_user'
LDAP_AUTH_PASS_TEXTBOX = 'auth_pass'
LDAP_SERVER_TYPE_LIST = 'server_type'
LDAP_PORT_TEXTBOX = 'port'
LDAP_BASE_DN_TEXTBOX = 'base'
LDAP_USE_SSL_CHECKBOX = 'use_ssl'
LDAP_CACHE_TTL_TEXTBOX = 'cache_ttl'
LDAP_MAX_ENTRIES_TEXTBOX = 'cache_size'
LDAP_MAX_CONN_TEXTBOX = 'max_connections'
LDAP_LOAD_BALANCE_RADIOBUTTON = 'load_balance'
LDAP_FAILOVER_RADIOBUTTON = 'failover'

# External LDAP authentication queries section
EXT_AUTH_ENABLE_CHECKBOX = 'externalauth_enable'
EXT_AUTH_NAME_TEXTBOX = 'externalauth_queryname'
EXT_AUTH_USER_BASEDN_TEXTBOX = 'externalauth_account_base'
EXT_AUTH_USER_QUERY_TEXTBOX = 'externalauth_user_query'
EXT_AUTH_FULL_NAME_TEXTBOX = 'externalauth_gecos_attribute'
EXT_AUTH_DENY_LOGIN = 'externalauth_deny_login'
EXT_AUTH_GROUP_BASEDN_TEXTBOX = 'externalauth_group_base'
EXT_AUTH_GROUP_QUERY_TEXTBOX = 'externalauth_membership_query'
EXT_AUTH_MEMBER_ATTR_TEXTBOX = 'externalauth_member_attribute'
EXT_AUTH_GROUP_ATTR_TEXTBOX = 'externalauth_group_name_attribute'

# ISQ end-user authentication query section
ISQ_AUTH_ENABLE_CHECKBOX = 'isqauth_enable'
ISQ_AUTH_NAME_TEXTBOX = 'isqauth_queryname'
ISQ_AUTH_ACTIVE_CHECKBOX = 'isqauth_active'
ISQ_AUTH_QUERY_TEXTBOX = 'isqauth_query'
ISQ_AUTH_EMAIL_ATTR_TEXTBOX = 'isqauth_mailattr'

# ISQ alias consolidation query section
ISQ_ALIAS_ENABLE_CHECKBOX = 'primaryaddress_enable'
ISQ_ALIAS_NAME_TEXTBOX = 'primaryaddress_queryname'
ISQ_ALIAS_ACTIVE_CHECKBOX = 'primaryaddress_active'
ISQ_ALIAS_QUERY_TEXTBOX = 'primaryaddress_query'
ISQ_ALIAS_EMAIL_ATTR_TEXTBOX = 'primaryaddress_mailattr'

# Domain assignments table
ADD_DOMAIN_ASSIGNMENTS_BUTTON = "//input[@value='Add Domain Assignments...']"
DOMAIN_ASSIGN_TABLE_EDIT_LINK = lambda name:\
    "//a[contains(@href, 'domain_queries') and "\
    "contains(@href, 'query_name=%s')]" %\
    (name,)
DOMAIN_ASSIGN_TABLE_DELETE_LINK = lambda name:\
    "//img[contains(@onclick, 'domain_queries') and contains(@onclick, '%s')]"\
    % (name,)
DOMAIN_ASSIGN_NAME_TEXTBOX = 'query_name'
DOMAIN_ASSIGN_QUERY_TYPE_LIST = 'query_type'
DOMAIN_ASSIGN_DEFAULT_QUERY_LIST= 'default_domain_query'
DOMAIN_ASSIGN_DOMAIN_TEXTBOX = lambda row:\
    'domain_assignments[%s][domain]' % (row,)
DOMAIN_ASSIGN_QUERY_LIST = lambda row:\
    'domain_assignments[%s][query]' % (row,)
ACTIVATE_QUERY_CHECKBOX = 'query_active'

# Chained queries table
ADD_CHAINED_QUERY_BUTTON = "//input[@value='Add Chained Query...']"
CHAINED_QUERIES_TABLE_EDIT_LINK = lambda name:\
    "//a[contains(@href, 'daisy_chains') and "\
    "contains(@href, 'query_name=%s')]" % (name,)
CHAINED_QUERIES_TABLE_DELETE_LINK = lambda name:\
    "//img[contains(@onclick, 'daisy_chains') and "\
    "contains(@onclick, 'query_name=%s')]" % (name,)
CHAINED_QUERIES_QUERY_LIST = lambda row: 'queries[%s][query]' % (row,)

LDAP_INTERFACES_LIST = 'interface'
FLUSH_CACHE_BUTTON = "//input[@value='Flush Cache']"

# LDAP server profile test
TEST_LDAP_PROFILE_BUTTON = 'server_testbtn'
TEST_LDAP_PROFILE_RESULT = "server_test_results"
TEST_LDAP_PROFILE_CLOSE_BUTTON = "//button[contains(text(), 'Close')]"

# LDAP external authentication test
TEST_LDAP_EXT_AUTH_USER_TEXTBOX = 'test_externalauth_user_login'
TEST_LDAP_EXT_AUTH_PASSWD_TEXTBOX = 'test_externalauth_password'
TEST_LDAP_EXT_AUTH_GROUP_TEXTBOX = 'test_externalauth_membership_login'
TEST_LDAP_EXT_AUTH_USER_BUTTON =\
"//input[@id='test_externalauth_start' and contains(@onclick, 'bind')]"
TEST_LDAP_EXT_AUTH_GROUP_BUTTON =\
"//input[@id='test_externalauth_start' and contains(@onclick, 'membership')]"
TEST_LDAP_EXT_AUTH_RESULT = 'externalauth_test_results'
TEST_LDAP_EXT_AUTH_CLOSE_BUTTON = "//div[@id='test_panel']//button[contains(text(), 'Cancel')]"
TEST_LDAP_EXT_AUTH_BUTTON = 'externalauth_testbtn'

# LDAP ISQ end user auth test
TEST_LDAP_ISQ_AUTH_BUTTON = 'isqauth_testbtn'
TEST_LDAP_ISQ_AUTH_RUN_BUTTON = 'test_isqauth_start'
TEST_LDAP_ISQ_AUTH_USER_TEXTBOX = 'test_isqauth_user'
TEST_LDAP_ISQ_AUTH_PASSWD_TEXTBOX = 'test_isqauth_pass'
TEST_LDAP_ISQ_AUTH_QUERY_TEXTBOX = 'test_isqauth_query'
TEST_LDAP_ISQ_AUTH_EMAIL_TEXTBOX = 'test_isqauth_mailattr'
TEST_LDAP_ISQ_AUTH_RESULT = 'isqauth_test_results'
TEST_LDAP_ISQ_AUTH_CLOSE_BUTTON = "//button[contains(text(), 'Cancel')]"

# LDAP alias consolidation test
TEST_LDAP_ALIAS_BUTTON = 'primaryaddress_testbtn'
TEST_LDAP_ALIAS_EMAIL_TEXTBOX = 'test_primaryaddress_mailaddr'
TEST_LDAP_ALIAS_QUERY_TEXTBOX = 'test_primaryaddress_query'
TEST_LDAP_ALIAS_EMAIL_ATTR_TEXTBOX = 'test_primaryaddress_mailattr'
TEST_LDAP_ALIAS_RUN_BUTTON = 'test_primaryaddress_start'
TEST_LDAP_ALIAS_RESULT = 'primaryaddress_test_results'
TEST_LDAP_ALIAS_CLOSE_BUTTON = "//button[contains(text(), 'Cancel')]"
ADVANCED_OPTION = '//*[@id="advancedLinkClosed"]'

class LDAP(GuiCommon):

    """Keywords for Management Appliance -> System Administration -> LDAP"""

    def get_keyword_names(self):
        return [
            'ldap_add_server_profile',
            'ldap_edit_server_profile',
            'ldap_delete_server_profile',
            'ldap_edit_external_authentication_queries',
            'ldap_disable_external_authentication_queries',
            'ldap_edit_isq_end_user_authentication_query',
            'ldap_disable_isq_end_user_authentication_query',
            'ldap_edit_isq_alias_consolidation_query',
            'ldap_disable_isq_alias_consolidation_query',
            'ldap_add_domain_based_query',
            'ldap_edit_domain_based_query',
            'ldap_delete_domain_based_query',
            'ldap_add_chained_query',
            'ldap_edit_chained_query',
            'ldap_delete_chained_query',
            'ldap_edit_global_settings',
            'ldap_flush_cache',
            'ldap_run_server_profile_test',
            'ldap_run_external_authentication_queries_test',
            'ldap_run_isq_end_user_authentication_query_test',
            'ldap_run_isq_alias_consolidation_query_test',
            ]

    def _open_page(self):
        self._navigate_to('Management', 'System Administration', 'LDAP')

    def _get_profile_row_index(self, name):
        err_msg = 'No LDAP Server Profiles Configured'
        if self._is_text_present(err_msg):
            raise guiexceptions.ConfigError(err_msg)

        num_of_rows = int(self.get_matching_xpath_count(
            LDAP_PROFILES_TABLE_NAME_CELL('*')))

        for index in range(2, num_of_rows + 2):
            if name == self.get_text(LDAP_PROFILES_TABLE_NAME_CELL(index)):
                return index
        else:
            raise ValueError('`%s` LDAP profile was not found on the page' %\
                (name,))

    def _click_edit_ldap_profile_link(self, name):
        row_index = self._get_profile_row_index(name)
        self.click_element(LDAP_PROFILES_TABLE_NAME_CELL(row_index))

    def _click_delete_ldap_profile_link(self, name):
        row_index = self._get_profile_row_index(name)
        self.click_element(LDAP_PROFILES_TABLE_DELETE_CELL(row_index),
            'dont wait')
        self._click_continue_button()

    def _select_auth_method(self, auth_method):
        if auth_method.lower() == 'anonymous':
            self._click_radio_button(LDAP_ANONYMOUS_AUTH_RADIOBUTTON)
        else:
            try:
                username, password = auth_method.split(':')
            except ValueError:
                raise ValueError('`auth_method` should be either `anonymous` '\
                    'or a string of colon-separated username and password. '\
                    'Got - `%s` instead' % (auth_method,))

            self._click_radio_button(LDAP_PASS_AUTH_RADIOBUTTON)
            self.input_text(LDAP_AUTH_USER_TEXTBOX, username)
            self.input_text(LDAP_AUTH_PASS_TEXTBOX, password)

    def _select_multiple_host_option(self, option):
        host_options = {
            'load-balancing': LDAP_LOAD_BALANCE_RADIOBUTTON,
            'failover': LDAP_FAILOVER_RADIOBUTTON
        }

        option_loc = host_options.get(option.lower())
        if option_loc is None:
            raise ValueError('Wrong `%s` value for multiple host option. '\
                'Possible values are - `%s`' %\
                (option, ', '.join(host_options.keys())))

        self._click_radio_button(option_loc)

    def _set_checkbox_value(self, locator, value):
        if value is None:
            return
        select_method = self.select_checkbox if value else\
            self.unselect_checkbox
        select_method(locator)

    def _fill_ldap_server_attributes(self, name, hostname, auth_method,
        server_type, port, base_dn, use_ssl, cache_ttl, max_entries,
        max_conn, mult_host_option):

        if name is not None:
            self.input_text(LDAP_PROFILE_NAME_TEXTBOX, name)

        if hostname is not None:
            self.input_text(LDAP_HOSTNAME_TEXTBOX, hostname)

        if auth_method is not None:
            self._select_auth_method(auth_method)

        if server_type is not None:
            self.select_from_list(LDAP_SERVER_TYPE_LIST, server_type)

        if port is not None:
            self.input_text(LDAP_PORT_TEXTBOX, port)

        if base_dn is not None:
            self.input_text(LDAP_BASE_DN_TEXTBOX, base_dn)

        if self._is_visible(ADVANCED_OPTION):
            self.click_element(ADVANCED_OPTION)

        self._set_checkbox_value(LDAP_USE_SSL_CHECKBOX, use_ssl)

        if cache_ttl is not None:
            self.input_text(LDAP_CACHE_TTL_TEXTBOX, cache_ttl)

        if max_entries is not None:
            self.input_text(LDAP_MAX_ENTRIES_TEXTBOX, max_entries)

        if max_conn is not None:
            self.input_text(LDAP_MAX_CONN_TEXTBOX, max_conn)

        if mult_host_option is not None:
            self._select_multiple_host_option(mult_host_option)

    def _disable_ldap_query(self, profile_name, query_checkbox):
        self._open_page()

        self._click_edit_ldap_profile_link(profile_name)

        if self._is_checked(query_checkbox):
            self.click_button(query_checkbox, 'dont wait')

        self._click_submit_button()

    def _fill_query_name(self, name):
        self.input_text(DOMAIN_ASSIGN_NAME_TEXTBOX, name)

    def _select_query_type(self, query_type):
        query_map = {'end-user': 'Spam Quarantine End-User Authentication',
                     'alias': 'Spam Quarantine Alias Consolidation'}

        query_item = query_map.get(query_type.lower())
        if query_item is None:
            raise ValueError('Query type should be one of %s' %\
                (', '.join(query_map.keys()),))

        self.select_from_list(DOMAIN_ASSIGN_QUERY_TYPE_LIST, query_item)

        # page is reloaded upon item selection
        self.wait_until_page_loaded()

    def _setup_table_rows(self, rows):
        num_of_rows = int(self.get_matching_xpath_count(
            DELETE_ROW_BUTTON('*')))
        rows_diff = num_of_rows - rows

        if rows_diff > 0:
            for i in range(rows_diff):
                self.click_element(DELETE_ROW_BUTTON('last()'), 'dont wait')
        elif rows_diff < 0:
            for i in range(abs(rows_diff)):
                self.click_button(ADD_ROW_BUTTON, 'dont wait')

    def _fill_domain_assignments_table(self, assignments):
        if assignments is None:
            return

        domain_assignments = self._convert_to_tuple(assignments)
        self._setup_table_rows(len(domain_assignments))

        for row, value in enumerate(domain_assignments):
            try:
                domain, query = value.split(':')
            except ValueError:
                raise ValueError(
                    'Domain assignment should be in `domain:query_name` '\
                    'format. Got `%s` instead' % (value,))

            self.input_text(DOMAIN_ASSIGN_DOMAIN_TEXTBOX(row), domain)
            self.select_from_list(DOMAIN_ASSIGN_QUERY_LIST(row), query)

    def _check_ability_to_edit_queries(self, locator, name):
        if not self._is_element_present(locator('')):
            raise guiexceptions.ConfigError('There are no configured queries')

        if not self._is_element_present(locator(name)):
            raise ValueError('`%s` query name is not present' % (name,))

    def _click_edit_query_link(self, link_locator, query_name):
        self._check_ability_to_edit_queries(link_locator, query_name)
        self.click_element(link_locator(query_name))

    def _click_delete_query_link(self, link_locator, query_name):
        self._check_ability_to_edit_queries(link_locator, query_name)
        self.click_element(link_locator(query_name), 'dont wait')
        self._click_continue_button()

    def _fill_chained_queries_table(self, queries):
        if queries is None:
            return

        queries_list = self._convert_to_tuple(queries)
        self._setup_table_rows(len(queries_list))

        for row, query in enumerate(queries_list):
            self.select_from_list(CHAINED_QUERIES_QUERY_LIST(row), query)

    def _check_ability_to_add_queries(self, err_msg):
        if self._is_text_present(err_msg):
            raise guiexceptions.ConfigError(
                'No LDAP profiles were configured.')

    def _click_add_domain_based_query_button(self):
        self._check_ability_to_add_queries(
            'Domain Assignments cannot be created')
        self.click_button(ADD_DOMAIN_ASSIGNMENTS_BUTTON)

    def _click_add_chained_query_button(self):
        self._check_ability_to_add_queries(
            'Chained Queries cannot be created')
        self.click_button(ADD_CHAINED_QUERY_BUTTON)

    def _select_default_domain_based_query(self, name):
        if name is not None:
            self.select_from_list(DOMAIN_ASSIGN_DEFAULT_QUERY_LIST, name)

    def _get_test_result(self, open_button, close_button, result_locator,
        select_options_method, *args):
        self.click_button(open_button, 'dont wait')

        if select_options_method is not None:
            select_options_method(*args)

        try:
            Wait(lambda: 'Connecting to LDAP' not in\
                self.get_text(result_locator),
                timeout=60, interval=3).wait()
        except guiexceptions.TimeoutError:
            pass
        finally:
            result = self.get_text(result_locator)
            self.click_button(close_button, 'dont wait')
            return result

    def _fill_ext_auth_test_options(self, query_type, login, password):
        if query_type.lower() == 'user':
            if password is None:
                raise guiexceptions.ConfigError('Password must be provided '\
                    'when testing user accounts query test')
            self.input_text(TEST_LDAP_EXT_AUTH_USER_TEXTBOX, login)
            self.input_text(TEST_LDAP_EXT_AUTH_PASSWD_TEXTBOX, password)
            self.click_button(TEST_LDAP_EXT_AUTH_USER_BUTTON, 'dont wait')
        elif query_type.lower() == 'group':
            self.input_text(TEST_LDAP_EXT_AUTH_GROUP_TEXTBOX, login)
            self.click_button(TEST_LDAP_EXT_AUTH_GROUP_BUTTON, 'dont wait')
        else:
            raise ValueError('Wrong `%s` value for query type' % (query_type,))

    def _fill_isq_end_user_auth_test_options(self, username, password,
        query_string, email_attrs):
        for locator, value in (
            (TEST_LDAP_ISQ_AUTH_USER_TEXTBOX, username),
            (TEST_LDAP_ISQ_AUTH_PASSWD_TEXTBOX, password),
            (TEST_LDAP_ISQ_AUTH_QUERY_TEXTBOX, query_string),
            (TEST_LDAP_ISQ_AUTH_EMAIL_TEXTBOX, email_attrs)):
            if value is not None:
                self.input_text(locator, value)

        self.click_button(TEST_LDAP_ISQ_AUTH_RUN_BUTTON, 'dont wait')

    def _fill_isq_alias_test_options(self, email, query_string, email_attr):
        for locator, value in (
            (TEST_LDAP_ALIAS_EMAIL_TEXTBOX, email),
            (TEST_LDAP_ALIAS_QUERY_TEXTBOX, query_string),
            (TEST_LDAP_ALIAS_EMAIL_ATTR_TEXTBOX, email_attr)):
            if value is not None:
                self.input_text(locator, value)
        self.click_button(TEST_LDAP_ALIAS_RUN_BUTTON, 'dont wait')

    def ldap_add_server_profile(self, profile_name, hostname, auth_method=None,
        server_type=None, port=None, base_dn=None, use_ssl=None,
        cache_ttl=None, max_entries=None, max_conn=None,
        mult_host_option=None):
        """Add LDAP server profile.

        Parameters:
        - `profile_name`: name for the server profile.
        - `hostname`: host name for the LDAP server. Either string of one host
           name value or a string of comma-separated host names.
        - `auth_method`: authentication method. 'anonymous' to use anonymous
           authentication or a string of colon-separated username and password.
        - `server_type`: LDAP server type.
        - `port`: port number to connect to.
        - `base_dn`: base DN for the LDAP server.
        - `use_ssl`: use SSL when communicating with the LDAP server. Boolean.
        - `cache_ttl`: the cache time-to-live.
        - `max_entries`: the maximum number of retained cache entries.
        - `max_conn`: the maximum number of simultaneous connections for each
           host.
        - `mult_host_option`: feature to use when connecting to multiple LDAP
           servers. Can be one of 'failover' or 'load-balancing'.


        Examples:
        | LDAP Add Server Profile | myldap | qa19.qa.sbr.ironport.com |
        | LDAP Add Server Profile | testldap | qa19.qa.sbr.ironport.com |
        | ... | testuser:ironport | OpenLDAP | 389 | dc=ironport, dc=com |
        | ... | ${True} | 10000 | 5000 | 7 |
        | LDAP Add Server Profile | two_ldaps |
        | ... | qa19.qa.sbr.ironport.com,sully.qa.sbr.ironport.com |
        | ... | anonymous | OpenLDAP | 389 | dc=ironport, dc=com |
        | ... | ${True} | 10000 | 5000 | 7 | load-balancing |

        Exceptions:
        - `ValueError`: in case of invalid `mult_host_option` or `auth_method`
           value.
        """
        self._open_page()

        self.click_button(ADD_LDAP_SERVER_BUTTON)

        self._fill_ldap_server_attributes(profile_name, hostname, auth_method,
            server_type, port, base_dn, use_ssl, cache_ttl, max_entries,
            max_conn, mult_host_option)

        self._click_submit_button()

    def ldap_edit_server_profile(self, profile_name, newname=None,
        hostname=None, auth_method=None, server_type=None, port=None,
        base_dn=None, use_ssl=None, cache_ttl=None, max_entries=None,
        max_conn=None, mult_host_option=None):
        """Edit LDAP server profile.

        Parameters:
        - `profile_name`: name of the server profile to edit.
        - `newname`: new name for the LDAP server profile.
        - `hostname`: host name for the LDAP server. Either string of one host
           name value or a string of comma-separated host names.
        - `auth_method`: authentication method. 'anonymous' to use anonymous
           authentication or a string of colon-separated username and password.
        - `server_type`: LDAP server type.
        - `port`: port number to connect to.
        - `base_dn`: base DN for the LDAP server.
        - `use_ssl`: use SSL when communicating with the LDAP server. Boolean.
        - `cache_ttl`: the cache time-to-live.
        - `max_entries`: the maximum number of retained cache entries.
        - `max_conn`: the maximum number of simultaneous connections for each
           host.
        - `mult_host_option`: feature to use when connecting to multiple LDAP
           servers. Can be one of 'failover' or 'load-balancing'.

        Examples:
        | LDAP Edit Server Profile | myldap |
        | ... | hostname=qa19.qa.sbr.ironport.com | auth_method=anonymous |
        | ... | use_ssl=${False} | max_conn=10 |
        | LDAP Edit Server Profile | myldap | hostname=windows-host.qa |
        | ... | server_type=Active Directory |

        Exceptions:
        - `ValueError`: in case of invalid `profile_name`, `mult_host_option`
           or `auth_method` value.
        - `ConfigError`: in case no LDAP server profiles were configured.
        """
        self._open_page()

        self._click_edit_ldap_profile_link(profile_name)

        self._fill_ldap_server_attributes(newname, hostname, auth_method,
            server_type, port, base_dn, use_ssl, cache_ttl, max_entries,
            max_conn, mult_host_option)

        self._click_submit_button()

    def ldap_delete_server_profile(self, profile_name):
        """Delete LDAP server profile.

        Parameters:
        - `profile_name`: name of the profile to delete.

        Examples:
        | LDAP Delete Server Profile | testLDAP |

        Exceptions:
        - `ValueError`: in case of invalid value for `profile_name`.
        - `ConfigError`: in case no LDAP server profiles were configured.
        """
        self._open_page()

        self._click_delete_ldap_profile_link(profile_name)

    def ldap_edit_external_authentication_queries(self, profile_name,
        query_name=None, user_base_dn=None, user_query=None,
        full_name_attr=None, deny_expired=None, group_base_dn=None,
        group_query=None, member_attr=None, group_attr=None):
        """Edit external LDAP authentication queries.

        Parameters:
        - `profile_name`: name of the LDAP server profile to edit queries for.
        - `query_name`: name for the query.
        - `user_base_dn`: base DN under which user records can be found.
        - `user_query`: query string for user records.
        - `full_name_attr`: user full name attribute.
        - `deny_expired`: deny login to expired accounts. Boolean.
        - `group_base_dn`: base DN under which group records can be found.
        - `group_query`: query string used to determine if a user is a
           member of a group.
        - `member_attr`: attribute that holds each member's username.
        - `group_attr`: attribute that contains the group name.

        Examples:
        | LDAP Edit External Authentication Queries | test_profile |
        | ... | new_query_name |
        | LDAP Edit External Authentication Queries | mytestprofile |
        | ... | extauthquery | dc=ironport,dc=com |
        | ... | (&(objectClass=posixAccount)(uid={u})) | gecos | ${True} |
        | ... | dc=ironport,dc=com |
        | ... | (&(objectClass=posixGroup)(memberUid={u})) | memberUid |
        | ... | cn |

        Exceptions:
        - `ValueError`: in case of invalid value for `profile_name`.
        - `ConfigError`: in case no LDAP server profiles were configured.
        """
        self._open_page()

        self._click_edit_ldap_profile_link(profile_name)

        if not self._is_checked(EXT_AUTH_ENABLE_CHECKBOX):
            self.click_button(EXT_AUTH_ENABLE_CHECKBOX, 'dont wait')

        for locator, value in\
            ((EXT_AUTH_NAME_TEXTBOX, query_name),
             (EXT_AUTH_USER_BASEDN_TEXTBOX, user_base_dn),
             (EXT_AUTH_USER_QUERY_TEXTBOX, user_query),
             (EXT_AUTH_FULL_NAME_TEXTBOX, full_name_attr),
             (EXT_AUTH_GROUP_BASEDN_TEXTBOX, group_base_dn),
             (EXT_AUTH_GROUP_QUERY_TEXTBOX, group_query),
             (EXT_AUTH_MEMBER_ATTR_TEXTBOX, member_attr),
             (EXT_AUTH_GROUP_ATTR_TEXTBOX, group_attr)):
             if value is not None:
                self.input_text(locator, value)

        self._set_checkbox_value(EXT_AUTH_DENY_LOGIN, deny_expired)

        self._click_submit_button()

    def ldap_disable_external_authentication_queries(self, profile_name):
        """Disable external LDAP authentication queries.

        Parameters:
        - `profile_name`: name of the LDAP server profile to disable queries
           for.

        Examples:
        | LDAP Disable External Authentication Queries | myProfile |

        Exceptions:
        - `ValueError`: in case of invalid value for `profile_name`.
        - `ConfigError`: in case no LDAP server profiles were configured.
        """
        self._disable_ldap_query(profile_name, EXT_AUTH_ENABLE_CHECKBOX)

    def ldap_edit_isq_end_user_authentication_query(self, profile_name,
        query_name=None, query_string=None, email_attrs=None,
        activate=None):
        """Edit spam quarantine end-user authentication query.

        Parameters:
        - `profile_name`: name of the LDAP server profile to edit query for.
        - `query_name`: name for the query.
        - `query_string`: LDAP query string.
        - `email_attrs`: email attributes. A string of one email attribute or
           a string of comma-separated values of email attributes.
        - `activate`: activate query. Boolean.

        Examples:
        | LDAP Edit ISQ End User Authentication Query | testLDAP |
        | ... | ldap_eu_auth | (uid={u}) | mail | ${True} |
        | LDAP Edit ISQ End User Authentication Query | testLDAP |
        | ... | email_attrs=mail,mail1 | activate=${False} |

        Exceptions:
        - `ValueError`: in case of invalid value for `profile_name`.
        - `ConfigError`: in case no LDAP server profiles were configured.
        """
        self._open_page()

        self._click_edit_ldap_profile_link(profile_name)

        if not self._is_checked(ISQ_AUTH_ENABLE_CHECKBOX):
            self.click_button(ISQ_AUTH_ENABLE_CHECKBOX, 'dont wait')

        for locator, value in\
            ((ISQ_AUTH_NAME_TEXTBOX, query_name),
             (ISQ_AUTH_QUERY_TEXTBOX, query_string),
             (ISQ_AUTH_EMAIL_ATTR_TEXTBOX,email_attrs)):
            if value is not None:
                self.input_text(locator, value)

        self._set_checkbox_value(ISQ_AUTH_ACTIVE_CHECKBOX, activate)

        self._click_submit_button()

    def ldap_disable_isq_end_user_authentication_query(self, profile_name):
        """Disable spam quarantine end-user authentication query.

        Parameters:
        - `profile_name`: name of the LDAP server profile to disable query for.

        Examples:
        | LDAP Disable ISQ End User Authentication Query | myProfile |

        Exceptions:
        - `ValueError`: in case of invalid value for `profile_name`.
        - `ConfigError`: in case no LDAP server profiles were configured.
        """
        self._disable_ldap_query(profile_name, ISQ_AUTH_ENABLE_CHECKBOX)

    def ldap_edit_isq_alias_consolidation_query(self, profile_name,
        query_name=None, query_string=None, email_attr=None, activate=None):
        """Edit spam quarantine alias consolidation query.

        Parameters:
        - `profile_name`: name of the LDAP server profile to edit query for.
        - `query_name`: name for the query.
        - `query_string`: LDAP query string.
        - `email_attr`: email attribute.
        - `activate`: activate query. Boolean.

        Examples:
        | LDAP Edit ISQ Alias Consolidation Query | test_profile |
        | LDAP Edit ISQ Alias Consolidation Query | LDAPprofile | alias_query |
        | ... | (mail={a}) | mail | ${True} |

        Exceptions:
        - `ValueError`: in case of invalid value for `profile_name`.
        - `ConfigError`: in case no LDAP server profiles were configured.
        """
        self._open_page()

        self._click_edit_ldap_profile_link(profile_name)

        if not self._is_checked(ISQ_ALIAS_ENABLE_CHECKBOX):
            self.click_button(ISQ_ALIAS_ENABLE_CHECKBOX, 'dont wait')

        for locator, value in\
            ((ISQ_ALIAS_NAME_TEXTBOX, query_name),
             (ISQ_ALIAS_QUERY_TEXTBOX, query_string),
             (ISQ_ALIAS_EMAIL_ATTR_TEXTBOX, email_attr)):
             if value is not None:
                self.input_text(locator, value)

        self._set_checkbox_value(ISQ_ALIAS_ACTIVE_CHECKBOX, activate)

        self._click_submit_button()

    def ldap_disable_isq_alias_consolidation_query(self, profile_name):
        """Disable qpam quarantine alias consolidation query.

        Parameters:
        - `profile_name`: name of the LDAP server profile to disable query for.

        Examples:
        | LDAP Disable ISQ Alias Consolidation Query | myProfile |

        Exceptions:
        - `ValueError`: in case of invalid value for `profile_name`.
        - `ConfigError`: in case no LDAP server profiles were configured.
        """
        self._disable_ldap_query(profile_name, ISQ_ALIAS_ENABLE_CHECKBOX)

    def ldap_add_domain_based_query(self, name, query_type, assignments,
        default=None, activate=None):
        """Add domain-based LDAP query.

        Parameters:
        - `name`: name for the domain-based query.
        - `query_type`: query type to select. Either 'end-user' to select
           'Spam Quarantine End-User Authentication' query or 'alias' to select
           'Spam Quarantine Alias Consolidation' query.
        - `assignments`: a string of comma-separated values of domain
           assignments in 'domain_name:queryname' format.
        - `default`: name of the default query to run if all other queries
           fail.
        - `activate`: designate as the active query. Boolean.

        Examples:
        | LDAP Add Domain Based Query | myquery | end-user |
        | ... | test.com:server1.query,domain.org:server2.query |
        | LDAP Add Domain Based Query | myquery | alias |
        | ... | mail.qa:ldapserver.isq_alias | ldap2.alias |
        | ... | ${True} |

        Exceptions:
        - `ValueError`: in case of invalid value for `query_type` or invalid
           value for `assignments`.
        - `ConfigError`: in case no LDAP profiles have been configured.
        """
        self._open_page()

        self._click_add_domain_based_query_button()

        self._select_query_type(query_type)

        self._fill_query_name(name)

        self._fill_domain_assignments_table(assignments)

        self._select_default_domain_based_query(default)

        self._set_checkbox_value(ACTIVATE_QUERY_CHECKBOX, activate)

        self._click_submit_button()

    def ldap_edit_domain_based_query(self, name, assignments=None,
        default=None, activate=None):
        """Edit domain-based LDAP query.

        Parameters:
        - `name`: name of the domain-based query to edit.
        - `assignments`: a string of comma-separated values of domain
           assignments in 'domain_name:queryname' format. Previous
           configuration will be wiped out.
        - `default`: name of the default query to run if all other queries
           fail.
        - `activate`: designate as the active query. Boolean.

        Examples:
        | LDAP Edit Domain Based Query | myquery |
        | ... | test.com:server1.query,domain.org:server2.query |
        | ... | server1.query | ${False} |
        | LDAP Edit Domain Based Query | myquery | ${None} |
        | ... | server2.query | ${True} |

        Exceptions:
        - `ValueError`: in case domain-based query is not present in the table
           or in case of invalid value for `assignments`.
        - `ConfigError`: in case no domain-based queries have been configured.
        """
        self._open_page()

        self._click_edit_query_link(DOMAIN_ASSIGN_TABLE_EDIT_LINK, name)

        self._fill_domain_assignments_table(assignments)

        self._select_default_domain_based_query(default)

        self._set_checkbox_value(ACTIVATE_QUERY_CHECKBOX, activate)

        self._click_submit_button()

    def ldap_delete_domain_based_query(self, name):
        """Delete domain-based LDAP query.

        Parameters:
        - `name`: name of the domain-based query to delete.

        Examples:
        | LDAP Delete Domain Based Query | testquery |

        Exceptions:
        - `ValueError`: in case domain-based query is not present in the table.
        - `ConfigError`: in case no domain-based queries have been configured.
        """
        self._open_page()

        self._click_delete_query_link(DOMAIN_ASSIGN_TABLE_DELETE_LINK, name)

    def ldap_add_chained_query(self, name, query_type, queries, activate=None):
        """Add chained LDAP query.

        Parameters:
        - `name`: name for the chained query.
        - `query_type`: query type to select. Either 'end-user' to select
           'Spam Quarantine End-User Authentication' query or 'alias' to select
           'Spam Quarantine Alias Consolidation' query.
        - `queries`: a string of comma-separated values of queries names to add
           to the chain.
        - `activate`: designate as active query. Boolean.

        Examples:
        | LDAP Add Chained Query | testquery | end-user |
        | ... | server1.query,server2.query | ${True} |
        | LDAP Add Chained Query | testquery | alias | ldap_server.isq_alias |
        | ... | ${False} |

        Exceptions:
        - `ValueError`: in case of invalid value for `query_type`.
        - `ConfigError`: in case no LDAP profiles have been configured.
        """
        self._open_page()

        self._click_add_chained_query_button()

        self._select_query_type(query_type)

        self._fill_query_name(name)

        self._fill_chained_queries_table(queries)

        self._set_checkbox_value(ACTIVATE_QUERY_CHECKBOX, activate)

        self._click_submit_button()

    def ldap_edit_chained_query(self, name, queries=None, activate=None):
        """Edit chained LDAP query.

        Parameters:
        - `name`: name of the chained query to edit.
        - `queries`: a string of comma-separated values of queries names to add
           to the chain. Previous configuration will be wiped out. ${None} to
           leave the chain unchanged.
        - `activate`: designate as active query. Boolean.

        Examples:
        | LDAP Edit Chained Query | testquery | ${None} | ${True} |
        | LDAP Edit Chained Query | testquery | server1.query,server2.query |

        Exceptions:
        - `ValueError`: in case chained query is not present in the table.
        - `ConfigError`: in case no chained queries have been configured.
        """
        self._open_page()

        self._click_edit_query_link(CHAINED_QUERIES_TABLE_EDIT_LINK, name)

        self._fill_chained_queries_table(queries)

        self._set_checkbox_value(ACTIVATE_QUERY_CHECKBOX, activate)

        self._click_submit_button()

    def ldap_delete_chained_query(self, name):
        """Delete chained LDAP query.

        Parameters:
        - `name`: name of the chained query to delete.

        Examples:
        | LDAP Delete Chained Query | testchain |

        Exceptions:
        - `ValueError`: in case chained query is not present in the table.
        - `ConfigError`: in case no chained queries have been configured.
        """
        self._open_page()

        self._click_delete_query_link(CHAINED_QUERIES_TABLE_DELETE_LINK, name)

    def ldap_edit_global_settings(self, interface=None):
        """Edit global LDAP settings.

        Parameters:
        - `interface`: interface to use for LDAP traffic.

        Examples:
        | LDAP Edit Global Settings | Management |
        | LDAP Edit Global Settings | Auto |
        """
        self._open_page()

        self._click_edit_settings_button()

        self.select_from_list(LDAP_INTERFACES_LIST, interface)

        self._click_submit_button()

    def ldap_flush_cache(self):
        """Flush LDAP cache.

        Examples:
        | LDAP Flush Cache |
        """
        self._open_page()

        self.click_button(FLUSH_CACHE_BUTTON, 'dont wait')

        self._click_continue_button()

    def ldap_run_server_profile_test(self, profile_name):
        """Test connection to the LDAP server(s).

        Parameters:
        - `profile_name`: name of the LDAP profile to run test against.

        Return:
        A string containing the result of the test.

        Examples:
        | ${test_result} = | LDAP Run Profile Server Test |

        Exception:
        - `ValueError`: in case of invalid `profile_name`.
        - `ConfigError`: in case no LDAP server profiles were configured.
        """
        self._open_page()

        self._click_edit_ldap_profile_link(profile_name)

        result = self._get_test_result(
            TEST_LDAP_PROFILE_BUTTON,
            TEST_LDAP_PROFILE_CLOSE_BUTTON,
            TEST_LDAP_PROFILE_RESULT,
            None)

        return result

    def ldap_run_external_authentication_queries_test(self, profile_name,
        query_type, login, password=None):
        """Test configured external authentication queries.

        Parameters:
        - `profile_name`: name of the LDAP profile to run test against.
        - `query_type`: query type to test. Can be either 'user' to test user
           accounts query or 'group' to test group membership query.
        - `login`: login to use for query test.
        - `password`: password to use for query test. Applies only if
          `query_type` is 'user'.

        Return:
        A string containing the result of the test.

        Examples:
        | ${test_result} = | LDAP Run External Authentication Queries Test |

        Exception:
        - `ValueError`: in case of invalid `profile_name` or `query_type`.
        - `ConfigError`: in case no LDAP server profiles were configured,
          `password` was not specified when doing user accounts query test or
          external authentication queries are not configured.
        """
        self._open_page()

        self._click_edit_ldap_profile_link(profile_name)

        if not self._is_checked(EXT_AUTH_ENABLE_CHECKBOX):
            raise guiexceptions.ConfigError(
                'External authentication query has to be enabled first')

        result =  self._get_test_result(
            TEST_LDAP_EXT_AUTH_BUTTON,
            TEST_LDAP_EXT_AUTH_CLOSE_BUTTON,
            TEST_LDAP_EXT_AUTH_RESULT,
            self._fill_ext_auth_test_options,
            query_type, login, password)

        return result

    def ldap_run_isq_end_user_authentication_query_test(self, profile_name,
        username, password, query_string=None, email_attrs=None):
        """Test configured spam quarantine end-user authetication query.

        Parameters:
        - `profile_name`: name of the LDAP profile to run test against.
        - `username`: user login to use for test.
        - `password`: user password to use for test.
        - `query_string`: LDAP query string.
        - `email_attrs`: email attributes. A string of one email attribute or
           a string of comma-separated values of email attributes.

        Return:
        A string containing the result of the test.

        Examples:
        | ${test_result} = | LDAP Run ISQ End User Authentication Query Test |

        Exception:
        - `ValueError`: in case of invalid `profile_name`.
        - `ConfigError`: in case no LDAP server profiles were configured.
        """
        self._open_page()

        self._click_edit_ldap_profile_link(profile_name)

        if not self._is_checked(ISQ_AUTH_ENABLE_CHECKBOX):
            raise guiexceptions.ConfigError(
                'ISQ end-user authentication query has to be enabled first')

        result = self._get_test_result(
            TEST_LDAP_ISQ_AUTH_BUTTON,
            TEST_LDAP_ISQ_AUTH_CLOSE_BUTTON,
            TEST_LDAP_ISQ_AUTH_RESULT,
            self._fill_isq_end_user_auth_test_options,
            username, password, query_string, email_attrs)

        return result

    def ldap_run_isq_alias_consolidation_query_test(self, profile_name, email,
        query_string=None, email_attr=None):
        """Test configured spam quarantine qlias consolidation query.

        Parameters:
        - `profile_name`: name of the LDAP profile to run test against.
        - `email`: email address to use for test.
        - `query_string`: LDAP query string.
        - `email_attr`: email attribute.

        Return:
        A string containing the result of the test.

        Examples:
        | ${test_result} = | LDAP Run ISQ Alias Consolidation Query Test |

        Exception:
        - `ValueError`: in case of invalid `profile_name`.
        - `ConfigError`: in case no LDAP server profiles were configured.

        """
        self._open_page()

        self._click_edit_ldap_profile_link(profile_name)

        if not self._is_checked(ISQ_ALIAS_ENABLE_CHECKBOX):
            raise guiexceptions.ConfigError(
                'ISQ alias consolidation query has to be enabled first')

        result = self._get_test_result(
            TEST_LDAP_ALIAS_BUTTON,
            TEST_LDAP_ALIAS_CLOSE_BUTTON,
            TEST_LDAP_ALIAS_RESULT,
            self._fill_isq_alias_test_options,
            email, query_string, email_attr)

        return result

