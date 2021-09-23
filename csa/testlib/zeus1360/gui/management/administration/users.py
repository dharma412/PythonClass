# $Id: //prod/main/sarf_centos/testlib/zeus1360/gui/management/administration/users.py#4 $
# $DateTime: 2020/04/01 03:33:13 $
# $Author: vsugumar $

import re
import time
import common.gui.guiexceptions as guiexceptions
import common.Variables

from common.gui.decorators import go_to_page
from common.gui.guicommon import GuiCommon
from users_def.extauth_devops_settings import ExtAuthDevopsSettings

GROUP_ROW_ID = 'ldap_groups_mapping_row'
SERVER_ROW_ID = 'service_hosts_row'
GROUP_ROW_PATTERN = 'ldap_groups_mapping\[(\d+)\]\[group_name\]'
SERVER_ROW_PATTERN = 'service_hosts\[(\d+)\]\[host\]'
GROUP_TBODY_ROW = '//tbody[@id=\'ldap_groups_mapping_rowContainer\']/tr'
GROUP_ROW = lambda index, info_type: 'xpath=//input[@id=\'ldap_groups_mapping[%s][%s]\']' % (index, info_type)
GROUP_SELECT_BOX = lambda index: 'ldap_groups_mapping[%s][role]' % (index,)
SERVER_ADD_ROW_BUTTON = 'service_hosts_domtable_AddRow'
GROUP_ADD_ROW_BUTTON = 'ldap_groups_mapping_domtable_AddRow'

ADD_USER_BUTTON = 'xpath=//input[@value=\'Add User...\']'
USERS_TABLE = '//table[@class=\'cols\']'
USERS_TABLE_ROW = '%s//tr' % (USERS_TABLE,)
USER_DATA_CELL = lambda row, column: '%s//tr[%s]//td[%s]' % (USERS_TABLE, row, column)
USERNAME_CELL_TEXT = lambda row: USER_DATA_CELL(row, 2)
FULLNAME_CELL_TEXT = lambda row: USER_DATA_CELL(row, 3)
USER_ROLE_CELL_TEXT = lambda row: USER_DATA_CELL(row, 4)
STATUS_CELL_TEXT = lambda row: USER_DATA_CELL(row, 5)
EXPIRATION_CELL_TEXT = lambda row: USER_DATA_CELL(row, 6)
EDIT_USER_LINK = lambda index: '%s//tr[%s]//td[2]/a' % (USERS_TABLE, index)
DELETE_USER_LINK = lambda index: '%s//tr[%s]//td[last()]/img' % (USERS_TABLE, index)
USERNAME_TEXTBOX = 'name=userName'
FULLNAME_TEXTBOX = 'name=fullName'
PREDEFINED_ROLE_RADIOBUTTON = 'id=role_predefined'
PREDEFINED_ROLES_LIST = 'id=group'
CUSTOM_ROLE_RADIOBUTTON = 'id=role_custom'
CUSTOM_ROLES_LIST = 'id=custom_role'
CONFIRM_PWD_TEXT= 'name=old_pwd'
PASSWORD_TEXTBOXES = ('name=passwdv', 'name=repasswd')
LOCK_ACCOUNT_BUTTON = 'xpath=//input[@value=\'Lock Account\']'
UNLOCK_ACCOUNT_BUTTON = 'xpath=//input[@value=\'Unlock Account\']'
CONFIRM_DLG = 'xpath=//div[@id="confirmation_dialog"]'
CONFIRM_BTN ='xpath=//div[@id="confirmation_dialog"]//button[text()="Continue"]'

ENABLE_EXTAUTH_BUTTON = 'xpath=//input[@value=\'Enable...\']'
EXT_AUTH_CUSTOMER_ENABLE_BUTTON = "//input[@value='Enable...' and @id='user']"
EXT_AUTH_CUSTOMER_EDIT_BUTTON = "//input[@value='Edit Global Settings...' and @id='user']"
EXT_AUTH_DEVOPS_ENABLE_BUTTON = "//input[@value='Enable...' and @id='devops']"
EXT_AUTH_DEVOPS_EDIT_BUTTON = "//input[@value='Edit Global Settings...' and @id='devops']"
SAML_EXT_AUTH_ATTRIBUTE_MAP ="//textarea[@id='extauth_group_attribute']"


EDIT_GLOBAL_SETTINGS_BUTTON = 'xpath=//input[@value=\'Edit Global Settings...\']'
EDIT_SECOND_SETTINGS_BUTTON = 'xpath=//input[@value=\'Edit Settings...\' and @type=\'button\']'

#MATCHED_CONTENT_VISIBILITY_CHECKBOX = 'matched_content_visibility'
DLP_TRACKING_PRIVILEGE_ROLES = ('admin', 'operators', 'readonly', 'emailadmin', 'helpdesk')
DLP_TRACKING_PRIVILEGE_MAP = lambda role:\
                'xpath=//input[@name="matched_content_visibility[]" and @value="%s"]' % (role,)

ENABLE_EXTAUTH_CHECKBOX = 'id=extauth_enabled'
AUTH_TYPES_LIST = 'id=ext_auth'
EXT_AUTH_CACHE_TIMEOUT_TEXTBOX = 'xpath=//input[@id=\'extauth_cache_timeout\']'
MAPPING_TBODY_ROW = '//tbody[@id="ldap_groups_mapping_rowContainer"]/tr'
ADD_MAPPING_ROW_BUTTON = 'id=ldap_groups_mapping_domtable_AddRow'
DELETE_MAPPING_ROW_LINK = lambda index:\
                '//tr[@id="ldap_groups_mapping_row%s"]/td[3]/img' % (index,)
MAPPING_GROUP_TEXTBOX = lambda index:\
                        'id=ldap_groups_mapping[%s][group_name]' % (index,)
MAPPING_ROLE_LIST = lambda index: 'id=ldap_groups_mapping[%s][role]' % (index,)
LIST_LABEL = lambda label: 'label=%s' % (label,)
MAP_TO_ADMIN_RADIOBUTTON = 'id=groups_enabled_false'
MAP_TO_ROLES_RADIOBUTTON = 'id=groups_enabled_true'

LDAP_AUTH_QUERY_LIST = 'id=query'
RESPONSE_TIMEOUT_TEXTBOX = 'id=timeout'

RADIUS_SERVER_ROW = lambda index, info_type:\
                    'id=service_hosts[%s][%s]' % (index, info_type)
RADIUS_SERVERS_TBODY_ROW = '//tbody[@id=\'service_hosts_rowContainer\']/tr'
DELETE_SERVER_ROW_LINK = lambda index:\
                         '//tr[@id=\'service_hosts_row%s\']/td[5]/img' % (index,)
ADD_SERVER_ROW_BUTTON = 'id=service_hosts_domtable_AddRow'
PROTOCOL_SELECT_BOX = lambda index: 'service_hosts[%s][auth_type]' % (index,)

# locators for account locking settings
ENABLE_FAILED_LOGIN_CHECKBOX = 'enable_failed_login_lock'
FAILED_LOGIN_ATTEMPTS_TEXTBOX = 'account_lock_threshold'
DISPLAY_LOCK_MSG_CHECKBOX = 'display_account_locked_message'
LOCK_MSG_TEXTBOX = 'account_locked_message'

# locators for password reset settings
ADMIN_CHANGE_RESET_CHECKBOX = 'force_pw_change_on_admin_reset'
ENABLE_PW_EXP_CHECKBOX = 'enable_password_expiration'
PW_EXP_PERIOD_TEXTBOX = 'password_expiration_period'
DISPLAY_PW_EXP_REMINDER_CHECKBOX = 'enable_password_expiration_warning'
PW_EXP_REMINDER_TEXTBOX = 'password_expiration_warning_period'

# locators for password rules settings
PWD_REQ_MIN_CHARS_TEXTBOX = 'password_min_length'
PWD_REQ_ALPHA_CHECKBOX = 'password_require_upper_lower'
PWD_REQ_NUMBER_CHECKBOX = 'password_require_numeric_char'
PWD_REQ_SPEC_CHECKBOX = 'password_require_special_char'
PWD_BAN_USERNAME_CHECKBOX = 'password_no_username_resemblance'
PWD_BAN_PWD_REUSE_CHECKBOX = 'password_reject_recent'
PWD_BAN_RECENT_TEXTBOX = 'password_num_recent_rejected'

ENTRY_USER_LINK = lambda row,col: '//table[@class=\'cols\']/tbody/tr[%s]/td[%d]' % (row,col,)
ENTRY_USER_SETTINGS = 'dl[@class=\'box\' and contains(dt, \'Settings\')]/dd'
ENTRY_USER_EXTERNAL_AUTHENTICATION = 'dl[@class=\'box\' and contains(dt, \'External Authentication\')]/dd'
ENTRY_USER_TABLE_LINK_EXTUSER = lambda table_name,row,col: '//%s/table[@class=\'pairs\']/tbody/tr[%s]/td[%d]' % (table_name,row,col,)
ENTRY_USER_NAME_LINK_EXTUSER  = lambda table_name,row: '//%s/table[@class=\'pairs\']/tbody/tr[%s]/th[1]' % (table_name,row,)
ENTRY_USER_VALUE_LINK_EXTUSER  = lambda table_name,row: '//%s/table[@class=\'pairs\']/tbody/tr[%s]/td[1]' % (table_name,row,)
ENTRY_USER_DLP = 'dl[@class=\'box\' and contains(dt, \'Tracking Privileges\')]/dd'
ENTRY_USER_TABLE_LINK = lambda table_name,table: '//%s/table[%s]/tbody/tr/th' % (table_name,table,)
ENTRY_USER_NAME_LINK  = lambda table_name,row: '//%s/table[%s]/tbody/tr/th[1]' % (table_name,row,)
ENTRY_USER_VALUE_LINK  = lambda table_name,row: '//%s/table[%s]/tbody/tr/td[1]' % (table_name,row,)

PAGE_PATH = ('Management', 'System Administration', 'Users')

class Users(GuiCommon):
    """Users Settings page interaction class.
    'System Administration -> Users' section.
    """

    def get_keyword_names(self):

        return ['users_add_user',
                'users_edit_user',
                'users_delete_user',
                'users_edit_external_authentication',
                'users_disable_external_authentication',

                'users_external_auth_devops_is_enabled',
                'users_external_auth_devops_enable',
                'users_external_auth_devops_edit',
                'users_external_auth_devops_disable',

                'users_edit_account_locking',
                'users_lock_account',
                'users_unlock_account',
                'users_edit_reset_rules',
                'users_edit_password_rules',
                'users_edit_dlp_tracking_privileges',
                'users_get_list',
                'users_get_settings',
                'users_get_external_authentication',
                'users_get_dlp_tracking_privileges']

    def _open_page(self):
        self._navigate_to('Management', 'System Administration', 'Users')

    def _get_ext_auth_devops_controller(self):
        if not hasattr(self, '_ext_auth_devops_controller'):
            self._ext_auth_devops_controller = ExtAuthDevopsSettings(self)
        return self._ext_auth_devops_controller

    def _click_add_user_button(self):
        self.click_button(ADD_USER_BUTTON)

    def _fill_username_textbox(self, name):
        self.input_text(USERNAME_TEXTBOX, text=name)

    def _fill_fullname_textbox(self, name):
        self.input_text(FULLNAME_TEXTBOX, text=name)

    def _get_predefined_roles(self):
        return self.get_list_items(PREDEFINED_ROLES_LIST)

    def _get_custom_roles(self):
        if self._is_element_present(CUSTOM_ROLES_LIST):
            return self.get_list_items(CUSTOM_ROLES_LIST)
        return []

    def _set_user_role(self, user_role):
        predefined_roles = self._get_predefined_roles()
        custom_roles = self._get_custom_roles()

        if user_role in predefined_roles:
            self._click_radio_button(PREDEFINED_ROLE_RADIOBUTTON)
            self.select_from_list(PREDEFINED_ROLES_LIST, LIST_LABEL(user_role))
        elif user_role in custom_roles:
            self._click_radio_button(CUSTOM_ROLE_RADIOBUTTON)
            self.select_from_list(CUSTOM_ROLES_LIST, LIST_LABEL(user_role))
        else:
            raise ValueError('"%s" user role does not exist' % (user_role,))

    def _fill_password_textbox(self, password, generate_passphrase):
        RADIO_BUTTON_GENERATE='sys_gen'
        RADIO_BUTTON_MANUAL='manual'
        RADIO_BUTTON_CHANGE='change'
        BUTTON_GENERATE="//input[@value, 'Generate']"

        if generate_passphrase is not None and str(generate_passphrase).lower() == 'y':
            self._click_radio_button(RADIO_BUTTON_GENERATE)
            self.click_button(BUTTON_GENERATE)

        else:
            if self._is_element_present(RADIO_BUTTON_CHANGE):
                self._click_radio_button(RADIO_BUTTON_CHANGE)
            if self._is_element_present(RADIO_BUTTON_MANUAL):
                self._click_radio_button(RADIO_BUTTON_MANUAL)
            for field in PASSWORD_TEXTBOXES:
                self.input_text(field, text=password)

    def _get_user_row_index(self, username):
        table_rows = int(self.get_matching_xpath_count(USERS_TABLE_ROW))

        for index in xrange(2, table_rows+1):
            name = self.get_text(USERNAME_CELL_TEXT(index))
            if name == username:
                return index
        else:
            return None

    def _click_edit_user_link(self, username):
        row_index = self._get_user_row_index(username)
        if row_index is None:
            raise ValueError('"%s" user does not exist' % (username,))

        self.click_element(EDIT_USER_LINK(row_index))

    def _click_delete_user_link(self, username):
        row_index = self._get_user_row_index(username)
        if row_index is None:
            raise ValueError('"%s" user does not exist' % (username,))

        self.click_element(DELETE_USER_LINK(row_index), "don't wait")
        self._click_continue_button()

    def _add_table_rows(self, num_of_rows, add_row_button):
        for i in xrange(num_of_rows):
            self.click_button(add_row_button, "don't wait")

    def _delete_table_rows(self, num_of_rows, del_row_button, row_id_patt):
        current_rows = self._get_table_rows_ids(row_id_patt)

        for i in xrange(num_of_rows):
            self.click_element(del_row_button(current_rows[i]), "don't wait")

    def _get_table_rows_ids(self, patt):
        fields_nums = []
        field_patt = re.compile(patt)
        text_fields = self._get_all_fields()

        for field in text_fields:
            result = field_patt.search(field)
            if result:
                fields_nums.append(result.group(1))

        return fields_nums

    def _setup_table(self, num_of_rows, table_row_loc, add_row_button,
                     del_row_button, row_id_patt):
        num_of_entries = int(self.get_matching_xpath_count(table_row_loc))
        rows_diff = num_of_rows - num_of_entries
        if rows_diff < 0:
            self._delete_table_rows(abs(rows_diff), del_row_button, row_id_patt)
        elif rows_diff > 0:
            self._add_table_rows(rows_diff, add_row_button)

    def _is_extauth_enabled(self):
        if self._is_element_present(EDIT_GLOBAL_SETTINGS_BUTTON):
            return True
        return False

    def _get_current_auth_type(self):
        return self.get_value(AUTH_TYPES_LIST).upper()

    def _click_enable_extauth_button(self):
        self.click_button(ENABLE_EXTAUTH_BUTTON)

    def _click_edit_global_settings_button(self):
        self.click_button(EDIT_GLOBAL_SETTINGS_BUTTON)

    def _uncheck_extauth_checkbox(self):
        if self._is_checked(ENABLE_EXTAUTH_CHECKBOX):
            self.unselect_checkbox(ENABLE_EXTAUTH_CHECKBOX)

    def _select_auth_type(self, auth_type):
        self.select_from_list(AUTH_TYPES_LIST, LIST_LABEL(auth_type))

    def _fill_radius_server_row(self, server, index):
        for entry, link in zip(
            (server[0], server[1], server[2], server[3],),
            ('host', 'port', 'shared_secret', 'timeout')):
            self.input_text(RADIUS_SERVER_ROW(index, link), entry)
            if len(server) == 5:
                value = server[4].lower()
            else:
                value = 'pap'
            protocol_option = "value=%s" % (value,)
            self.select_from_list(PROTOCOL_SELECT_BOX(index),
            protocol_option)

    def _select_radius_auth_type(self, auth_type, locator):
        if auth_type is not None:
            auth_types = self.get_list_items(locator)
            if auth_type.upper() not in auth_types:
                raise ValueError('"%s" auth type for RADIUS is not valid' %\
                                 (auth_type,))
            self.select_from_list(locator, LIST_LABEL(auth_type.upper()))

    def _set_table(self, num_of_rows, table):
        if table == 'groups':
            entry_row = GROUP_TBODY_ROW
            add_button = GROUP_ADD_ROW_BUTTON
            row_id = GROUP_ROW_ID
            delete_column = 3
        elif table == 'servers':
            entry_row = RADIUS_SERVERS_TBODY_ROW
            add_button = ADD_SERVER_ROW_BUTTON
            row_id = SERVER_ROW_ID
            delete_column = 6
        else:
            raise ValueError('Value should be either groups or servers')

        num_of_entries = int(self.get_matching_xpath_count(entry_row))
        rows_diff = num_of_rows - num_of_entries
        if rows_diff < 0:
           self._delete_table_rows(row_id=row_id,
                        num_of_rows=abs(rows_diff),
                        delete_column=delete_column)
        elif rows_diff > 0:
            self._add_table_rows(rows_diff, add_button)

    def _fill_radius_servers_table(self, servers):
        if servers is not None:
            self._set_table(len(servers), 'servers')
            row_ids = self._get_table_rows_ids(SERVER_ROW_PATTERN)
            for server, index in zip(servers, row_ids):
                self._fill_radius_server_row(server, index)

    def _set_groups_state(self, groups):
        if groups is not None:
            groups = tuple([tuple(item.split(':'))\
                    for item in self._convert_to_tuple(groups)])

            self._set_table(len(groups), 'groups')
            row_ids = self._get_table_rows_ids(GROUP_ROW_PATTERN)

            for group, index in zip(groups, row_ids):
                self._fill_group_mapping_row(group, index)
        else:
            return

    def _fill_extauth_cache_timeout_textbox(self, timeout):
        if timeout is not None:
            self.input_text(EXT_AUTH_CACHE_TIMEOUT_TEXTBOX, text=timeout)

    def _fill_response_timeout_textbox(self, timeout):
        if timeout is not None:
            self.input_text(RESPONSE_TIMEOUT_TEXTBOX, timeout)

    def _is_ldap_query_configured(self):
        return self._is_element_present(LDAP_AUTH_QUERY_LIST)

    def _select_ldap_auth_query(self, query):
        if not self._is_ldap_query_configured():
            raise guiexceptions.ConfigError(
                    'At least one ldap query must be configured')

        if query is None:
            return

        ldap_queries = self.get_list_items(LDAP_AUTH_QUERY_LIST)
        if query not in ldap_queries:
            raise ValueError('"%s" ldap query does not exist' % (query,))
        self.select_from_list(LDAP_AUTH_QUERY_LIST, LIST_LABEL(query))

    def _fill_group_mapping_table(self, mapping):
        if mapping is None:
            return

        table_entry_patt = 'ldap_groups_mapping\[(\d+)\]\[group_name\]'
        self._setup_table(len(mapping),
                          MAPPING_TBODY_ROW,
                          ADD_MAPPING_ROW_BUTTON,
                          DELETE_MAPPING_ROW_LINK,
                          table_entry_patt)

        row_ids = self._get_table_rows_ids(table_entry_patt)
        for group_name, index in zip(mapping, row_ids):
            self._fill_group_mapping_row(group_name, mapping[group_name], index)

    def _fill_group_mapping_row(self, group, index):
        for entry, link in zip((group[0],), ('group_name',)):
            self.input_text(GROUP_ROW(index, link), entry)
            self.select_from_list(GROUP_SELECT_BOX(index), group[1])

    def _edit_account_rules(self, rules_edit_method, *args):
        self._open_page()

        self._click_edit_settings_button()

        rules_edit_method(*args)

        self._click_submit_button(wait=False, skip_wait_for_title=True,\
                    accept_confirm_dialog=True)

    def _select_checkbox_value(self, locator, value, text_locator=None):
        if value:
            self.click_element(locator, "don't wait")
            if (text_locator is not None) and (not isinstance(value, bool)):
                self.input_text(text_locator, value)
        elif value is not None:
            self.unselect_checkbox(locator)

    def _edit_account_locking_rules(self, lock_failed_login, display_message):
        for locator, value, text_locator in (
            (ENABLE_FAILED_LOGIN_CHECKBOX, lock_failed_login, FAILED_LOGIN_ATTEMPTS_TEXTBOX),
            (DISPLAY_LOCK_MSG_CHECKBOX, display_message, LOCK_MSG_TEXTBOX)):
            self._select_checkbox_value(locator, value, text_locator)

    def _edit_account_reset_rules(self, admin_change, password_expiration, display_reminder):
        for locator, value, text_locator in (
            (ADMIN_CHANGE_RESET_CHECKBOX, admin_change, None),
            (ENABLE_PW_EXP_CHECKBOX, password_expiration, PW_EXP_PERIOD_TEXTBOX)
            ):
            self._select_checkbox_value(locator, value, text_locator)

        if display_reminder and \
            not self._is_checked(ENABLE_PW_EXP_CHECKBOX):
            raise guiexceptions.ConfigError('Password expiration must be enabled to '\
                    'use expiration reminder')

        self._select_checkbox_value(DISPLAY_PW_EXP_REMINDER_CHECKBOX,
            display_reminder, PW_EXP_REMINDER_TEXTBOX)

    def _edit_account_password_rules(self, req_min_chars, req_alpha, req_number,
        req_special_char, ban_username, ban_reuse):
        if req_min_chars:
            self.input_text(PWD_REQ_MIN_CHARS_TEXTBOX, req_min_chars)

        for locator, value, text_locator in (
            (PWD_REQ_ALPHA_CHECKBOX, req_alpha, None),
            (PWD_REQ_NUMBER_CHECKBOX, req_number, None),
            (PWD_REQ_SPEC_CHECKBOX, req_special_char, None),
            (PWD_BAN_USERNAME_CHECKBOX, ban_username, None),
            (PWD_BAN_PWD_REUSE_CHECKBOX, ban_reuse, PWD_BAN_RECENT_TEXTBOX)
            ):
            self._select_checkbox_value(locator, value, text_locator)

    def _fill_confirm_password_textbox(self):
        variables = common.Variables.get_variables()
        if variables.has_key("${DUT_ADMIN_SSW_PASSWORD}"):
            passwd = variables["${DUT_ADMIN_SSW_PASSWORD}"]
            self.input_text(CONFIRM_PWD_TEXT,passwd)

    def users_add_user(self, username, fullname, password, user_role=None, generate_passphrase=None):
        """Add new local user.

        Parameters:
            - `username`: name for the user.
            - `fullname`: full name for the user.
            - `password`: password for the user.
            - `user_role`: role of the user. If None, default value will be
              used.

        Examples:
            | Users Add User | user_name | full_user_name | user_password |
            | Users Add User | user_name | full_user_name | user_password | ${sma_user_roles.OPERATOR} |
        """
        self._open_page()

        self._click_add_user_button()

        self._fill_username_textbox(username)

        self._fill_fullname_textbox(fullname)

        if user_role is not None:
            self._set_user_role(user_role)

        if self._is_element_present(CONFIRM_PWD_TEXT):
            self._fill_confirm_password_textbox()

        self._fill_password_textbox(password,generate_passphrase)

        self._click_submit_button()

    def users_edit_user(self, username, fullname=None, password=None, user_role=None, generate_passphrase=None):
        """Edit existent local user.

        Parameters:
            - `username`: name of the user to edit.
            - `fullname`: new full name for the user. If None, fullname will
              not be changed.
            - `password`: new password for the user. If None, password will not
              be changed.
            - `user_role`: new role for the user. If None, value will not be
              changed.

        Examples:
            | Users Edit User  user_name | fullname=full_user_name | password=newpassword | user_role|=${sma_user_roles.RO_OPERATOR} |
        """
        self._open_page()

        self._click_edit_user_link(username)

        if fullname is not None:
            self._fill_fullname_textbox(fullname)

        if user_role is not None:
            self._set_user_role(user_role)

        if password is not None:
            self._fill_password_textbox(password,generate_passphrase)

        if self._is_element_present(CONFIRM_PWD_TEXT):
            self._fill_confirm_password_textbox()

        self._click_submit_button()

    def users_delete_user(self, username):
        """Delete local user.

        Parameters:
            - `username`: name of the user to delete.

        Examples:
            | Users Delete User | user_name |
        """
        self._open_page()

        self._click_delete_user_link(username)

    def users_edit_external_authentication(self, auth_type, radius_servers=None,
                          ldap_query=None, auth_cache_timeout=None,
                          group_mapping=None, response_timeout=None,
                          extauth_attribute_name_map=None):
        """Edit external authentication settings.

        Parameters:
            - `auth_type`: authentication type to use: 'LDAP' or 'RADIUS' or 'SAML'.
            - `radius_servers`: a string with comma separated values of
              radius_host:port:secret:timeout:protocol type.
              Existing RADIUS servers will be replaced with this
              configuration. If None, configuration will not be
              changed. Default protocol is 'PAP'. Applies only if `auth_type`
              is 'Radius'.
            - `ldap_query`: name of the LDAP authentication query to use. If
              None, default value will be used. Applies only if `auth_type` is
              'LDAP'.
            - `auth_cache_timeout`: number of seconds for the appliance to wait
              for a response from the server. If None, the value will be left
              unchanged.
            - `group_mapping`: a string with comma separated values of
              group_name:role. Specify mappping of externally authenticated
              users to different roles. If `auth_type` is 'RADIUS' value can be
              'Administaror' to specify mapping of all externally authenticated
              users to the Administrator role.
            - `response_timeout`: timeout to wait for valid response from
              server in seconds. If None, default value will be used. Applies
              only if `auth_type` is 'LDAP'.
            - 'extauth_attribute_name_map' :The Attribute Name and Value depends on what

        Examples:
            | Users Edit External Authentication | RADIUS | radius_servers=services1.wga:1812:ironport:10,services2.wga:1812:ironport:10|
            | Users Edit External Authentication  LDAP | ldap_query=test.externalauth | auth_cache_timeout=200 | group_mapping=Group3:administrator | response_timeout=6
 |

            | Users Edit External Authentication  SAML |
            ...  extauth_attribute_name_map=mailLocalAddress |
            ...  group_mapping= Helpdesk:Guest |

        Exceptions:
            - `ConfigError`: in case if external authentication is not enabled;
              in case if radius or ldap server is not specified.
            - `ValueError`: in case if auth_type is not equal LDAP or RADIUS
        """
        self._open_page()

        auth_enabled = self._is_extauth_enabled()

        if auth_enabled:
            self._click_edit_global_settings_button()
            current_auth_type = self._get_current_auth_type()
        else:
            self._click_enable_extauth_button()
            current_auth_type = auth_type

        if (not auth_enabled or auth_type != current_auth_type)  and (group_mapping is None):
            raise guiexceptions.ConfigError('Group mapping must be provided when external '\
                              'authentication is being enabled fo the first '\
                              'time or when changing auth type.')

        if auth_type == 'RADIUS':
            if (not auth_enabled or auth_type != current_auth_type) \
                and radius_servers is None:
                raise guiexceptions.ConfigError('At least one Radius server must be specified '\
                    'when external authentication is being enabled for the '\
                    'first time or when changing auth type.')

            self._select_auth_type(auth_type)

            if radius_servers is not None:
                radius_servers = tuple([tuple(item.split(':'))\
                        for item in self._convert_to_tuple(radius_servers)])

            self._fill_radius_servers_table(radius_servers)
            self._set_groups_state(group_mapping)

        elif auth_type == 'LDAP':
            self._select_auth_type(auth_type)

            self._select_ldap_auth_query(ldap_query)

            self._set_groups_state(group_mapping)

            self._fill_response_timeout_textbox(response_timeout)

        elif auth_type == 'SAML':
             self._select_auth_type(auth_type)
             self.input_text(SAML_EXT_AUTH_ATTRIBUTE_MAP,extauth_attribute_name_map)
             self._set_groups_state(group_mapping)

        else:
            raise ValueError('"%s" auth type is unknown' % (auth_type,))

        self._fill_extauth_cache_timeout_textbox(auth_cache_timeout)
        prev_timeout = self.set_selenium_timeout(60)
        try:
            prev_timeout = self.set_selenium_timeout(10)
            self._click_submit_button(accept_confirm_dialog=True, skip_wait_for_title=True)
        except Exception as e:
            self._click_continue_button()

        finally:
            self.set_selenium_timeout(prev_timeout)

    def users_disable_external_authentication(self):
        """Disable external authentication.

        Examples:
            | Users Disable External Authentication |
        """
        self._open_page()

        if self._is_extauth_enabled():

            self._click_edit_global_settings_button()

            self._uncheck_extauth_checkbox()
            self._handle_continue_on_submit()

    @go_to_page(PAGE_PATH)
    def users_external_auth_devops_is_enabled(self):
        """Get External Authentication state for Devops users.

        *Return:*
        - True or False depending on current state

        *Examples:*
        | ${ext_auth_devops_is_enabled}= | Users External Auth Devops Is Enabled |
        """
        return not self._is_element_present(EXT_AUTH_DEVOPS_ENABLE_BUTTON)

    @go_to_page(PAGE_PATH)
    def users_external_auth_devops_enable(self, settings):
        """
        Enable External Authentication for Devops users

        *Parameters:*
        - `settings`: dictionary containing External Authentication settings
        for Devops users. Possible items are:
        | `Authentication Type` | External Authentication type. Allowed value - SAML. Mandatory |
        | `External Authentication Attribute Name Map` | The Attribute Name and Value depends on what
        attributes have been configured on the Idp to be returned. Mandatory |
        | `Group Mapping` | dictionary containing external groups to local roles mapping. Mandatory. |

        *Examples:*
        | ${saml_group_mapping}=                           | Create Dictionary      |
        | ... | ${SAML_GROUP_ADMINS}                       | Administrator          |
        | ... | ${SAML_GROUP_OPERATORS}                    | Operator               |
        | Users External Auth Devops Enable                |                        |
        | ... | Authentication Type                        | SAML                   |
        | ... | External Authentication Attribute Name Map | mailRoutingAddress     |
        | ... | Group Mapping                              | ${saml_group_mapping}  |
        """
        self.click_button(EXT_AUTH_DEVOPS_ENABLE_BUTTON)
        self._get_ext_auth_devops_controller().set(settings)
        self._handle_continue_on_submit()

    @go_to_page(PAGE_PATH)
    def users_external_auth_devops_edit(self, settings):
        """
        Edit External Authentication for Devops users

        *Parameters:*
        - `settings`: dictionary containing External Authentication settings
        for Devops users. Possible items are:
        | `Authentication Type` | External Authentication type. Allowed value - SAML. Mandatory |
        | `External Authentication Attribute Name Map` | The Attribute Name and Value depends on what
        attributes have been configured on the Idp to be returned. Mandatory |
        | `Customize Strings to View Devops SSO Login` | ',' separated values to see Devops SSO button |
        | `Group Mapping` | dictionary containing external groups to local roles mapping. Mandatory. |

        *Examples:*
        | ${saml_group_mapping}=                           | Create Dictionary      |
        | ... | ${SAML_GROUP_HELPDESK                      | Helpdesk               |
        | ... | ${SAML_GROUP_GUEST}                        | Guest                  |
        | Users External Auth Devops Edit                  |                        |
        | ... | Authentication Type                        | SAML                   |
        | ... | External Authentication Attribute Name Map | mailLocalAddress       |
        | ... | Customize Strings to View Devops SSO Login | testuser,testsaml,test |
        | ... | Group Mapping                              | ${saml_group_mapping}  |
        """
        if not self.users_external_auth_devops_is_enabled():
            raise guiexceptions.ConfigError('External Authentication for Devops '\
                    'should be enabled in order to edit its settings')
        self.click_button(EXT_AUTH_DEVOPS_EDIT_BUTTON)
        self._get_ext_auth_devops_controller().set(settings)
        self._handle_continue_on_submit()

    @go_to_page(PAGE_PATH)
    def users_external_auth_devops_disable(self):
        """Disable External Authentication for Devops users.
        Will do nothing is the feature is already disabled

        *Examples:*
        | Users External Auth Devops Disable |
        """
        if self.users_external_auth_devops_is_enabled():
            self.click_button(EXT_AUTH_DEVOPS_EDIT_BUTTON)
            self._unselect_checkbox(ENABLE_EXTAUTH_CHECKBOX)
            self._handle_continue_on_submit()
        else:
            print '*DEBUG* External Authentication for DevOps is already disabled'

    def users_edit_account_locking(self, lock_failed_login=None, display_message=None):
        """Edit user account locking settings.

        Parameters:
            - `lock_failed_login`: lock the user account after the user fails
              to login successfully. Boolean. Integer to specify the custom
              number of failed login attempts that cause the account locking.
            - `display_message`: display locked account message if administrator
              has manually locked a user account. Boolean. String to enable and
              set custom message.

        Examples:
            | Users Edit Account Locking | lock_failed_login=15 | display_message=test |
        """
        self._edit_account_rules(self._edit_account_locking_rules,
            lock_failed_login, display_message)

    def users_edit_reset_rules(self, admin_change=None, password_expiration=None,
        display_reminder=None):
        """Edit password reset settings.

        Parameters:
            - `admin_change`: require a password reset whenever a user's
              password is set or changed by an admin. Boolean.
            - `password_expiration`: enable password expiration. Boolean.
              Integer to set custom number of days a password can last.
            - `display_reminder`: display a notification about the upcoming
              password expiration. Boolean. Integer to set custom number of
              days before expiration to notify users.

        Examples:
            | Users Edit Reset Rules | admin_change=on | password_expiration=10 | display_reminder=5 |

        Exceptions:
            - `ConfigError`: in case if try to enable expiration reminder when password
              expiration is disabled
        """
        self._edit_account_rules(self._edit_account_reset_rules, admin_change,
            password_expiration, display_reminder)

    def users_edit_password_rules(self, req_min_chars=None, req_alpha=None,
        req_number=None, req_special_char=None, ban_username=None,
        ban_reuse=None):
        """Edit password rules settings.

        Parameters:
            - `req_min_chars`: minimum number of characters passwords may
              contain. Integer.
            - `req_alpha`: require at least one upper and lower case letter.
              Boolean.
            - `req_number`: require at least one number. Boolean.
            - `req_special_char`: require at least one special character.
              Boolean.
            - `ban_username`: ban usernames and their variations as passwords.
            - `ban_reuse`: ban reuse of the last passwords. Boolean. Integer
              to set custom number of last passwords.

        Examples:
            | Users Edit Password Rules | req_min_chars=20 | req_alpha=on | req_number=off | req_special_char=on | ban_username=on |ban_reuse=10 |
        """

        self._edit_account_rules(self._edit_account_password_rules,
            req_min_chars, req_alpha, req_number, req_special_char,
            ban_username, ban_reuse)

    def users_edit_dlp_tracking_privileges(self, dlp_tracking_privileges=None,
        admin=None, operators=None, readonly=None, emailadmin=None, helpdesk=None):
        """Edit DLP Tracking Privileges

        Parameters:
            - `dlp_tracking_privileges`: Allow access to DLP Matched Content
              in Message Tracking results. Boolean.
              If this argument defined additional arguments will be ignored (legacy behavior).
              If this argument is set to true then tracking privileges will be enabled
              for all user categories and othenwise if argument is set to false
              no user categories will have tracking privileges.
            - `admin`: Allow users with Administrators role
                to have access to DLP Matched Content
            - `operators`: Allow users with Operators role
                to have access to DLP Matched Content
            - `readonly`: Allow users with Read-Only Operators role
                to have access to DLP Matched Content
            - `emailadmin`: Allow users with Email Administrators role
                to have access to DLP Matched Content
            - `helpdesk`: Allow users with Help Desk Users role
                to have access to DLP Matched Content

        Examples:
            | Users Edit DLP Tracking Privileges | dlp_tracking_privileges=${True} |
            | Users Edit DLP Tracking Privileges | dlp_tracking_privileges=${False} |
            | Users Edit DLP Tracking Privileges |
            | ... | admin=${True} |
            | ... | operators=${False} |
            | ... | readonly=${True} |
            | ... | emailadmin=${False} |
            | ... | helpdesk=${True} |
        """

        self._open_page()

        self.click_button(EDIT_SECOND_SETTINGS_BUTTON)

        if dlp_tracking_privileges is not None:
            for role in DLP_TRACKING_PRIVILEGE_ROLES:
                self._set_checkbox(dlp_tracking_privileges,
                    DLP_TRACKING_PRIVILEGE_MAP(role),)
        else:
            locals_dict = locals()
            for role in DLP_TRACKING_PRIVILEGE_ROLES:
                if locals_dict[role] is not None:
                    self._set_checkbox(locals_dict[role],
                        DLP_TRACKING_PRIVILEGE_MAP(role))


        self._click_submit_button()

    def users_get_list(self):
        """Get users list.

        *Parameters:*
            None

        *Return:*
            This keyword returns:
            'username':['full name', 'user role', 'account status', 'password expires']

        *Examples:*
            | ${UsersList} | Users Get List |

        Exceptions:
            None
        """
        self._info('users_get_list')
        self._open_page()
        entries = {}
        num_of_entries = int(self.get_matching_xpath_count(ENTRY_USER_LINK('*', 1)))
        for row in xrange(2, num_of_entries + 2):
            user_name = self.get_text(ENTRY_USER_LINK(row,2))
            full_name = self.get_text(ENTRY_USER_LINK(row,3))
            user_role = self.get_text(ENTRY_USER_LINK(row,4))
            account_status = self.get_text(ENTRY_USER_LINK(row,5))
            password_expires = self.get_text(ENTRY_USER_LINK(row,6))
            entries[user_name]=[full_name, user_role,
                account_status, password_expires]

        return entries

    def _get_list_of_table(self, xpath_table):
        entries = {}
        num_of_entries = int(self.get_matching_xpath_count(ENTRY_USER_TABLE_LINK(xpath_table, '*')))
        print '_get_list_of_table: num(%s)' % (str(num_of_entries))
        for row in xrange(1, num_of_entries+1):
            print '_get_list_of_table: row(%s)' % (str(row))
            field_name  = self.get_text(ENTRY_USER_NAME_LINK(xpath_table, row))
            field_value = self.get_text(ENTRY_USER_VALUE_LINK(xpath_table, row))
            entries[field_name] = field_value
        return entries

    def _get_list_of_table_external(self, xpath_table):
        entries = {}
        num_of_entries = int(self.get_matching_xpath_count(ENTRY_USER_TABLE_LINK_EXTUSER(xpath_table, '*', 1)))
        print '_get_list_of_table: num(%s)' % (str(num_of_entries))
        if self._is_element_present(EXT_AUTH_CUSTOMER_EDIT_BUTTON) and self._is_element_present(EXT_AUTH_DEVOPS_EDIT_BUTTON):
             num_of_entries = num_of_entries+1
        for row in xrange(1, num_of_entries):
             print '_get_list_of_table: row(%s)' % (str(row))
             field_name  = self.get_text(ENTRY_USER_NAME_LINK_EXTUSER(xpath_table, row))
             field_value = self.get_text(ENTRY_USER_VALUE_LINK_EXTUSER(xpath_table, row))
             entries[field_name] = field_value
        return entries

    def users_get_settings(self):
        """Get local user account & password settings

        *Parameters:*
            None

        *Return:*
            This keyword returns dictionary:
            - 'field name':'field value'

        *Examples:*
            | ${Settings} | Users Get Settings |
        """
        self._info('users_get_settings')
        self._open_page()
        return self._get_list_of_table(ENTRY_USER_SETTINGS)

    def users_get_external_authentication(self):
        """Get configuration of external authentication

        *Parameters:*
            None

        *Return:*
            This keyword returns:
            - dictionary with 'field name':'field value' when external authentication is enabled;
            - empty dictionary when external authentication is disabled.

        *Examples:*
            | ${ExtAuthen} | Users Get External Authentication |
        """
        self._info('users_get_list')
        self._open_page()
        if self._is_text_present('External Authentication is disabled.') and self._is_element_present(EXT_AUTH_CUSTOMER_ENABLE_BUTTON) and self._is_element_present(EXT_AUTH_DEVOPS_ENABLE_BUTTON):
            return {}
        else:
            return self._get_list_of_table_external(ENTRY_USER_EXTERNAL_AUTHENTICATION)

    def users_get_dlp_tracking_privileges(self):
        """Get configuration of DLP tracking privileges

        *Parameters:*
            None

        *Return:*
            This keyword returns dictionary:
            'field name':'field value'

        *Examples:*
            | ${DLPList} | Users Get DLP Tracking Privileges |

        Exceptions:
            None
        """
        self._info('users_get_list')
        self._open_page()
        return self._get_list_of_table(ENTRY_USER_DLP)

    def _click_lock_account_button(self):
        self.click_button(LOCK_ACCOUNT_BUTTON, "don't wait")
        time.sleep(5) # to avoid time races
        if self._is_visible(CONFIRM_DLG):
            self._info('%s is found' % CONFIRM_DLG)
            self.click_button(CONFIRM_BTN)

    def _click_unlock_account_button(self):
        self.click_button(UNLOCK_ACCOUNT_BUTTON, "don't wait")

    def users_lock_account(self, username):
        """Lock existent local user account status.

        Parameters:
             - `username`: name of the user to lock.
        Examples:
            | Users Lock Account | user_name |
        """
        self._open_page()

        self._click_edit_user_link(username)

        if self._is_element_present(CONFIRM_PWD_TEXT):
            self._fill_confirm_password_textbox()

        self._click_lock_account_button()

    def users_unlock_account(self, username):
        """ Unlock existent local user account status.

        Parameters:
            - `username`: name of the user to unlock.
        Examples:
            | Users Unlock Account | user_name |
        """
        self._open_page()

        self._click_edit_user_link(username)
        if self._is_element_present(CONFIRM_PWD_TEXT):
            self._fill_confirm_password_textbox()

        self._click_unlock_account_button()

    def _handle_continue_on_submit(self):
        """ Handles continue button if it appears after submit"""

        try:
            prev_timeout = self.set_selenium_timeout(10)
            self._click_submit_button(accept_confirm_dialog=True, skip_wait_for_title=True)
        except Exception as e:
            self._click_continue_button()
        finally:
            self.set_selenium_timeout(prev_timeout)

