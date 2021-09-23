#!/usr/bin/env python
#$Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/users.py#2 $
#$DateTime: 2019/11/21 19:17:49 $
#$Author: uvelayut $

import re
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from sal.containers.yesnodefault import  is_yes

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
USERNAME_CELL_TEXT = lambda index: '%s//tr[%s]//td[2]' % (USERS_TABLE, index)
EDIT_USER_LINK = lambda index: '%s//tr[%s]//td[2]/a' % (USERS_TABLE, index)
DELETE_USER_LINK = lambda index: '%s//tr[%s]//td[7]/img' % (USERS_TABLE, index)
USERNAME_TEXTBOX = 'name=userName'
FULLNAME_TEXTBOX = 'name=fullName'
ADMIN_USER_GROUP = 'id=gr_admin'
OPERATOR_USER_GROUP = 'id=gr_operators'
READ_ONLY_OPERATOR_USER_GROUP = 'id=gr_readonly'
GUEST_USER_GROUP = 'id=gr_guest'
ENABLE_EXTAUTH_BUTTON = 'xpath=//input[@value=\'Enable...\']'
EDIT_GLOBAL_SETTINGS_BUTTON = 'xpath=//input[@value=\'Edit Global Settings...\']'
RADIUS_SERVER_ROW = lambda index, info_type:\
                    'xpath=//input[@id=\'service_hosts[%s][%s]\']' % (index, info_type)
RADIUS_SERVERS_TBODY_ROW = '//tbody[@id=\'service_hosts_rowContainer\']/tr'
DELETE_ROW_LINK = lambda row_id, index, column:\
                    '//tr[@id=\'%s%s\']/td[%s]/img' % (row_id, index, column,)
ADD_ROW_BUTTON = lambda button: 'id=%s' % (button,)
EXT_AUTH_CACHE_TIMEOUT_TEXTBOX = 'xpath=//input[@id=\'extauth_cache_timeout\']'
ENABLE_EXTAUTH_CHECKBOX = 'id=extauth_enabled'
PROTOCOL_SELECT_BOX = lambda index: 'service_hosts[%s][auth_type]' % (index,)

class Users(GuiCommon):
    """Users Settings page interaction class.
    'System Administration -> Users' section.
    """
    #Elements of passphrase expiration settings page
    ui_elements_passphrase_seetings = {
        "EDIT_SETTINGS" : "//input[@value='Edit Settings...']",
        "ENABLE_PASSWORD_EXPIRATION" : "//input[@id='enable_password_expiration']",
        "PASSWORD_EXPIRATION_PERIOD" : "//input[@id='password_expiration_period']",
        "ENABLE_PASSWORD_EXPIRATION_WARNING" : "//input[@id='enable_password_expiration_warning']",
        "PASSWORD_EXPIRATION_WARNING_PERIOD" : "//input[@id='password_expiration_warning_period']",
        "ENABLE_PASSWORD_GRACE" : "//input[@id='enable_password_grace']",
        "PASSWORD_GRACE_PERIOD" : "//input[@id='password_grace_period']"
    }

    def get_keyword_names(self):

        return ['users_add_user',
                'users_edit_user',
                'users_delete_user',
                'users_edit_external_authentication',
                'users_disable_external_authentication',
                'users_get_external_authentication_status',
                'users_edit_passphrase_expiration'  #Added as per SARF bug CSCuv13525
                ]
    #This method retrieves UI locators as per the specified key
    def _get_ui_element(self,ui_element):
        self._info("Getting the locator ... %s" %self.ui_elements_passphrase_seetings[ui_element])
        return self.ui_elements_passphrase_seetings[ui_element]

    def _open_page(self):
        self._navigate_to('System Administration', 'Users')

    def _click_add_user_button(self):
        self.click_button(ADD_USER_BUTTON)

    def _fill_username_textbox(self, name):
        self.input_text(USERNAME_TEXTBOX, text=name)

    def _fill_fullname_textbox(self, name):
        self._wait_until_element_is_present(FULLNAME_TEXTBOX)
        self.input_text(FULLNAME_TEXTBOX, text=name)

    def _set_user_type(self, user_type):

        user_types = {'administrator': ADMIN_USER_GROUP,
                      'operator': OPERATOR_USER_GROUP,
                      'read-only operator': READ_ONLY_OPERATOR_USER_GROUP,
                      'guest': GUEST_USER_GROUP}

        type_locator = user_types.get(user_type.lower())
        if type_locator is None:
            raise guiexceptions.ConfigError('"%s" user type does not exist' % (user_type,))
        self._click_radio_button(type_locator)

    def _set_groups_state(self, groups):
        GROUPS_DISABLE = "id=groups_enabled_false"
        GROUPS_ENABLE  = "id=groups_enabled_true"

        if groups is not None:
            if groups.lower() == 'off':
                if self._is_visible(GROUPS_DISABLE):
                    self._click_radio_button(GROUPS_DISABLE)
            else:
                if self._is_visible(GROUPS_ENABLE):
                    self._click_radio_button(GROUPS_ENABLE)

                groups = tuple([tuple(item.split(':'))\
                        for item in self._convert_to_tuple(groups)])

                self._set_table(len(groups), 'groups')
                row_ids = self._get_table_rows_ids(GROUP_ROW_PATTERN)

                for group, index in zip(groups, row_ids):
                    self._fill_group_mapping_row(group, index)

    def _fill_password_textbox(self, password):
        PASSWORD_TEXTBOXES = (
            'xpath=//input[@name="passwdv"]',
            'xpath=//input[@name="repasswd"]',
        )
        for field in PASSWORD_TEXTBOXES:
            self._wait_until_element_is_present(field)
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
            raise guiexceptions.ConfigError('"%s" user does not exist'\
                                            % (username,))

        self.click_element(EDIT_USER_LINK(row_index), "don't wait")

    def _click_delete_user_link(self, username):

        row_index = self._get_user_row_index(username)
        if row_index is None:
            raise guiexceptions.ConfigError('"%s" user does not exist'\
                                            % (username,))

        self.click_element(DELETE_USER_LINK(row_index), "don't wait")
        self._click_continue_button()

    def _is_extauth_enabled(self):

        if self._is_element_present(EDIT_GLOBAL_SETTINGS_BUTTON):
            return True
        return False

    def _click_enable_extauth_button(self):

        self.click_button(ENABLE_EXTAUTH_BUTTON)

    def _click_edit_global_settings_button(self):

        self.click_button(EDIT_GLOBAL_SETTINGS_BUTTON)

    def _uncheck_extauth_checkbox(self):

        self.unselect_checkbox(ENABLE_EXTAUTH_CHECKBOX)

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
            self.select_from_list(PROTOCOL_SELECT_BOX(index), protocol_option)

    def _fill_group_mapping_row(self, group, index):

        group_options = {'administrator': 'admin',
                         'operator': 'operators',
                         'read-only operator': 'readonly',
                         'guest': 'guest'}

        for entry, link in zip((group[0],), ('group_name',)):
            self.input_text(GROUP_ROW(index, link), entry)
            if len(group) == 2:
                value = group_options[group[1].lower()]
            else:
                value = group_options['administrator']
            group_option = "value=%s" % (value,)
            self.select_from_list(GROUP_SELECT_BOX(index), group_option)

    def _get_table_rows_ids(self, row_pattern):
        fields_nums = []
        field_patt = re.compile(row_pattern)
        text_fields = self._get_all_fields()
        for field in text_fields:
            result = field_patt.search(field)
            if result:
                fields_nums.append(result.group(1))
        return fields_nums

    def _add_table_rows(self, num_of_rows, button_id):

        for i in xrange(num_of_rows):
            self.click_button(ADD_ROW_BUTTON(button_id), "don't wait")

    def _delete_table_rows(self, num_of_rows, row_id, delete_column):

        for i in xrange(num_of_rows):
            self.click_element(DELETE_ROW_LINK(row_id, i, delete_column),\
                               "don't wait")

    def _set_table(self, num_of_rows, table):

        if table == 'groups':
            entry_row = GROUP_TBODY_ROW
            add_button = GROUP_ADD_ROW_BUTTON
            row_id = GROUP_ROW_ID
            delete_column = 3
        elif table == 'servers':
            entry_row = RADIUS_SERVERS_TBODY_ROW
            add_button = SERVER_ADD_ROW_BUTTON
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

    def _fill_extauth_cache_timeout_textbox(self, timeout):

        if timeout is not None:
            self.input_text(EXT_AUTH_CACHE_TIMEOUT_TEXTBOX, text=timeout)

    def users_add_user(self,
                       username,
                       fullname,
                       password=None,
                       user_type=None,
                       ):
        """Add new local user.

        Parameters:
        - `username`: name for the user. Should be lower case string.
        - `fullname`: full name for the user.
        - `generate`: yes or no. To auo generate password
        - `password`: password for the user. Mandatory.
        - `user_type`: type of the user. Correct values are: 'Administrator',
                    'Operator', 'Read-Only Operator', 'Guest'. If None,
                    user type will be set to default value - 'Administrator'.

        Example:
        | Users Add User | testname | Full Name | password=Password | user_type=Guest
        | Users Add User | testname | Full Name | generate=yes | user_type=Guest
        """
        self._open_page()
        self._click_add_user_button()
        self._fill_username_textbox(username.lower())
        self._fill_fullname_textbox(fullname)

        if user_type:
            self._set_user_type(user_type)

        if password:
            self._fill_password_textbox(password)
        else:
            raise guiexceptions.GuiValueError('Password is mandatory')
        self._click_submit_button()

    def users_edit_user(self,
                        username,
                        fullname=None,
                        password=None,
                        user_type=None,
                        ):
        """Edit existent local user.

        Parameters:
        - `username`: name of the user to edit.
        - `fullname`: new full name for the user. If None, fullname will
                          not be changed.
        - `password`: new password for the user. If None, password will not
                          be changed.
        - `user_type`: new type for the user. If None, value will not be
                           changed.
        - `generate`: yes or no. To auto generate password.

        Example:
        | Users Edit User | Full Name | Password | Operator |
        | Users Edit User | Full Name | Password | Administrator |
        | Users Edit User | User Name | Full Name | user_type=Guest | generate=yes |
        """
        self._open_page()
        self._click_edit_user_link(username.lower())

        if fullname:
            self._fill_fullname_textbox(fullname)

        if user_type:
            self._set_user_type(user_type)

        if password:
            self._fill_password_textbox(password)
        else:
            raise guiexceptions.GuiValueError('Full Name, User Type and Password are mandatory fields cant be empty')

        self._click_submit_button()

    def users_delete_user(self, username):
        """Delete local user.

        Parameters:
        - `username`: name of the user to delete.

        Example:
        | Users Delete User | testuser |
        """
        self._open_page()
        self._click_delete_user_link(username)

    def users_edit_external_authentication(self,
        radius_servers=None,
        timeout=None,
        groups=None,
        auth_type=None,
        ldap_ext_query=None,
        timeout_for_valid_response=None,
        ):
        """Edit external authentication settings.

        Parameters:
        - `radius_servers`: RADIUS Server Information
          a string with comma separated values of
          radius_host:port:secret:timeout:protocol type.
          Existing RADIUS servers will be replaced with this
          configuration. If None, configuration will not be
          changed. Default protocol is 'PAP'.
        - `timeout`: External Authentication Cache Timeout:
        - `groups`: a string with comma separated values of group_name:role
           type. group_name must be at least 3 symbols. Role should
           be one of 'Administrator', 'Operator', 'Guest',
           'Read-Only Operator'. Default role is 'Administrator'.
           If None, configuration will not be changed.
           String 'Off' to disable groups.
        - `auth_type`: RADIUS, LDAP, or None
        - `ldap_ext_query`: LDAP External Authentication Query
        - `timeout_for_valid_response`: Timeout To Wait For Valid Response
         From Server (inseconds)

        Example:
        | Users Edit External Authentication | radius_servers=server.wga:1812:ironport:10:chap |
        | Users Edit External Authentication | radius_servers=server.wga:1812:ironport:10:chap, example.wga:1812:ironport:20:pap |
        | Users Edit External Authentication | radius_servers=server.wga:1815:secret:10:pap | timeout=100 |
        | Users Edit External Authentication | radius_servers=server.wga:1815:secret:10:pap | groups=TestGroup:Administrator |
        | Users Edit External Authentication | radius_servers=server.wga:1812:ironport:10 | groups=TestGroup, NewGroup:Read-Only Operator |
        | Users Edit External Authentication | radius_servers=server.wga:1812:ironport:10 | groups=off |
        | Users Edit External Authentication | groups=off |
        """
        self._open_page()
        auth_enabled = self._is_extauth_enabled()
        if auth_enabled:
            self._click_edit_global_settings_button()
        else:
            self._click_enable_extauth_button()
        self._select_auth_type(auth_type)
        if radius_servers is not None:
            radius_servers = tuple([tuple(item.split(':'))\
                for item in self._convert_to_tuple(radius_servers)])
            self._fill_radius_servers_table(radius_servers)
        self._fill_extauth_cache_timeout_textbox(timeout)
        self._set_groups_state(groups)
        self._select_ldap_ext_query(ldap_ext_query)
        self._fill_timeout_for_valid_response(timeout_for_valid_response)
        self._click_submit_button(wait=False, skip_wait_for_title=True,\
            accept_confirm_dialog=None, check_result=False)

    def _select_auth_type(self, auth_type):
        LIST = '//select [@id="ext_auth"]'
        if auth_type:
            self.select_from_list(LIST, auth_type)

    def _select_ldap_ext_query(self, ldap_ext_query):
        LIST = '//select [@id="query"]'
        if ldap_ext_query:
            self.select_from_list(LIST, ldap_ext_query)

    def _fill_timeout_for_valid_response(self, timeout_for_valid_response):
        FIELD = 'xpath=//input [@id="timeout"]'
        self._input_text_if_not_none(FIELD, timeout_for_valid_response)

    def users_disable_external_authentication(self):
        """Disable external authentication.

        Example:
        | Users Disable External Authentication |
        """
        self._open_page()

        if not self._is_extauth_enabled():
            raise guiexceptions.ConfigError('External authentication has to be enabled first.')

        self._click_edit_global_settings_button()
        self._uncheck_extauth_checkbox()
        self._click_submit_button(wait=False, skip_wait_for_title=True,\
                                  accept_confirm_dialog=True)

    def users_get_external_authentication_status(self):
        """ Return External Authentication Status: True or False

        Example:
        ${result}=    Users Get External Authentication Status
        """
        TEXT = 'xpath=//th [text()= "External Authentication:"]/../td[text()="Enabled"]'
        self._open_page()

        return self._is_visible(TEXT) == True

    #Method to check state of passphrase expiration edit settings
    def _is_passphrase_settings_enabled(self):
        if self._is_element_present(self._get_ui_element('EDIT_SETTINGS')):
            return True
        return False

    #Method to click on passphrase edit settings button
    def _click_edit_passphrase_settings_button(self):
        if self._is_passphrase_settings_enabled():
           self.click_button(self._get_ui_element('EDIT_SETTINGS'))
        else:
            raise guiexceptions.GuiError('Edit Settings is disabled')

    #Method to set the specified passphrase expiration settings
    def _set_passpharse_settings(self, setting=None):
        if setting:
            #Split the string setting to get element, location and value
            setting_name, duration_input_element, duration_value = \
                                            setting.split('#')

            #If the element is not checked and user doesn't want to disable then set
            if not self._is_checked(setting_name) and duration_value != "disable":
                self.click_element(setting_name)
            self.input_text(duration_input_element, text=duration_value)

    #Method to disable specified setting
    def disable_setting(self, setting):
        #Disable the element only if enabled and checked
        if self._is_editable(setting) and self._is_checked(setting):
            self.click_element(setting)
            return

    #Keyword for setting passphrase expiration settings
    def users_edit_passphrase_expiration(self,
                                        expiration=None,
                                        reminder=None,
                                        grace_period=None):
        """ Configure users password expiration

        Example
        Users Edit Password Expiration
        ...  expiration=10
        ...  reminder=4
        ...  grace_period=disable
        """
        self._open_page()

        #Click passphrase expiration edit settings button
        self._click_edit_passphrase_settings_button()

        #Wait for passpharse settings are available
        self._wait_until_element_is_present(self._get_ui_element('ENABLE_PASSWORD_EXPIRATION'))

        if expiration == 'disable':
            #Disable passphrase expiration setting
            self.disable_setting(self._get_ui_element('ENABLE_PASSWORD_EXPIRATION'))
        elif expiration:
            self._info('Setting passphrase expiration')
            setting_values = [self._get_ui_element('ENABLE_PASSWORD_EXPIRATION'), \
                             self._get_ui_element('PASSWORD_EXPIRATION_PERIOD'),
                             expiration]
            setting = '#'.join(setting_values)
            self._info(setting)
            self._set_passpharse_settings(setting)

        if reminder == 'disable':
            #Disable passphrase expiration reminder setting
            self.disable_setting(self._get_ui_element('ENABLE_PASSWORD_EXPIRATION_WARNING'))
        elif reminder:
            self._info('Setting passphrase expiration warning')
            if self._is_checked(self._get_ui_element('ENABLE_PASSWORD_EXPIRATION')):
                 setting_values = [self._get_ui_element('ENABLE_PASSWORD_EXPIRATION_WARNING'), \
                             self._get_ui_element('PASSWORD_EXPIRATION_WARNING_PERIOD'),
                             reminder]
                 setting = '#'.join(setting_values)
                 self._info(setting)
                 self._set_passpharse_settings(setting)
            else:
		 raise guiexceptions.ConfigError('Password expiration is not set')

        if grace_period == 'disable':
            #Disable passphrase expiration grace period setting
            self.disable_setting(self._get_ui_element('ENABLE_PASSWORD_GRACE'))
        elif grace_period:
            self._info('Setting passphrase expiration grace period')
            if self._is_checked(self._get_ui_element('ENABLE_PASSWORD_EXPIRATION')):
                 setting_values = [self._get_ui_element('ENABLE_PASSWORD_GRACE'), \
                             self._get_ui_element('PASSWORD_GRACE_PERIOD'),
                             grace_period]
                 setting = '#'.join(setting_values)
                 self._info(setting)
                 self._set_passpharse_settings(setting)
            else:
                 raise guiexceptions.ConfigError('Password expiration is not set')

        #Click submit button after making the changes
        self._click_submit_button()
