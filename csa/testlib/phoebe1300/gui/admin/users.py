#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/admin/users.py#2 $
# $DateTime: 2019/08/13 22:20:55 $
# $Author: nthallap $

from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

from users_def.dlp_tracking_priv_settings import DlpTrackingPrivSettings
from users_def.sf_priv_settings import SecondFactorPrivSettings
from users_def.url_logging_priv_settings import UrlLoggingPrivSettings
from users_def.extauth_settings import ExtAuthSettings
from users_def.extauth_devops_settings import ExtAuthDevopsSettings
from users_def.sfauth_settings import SfAuthSettings
from users_def.password_and_account_settings import PasswordAndAccountSettings
from users_def.user_settings import UserSettings

ADD_USER_BUTTON = "//input[@value='Add User...']"
USERS_TABLE = "//table[@class='cols']"
USER_EDIT_LINK = lambda name: "%s//td/a[normalize-space()='%s']" % \
                              (USERS_TABLE, name)
USER_DELETE_LINK = lambda name: "%s//td[normalize-space()='%s']" \
                                "/following-sibling::td[5]/img" % \
                                (USERS_TABLE, name)
CONTROL_ALL_CHECKBOX = "//input[@id='control_all_box']"
CONTROL_CHECKBOX = lambda name: "%s//td[normalize-space()='%s']" \
                                "/preceding-sibling::td[1]/input" % \
                                (USERS_TABLE, name)
RESET_PASSWORDS_BUTTON = "//input[@value='Reset Passwords']"
USERS_INFO_MAP = {'User Name': 2,
                  'Full Name': 3,
                  'User Role': 4,
                  'Account Status': 5,
                  'Password Expires': 6}
# row_num and col_num starts from 1
USERS_TABLE_ROWS = "%s/tbody/tr" % (USERS_TABLE,)
USERS_TABLE_CELL = lambda row_num, col_num: "%s[%d]/td[%d]" % \
                                            (USERS_TABLE_ROWS, row_num, col_num)
EDIT_SETTING_BUTTON = "//input[@value='Edit Settings...']"
SUBMIT_BUTTON = "//input[@value='Submit']"

EXT_AUTH_CUSTOMER_ENABLE_BUTTON = "//input[@value='Enable...' and @id='user']"
EXT_AUTH_CUSTOMER_EDIT_BUTTON = "//input[@value='Edit Global Settings...' and @id='user']"
EXT_AUTH_DEVOPS_ENABLE_BUTTON = "//input[@value='Enable...' and @id='devops']"
EXT_AUTH_DEVOPS_EDIT_BUTTON = "//input[@value='Edit Global Settings...' and @id='devops']"
EXT_AUTH_ENABLED_CHECKBOX = "//input[@id='extauth_enabled']"

SF_AUTH_ENABLED_CHECKBOX = "//input[@id='sf_auth_enabled']"
SF_AUTH_EDIT_BUTTON = "//input[@type='button' and contains(@onclick, 'FormEditSecondFactorAuth')]"

EDIT_DLP_TRACKING_PRIV_BUTTON = "//input[@type='button' and " \
                                "contains(@onclick, 'EditTrackingPrivilegesForm')]"
EDIT_URL_LOGGING_PRIV_BUTTON = "//input[@type='button' and " \
                               "contains(@onclick, 'EditTrackingPrivilegesForm')]"

SYSTEM_GENERATED_PASSWORD = "//input[@id='sysgen']"
ENFORCE_PASSWORD_CHANGE_BUTTON = "//input[@value='Enforce Passphrase Change']"
PASSWORD_CHANGE_INSTANT_RADIO = "//input[@id='enable_immidiate_lock']"
PASSWORD_CHANGE_LATER_RADIO = "//input[@id='enable_password_expiration_time']"
EXP_TIME_TEXTBOX = "//input[@id='expiry_days']"
ENABLE_PASSWORD_GRACE_CHECKBOX = "//input[@id='enable_password_grace_time']"
GRACE_TIME_TEXTBOX = "//input[@id='grace_time']"
SAML_PROFILE_PATH = "//a[contains(., 'System Administration > SAML')]"

PAGE_PATH = ('System Administration', 'Users')


class Users(GuiCommon):
    """Keywords for GUI interaction with System Administration -> Users
    page
    """

    def get_keyword_names(self):
        return ['users_add',
                'users_edit',
                'users_delete',
                'users_get_info',
                'users_reset_password',
                'enforce_password_change',

                'users_external_auth_is_enabled',
                'users_external_auth_enable',
                'users_external_auth_disable',
                'users_external_auth_edit',

                'users_external_auth_devops_is_enabled',
                'users_external_auth_devops_enable',
                'users_external_auth_devops_edit',
                'users_external_auth_devops_disable',
                'users_sf_auth_is_enabled',
                'users_sf_auth_enable',
                'users_sf_auth_disable',
                'users_sf_auth_edit',
                'users_sf_auth_privileges',

                'users_edit_account_password_restrictions',

                'users_dlp_tracking_privileges_edit',
                'users_url_logging_privileges_edit',
                'navigate_to_saml_profile']

    def _get_user_settings_controller(self):
        if not hasattr(self, '_user_settings_controller'):
            self._user_settings_controller = UserSettings(self)
        return self._user_settings_controller

    def _get_account_and_passwords_controller(self):
        if not hasattr(self, '_acc_and_passw_controller'):
            self._acc_and_passw_controller = PasswordAndAccountSettings(self)
        return self._acc_and_passw_controller

    def _get_ext_auth_controller(self):
        if not hasattr(self, '_ext_auth_controller'):
            self._ext_auth_controller = ExtAuthSettings(self)
        return self._ext_auth_controller

    def _get_ext_auth_devops_controller(self):
        if not hasattr(self, '_ext_auth_devops_controller'):
            self._ext_auth_devops_controller = ExtAuthDevopsSettings(self)
        return self._ext_auth_devops_controller

    def _get_sf_auth_controller(self):
        if not hasattr(self, '_sf_auth_controller'):
            self._sf_auth_controller = SfAuthSettings(self)
        return self._sf_auth_controller

    @go_to_page(PAGE_PATH)
    def users_add(self, name, settings):
        """Add user to ESA appliance

        *Parameters:*
        - `name`: the short name of new user
        - `settings`: dictionary containing new user settings.
        This dictionary can contain next items:
        | `Full Name` | user's full name, mandatory |
        | `User Role` | user's role profile. Either "Predefined" or "Custom" |
        | `Predefined Role` | user's predefined role. Available if `User Role`
        is set to "Predefined". Either "Administrator", "Operator",
        "Read-Only Operator", "Guest", "Technician", "Help Desk User" |
        | `Custom Role` | user's custom role. Available if `User Role`
        is set to "Custom". Can be one of the roles defined in Users Roles |
        | `New Role Name` | name of the new user's role. Mandatory if
        `User Role` is set to "Custom" and `Custom Role` is not set |
        | `Password Option` | should be set to 'generated' if the user wants
        system to generate a password. |
        | `Password` | user's password, mandatory if we dont go for system generated
        password. It must satisfy current password policies defined in settings |

        *Returns:*
        - returns the generated password if the Password Option is set to
        generated, else returns nothing

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct

        *Examples:*
        | ${settings1}= | Create Dictionary |
        | ... | Full Name | test test |
        | ... | User Role | Predefined |
        | ... | Predefined Role | Guest |
        | ... | Password | Ironport@123 |
        | ${settings2}= | Create Dictionary |
        | ... | Full Name | custom 1 |
        | ... | User Role | Custom |
        | ... | New Role Name | my_new_role |
        | ... | Password Option | generated |
        | Users Add | test1 | ${settings1} |
        | ${sys_gen_pass}= | Users Add | test2 | ${settings2} |
        """
        self.click_button(ADD_USER_BUTTON)

        password = None
        settings_controller = self._get_user_settings_controller()
        settings.update({'User Name': name})
        settings_controller.set(settings)
        if self._is_element_present(SYSTEM_GENERATED_PASSWORD):
            password = self.get_value(SYSTEM_GENERATED_PASSWORD)
        self._click_submit_button()
        return password

    @set_speed(1)
    @go_to_page(PAGE_PATH)
    def users_edit(self, name, settings={}):
        """Edit user on ESA appliance

        *Parameters:*
        - `name`: the short name of existing user to be edited
        - `settings`: dictionary containing edited user settings.
        This dictionary can contain next items:
        | `Full Name` | user's full name, mandatory |
        | `User Role` | user's role profile. Either "Predefined" or "Custom" |
        | `Predefined Role` | user's predefined role. Available if `User Role`
        is set to "Predefined". Either "Administrator", "Operator",
        "Read-Only Operator", "Guest", "Technician", "Help Desk User" |
        | `Custom Role` | user's custom role. Available if `User Role`
        is set to "Custom". Can be one of the roles defined in Users Roles |
        | `New Role Name` | name of the new user's role. Mandatory if
        `User Role` is set to "Custom" and `Custom Role` is not set |
        | `Password Option` | should be set to 'generated' if the user wants
        system to generate a password. |
        | `Password` | user's password, mandatory if we dont go for system generated
        password. It must satisfy current password policies defined in settings |
        | `Lock Account` | whether to lock current user account. All other
        settings will be ignored if this option is set. Either ${True}
        or ${False} |

        *Returns:*
        - returns the generated password if the Password Option is set to
        generated, else returns nothing

        *Exceptions:*
        - `ValueError`: if any of passed values is not correct or
        given user does not exist on appliance

        *Examples:*
        | ${settings1}= | Create Dictionary |
        | ... | Full Name | test test |
        | ... | User Role | Predefined |
        | ... | Predefined Role | Guest |
        | ... | Password Option | generated |
        | ${settings2}= | Create Dictionary |
        | ... | Lock Account | ${True} |
        | ${sys_gen_pass}= | Users Edit | test1 | ${settings1} |
        # This account will be locked
        | Users Edit | test2 | ${settings2} |
        """
        password = None
        if self._is_element_present(USER_EDIT_LINK(name)):
            self.click_button(USER_EDIT_LINK(name))
        else:
            raise ValueError('User named "%s" does not exist' % \
                             (name,))

        settings_controller = self._get_user_settings_controller()
        settings_controller.set(settings)
        if self._is_element_present(SYSTEM_GENERATED_PASSWORD):
            password = self.get_value(SYSTEM_GENERATED_PASSWORD)
        if self._is_element_present(SUBMIT_BUTTON):
            self._click_submit_button()
        return password

    @go_to_page(PAGE_PATH)
    def users_delete(self, name):
        """Delete existing user from ESA appliance

        *Parameters:*
        - `name`: name of an existing user

        *Exceptions:*
        - `ValueError`: if user with given name does not exist on
        appliance or can not be deleted

        *Examples:*
        | Users Delete | test |
        """
        if self._is_element_present(USER_DELETE_LINK(name)):
            self.click_button(USER_DELETE_LINK(name), 'don\'t wait')
        else:
            raise ValueError('User named "%s" does not exist' \
                             ' or it is prohibited to delete this' \
                             ' user' % (name,))
        self._click_continue_button()

    @go_to_page(PAGE_PATH)
    def users_get_info(self, name='all'):
        """Get info about users configured on current ESA appliance

        *Parameters:*
        - `name`: name of user whose info will be taken. If not given
        then all users info will be returned

        *Return:*
        List of dictionaries or one dictionary if user name is not "all".
        Each dictionary contains info about one user
        and has the next items:
        | `User Name` | user'a short name |
        | `Full Name` | user's full name |
        | `User Role` | user's role |
        | `Account Status` | current account status. Can be, for example,
        "Active", "Pending" |
        | `Password Expires` | status of account password expiration. Can be,
        for example, "n/a" or "Expired" |

        *Exceptions:*
        - `ValueError`: if there is no user with given name

        *Examples:*
        | ${info}= | Users Get Info |
        | Log | ${info} |
        | ${status0}= | Get From List | ${info} | 0 |
        | ${status}= | Get From Dictionary | ${status0} | Account Status |
        | Should Be Equal | ${status} | Active |
        """
        details = []
        users_count = int(self.get_matching_xpath_count(USERS_TABLE_ROWS)) - 1
        for row_num in xrange(2, 2 + users_count):
            entry = {}
            for col_name, col_num in USERS_INFO_MAP.iteritems():
                entry[col_name] = self.get_text(USERS_TABLE_CELL(row_num, col_num))
            details.append(entry)
        if name.upper() == 'ALL':
            return details
        else:
            dest_entry = filter(lambda x: x['User Name'] == name, details)
            if dest_entry:
                return dest_entry[0]
            else:
                raise ValueError('User named "%s" does not exist on appliance' % \
                                 (name,))

    @go_to_page(PAGE_PATH)
    def users_reset_password(self, names):
        """Reset user(s) passwords

        *Parameters:*
        - `names`: user names list whose password will be reseted.
        Can be 'all' to reset all passwords

        *Exceptions:*
        - `ValueError`: if user with given name was not found

        *Examples:*
        | ${users_list}= | Create List | admin | test |
        | Users Reset Password | ${users_list} |
        # Reset passwords on all users
        | Users Reset Password | all |
        """
        if isinstance(names, basestring) and names.upper() == 'ALL':
            self._select_checkbox(CONTROL_ALL_CHECKBOX)
        else:
            if isinstance(names, basestring):
                names = (names,)
            for name in names:
                if self._is_element_present(CONTROL_CHECKBOX(name)):
                    self._select_checkbox(CONTROL_CHECKBOX(name))
                else:
                    raise ValueError('User named "%s" does not exist' % \
                                     (name,))
        self.click_button(RESET_PASSWORDS_BUTTON)
        self._check_action_result()

    @go_to_page(PAGE_PATH)
    def enforce_password_change(self, names, force_type, exp_time=None, \
                                enable_grace_period=None, grace_time=None):
        """Enforce password change

        *Parameters:*
        - `names`: user names list whose password will be forced
	   to change(either instantly or after a specified time)
           Can be 'all' to enforce change on all passwords
        - `force_type` : Either 'instant' or 'later'
	- `exp_time` : password expiration period in days.
           Applicable if 'force_type' is 'later'
	- `enable_grace_period` : Whether to use grace period
           Applicable if 'force_type' is 'later'
	- `grace_time` : period after user's password change time during
           which the user will be forced to change her/his password (in days)
	   Applicable if 'enable_grace_period' is set to 'yes'

        *Exceptions:*
        - `ValueError`: if user with given name was not found

        *Examples:*
	# Enforce password change on selected users(later)
        | ${users_list}= | Create List | admin | test |
        | Enforce Password Change | ${users_list} |
	| ... | later |
	| ... | 5 |
	| ... | yes |
	| ... | 3 |

        # Enforce password change on all users(instant}
        | Enforce Password Change | all | instant |
        """
        if isinstance(names, basestring) and names.upper() == 'ALL':
            self._select_checkbox(CONTROL_ALL_CHECKBOX)
        else:
            if isinstance(names, basestring):
                names = (names,)
            for name in names:
                if self._is_element_present(CONTROL_CHECKBOX(name)):
                    self._select_checkbox(CONTROL_CHECKBOX(name))
                else:
                    raise ValueError('User named "%s" does not exist' % \
                                     (name,))

        self.click_button(ENFORCE_PASSWORD_CHANGE_BUTTON, "don't wait")
        if force_type.lower() == 'instant':
            self._click_radio_button(PASSWORD_CHANGE_INSTANT_RADIO)
        elif force_type.lower() == 'later':
            self._click_radio_button(PASSWORD_CHANGE_LATER_RADIO)
            self.input_text(EXP_TIME_TEXTBOX, exp_time)
            if enable_grace_period:
                self._select_checkbox(ENABLE_PASSWORD_GRACE_CHECKBOX)
                self.input_text(GRACE_TIME_TEXTBOX, grace_time)
        self._click_continue_button()
        self._check_action_result()

    @go_to_page(PAGE_PATH)
    def users_edit_account_password_restrictions(self, restrictions={}):
        """Edit global account passwords policies

        *Parameters:*
        - `restrictions`: dictionary whose items can be:
        | `Lock Account After` | whether to lock account after particular
        count of failed attempts. Either ${True} or ${False} |
        | `Account Lock Threshold` | account lock threshold, number of attempts.
        Available if `Lock Account After` is set to ${True} |
        | `Display Locked Message` | whether to display Locked Account Message
        if Administrator has manually locked a user account. Either ${True} or
        ${False} |
        | `Account Locked Message` | message which appears on the login page if
        an Administrator manually locks a user account Either ${True} or
        ${False} |
        | `Force Password Change on Admin Reset` | whether to require a password
        reset whenever a user's password is set or changed by an admin. Either
        ${True} or ${False} |
        | `Enable Password Expiration` | whether to require users to reset
        passwords after some period. Either ${True} or ${False} |
        | `Password Expiration Period` | password expiration period in days |
        | `Enable Password Expiration Warning` | whether to display reminder
        before password expiration. Either ${True} or ${False} |
        | `Password Expiration Warning Period` | password expiration warning period,
        in days |
        | `Enable Password Grace Period` | whether to allow a grace period
        to reset the password after the password expiry. Either ${True} or ${False} |
        | `Password Grace Period` | password grace period in days |
        | `Minimum Password Length` | minimum password length, number
        in range 6..128 |
        | `Password Require Upper and Lower Letters` | whether to require at least
        one upper (A-Z) and one lower (a-z) case letter. Either ${True} or ${False} |
        | `Password Require Numbers` | whether to require at least one number (0-9).
        Either ${True} or ${False} |
        | `Password Require Special Char` | whether to require at least one special
        character. Either ${True} or ${False} |
        | `Ban Usernames and Their Variations as Passwords` | whether to ban usernames
        and their variations as passwords. Either ${True} or ${False} |
        | `Ban Reuse of the Recent Passwords` | whether to ban reuse of the recent
        passwords. Either ${True} or ${False} |
        | `Count of Recent Passwords` | count of recent passwords, number. Available
        if `Ban Reuse of the Recent Passwords` is set to ${True} |
        | `Words To Disallow` | list of words to disallow in password.
        Create a text file containing the forbidden words.
        Each word must be on a separate line.
        Save text file as "forbidden_password_words.txt".
        Upload the file to the appliance using SCP or FTP. |
        | `Enable Entropy For Admin` | Enable base entropy for admin
        Either ${True} or ${False} |
        | `Entropy Value For Admin` | Base entropy value for admin |
        | `Enable Entropy For Technitian` | Enable base entropy for technitian
        Either ${True} or ${False} |
        | `Entropy Value For Technitian` | Base entropy value for technitian |
        | `Enable Entropy For Readonly` | Enable base entropy for readonly
        Either ${True} or ${False} |
        | `Entropy Value For Readonly` | Base entropy value for readonly |
        | `Enable Entropy For Operator` | Enable base entropy for operator
        Either ${True} or ${False} |
        | `Entropy Value For Operator` | Base entropy value for operator |
        | `Enable Entropy For Guest` | Enable base entropy for guest
        Either ${True} or ${False} |
        | `Entropy Value For Guest` | Base entropy value for guest |
        | `Enable Entropy For Helpdesk` | Enable base entropy for helpdesk
        Either ${True} or ${False} |
        | `Entropy Value For Helpdesk` | Base entropy value for helpdesk |
        | `Enable Entropy For Customrole` | Enable base entropy for customrole
        Either ${True} or ${False} |
        | `Entropy Value For Customrole` | Base entropy value for customrole |


        *Exceptions:*
        - `ValueError`: if any of passed settings is not correct

        *Examples:*
        | ${policies}= | Create Dictionary |
        | ... | Lock Account After | ${True} |
        | ... | Account Lock Threshold | 6 |
        | ... | Display Locked Message | ${True} |
        | ... | Account Locked Message | blabla |
        | ... | Force Password Change on Admin Reset | ${True} |
        | ... | Enable Password Expiration | ${True} |
        | ... | Password Expiration Period | 100 |
        | ... | Enable Password Expiration Warning | ${True} |
        | ... | Password Expiration Warning Period | 50 |
        | ... | Enable Password Grace Period | ${True} |
        | ... | Password Grace Period | 3 |
        | ... | Minimum Password Length | 7 |
        | ... | Password Require Upper and Lower Letters | ${True} |
        | ... | Password Require Numbers | ${True} |
        | ... | Password Require Special Char | ${True} |
        | ... | Ban Usernames and Their Variations as Passwords | ${True} |
        | ... | Ban Reuse of the Recent Passwords | ${True} |
        | ... | Count of Recent Passwords | 10 |
        | ... | Words To Disallow | ${True} |
        | ... | Enable Entropy For Admin | ${True} |
        | ... | Entropy Value For Admin | 1 |
        | ... | Enable Entropy For Technitian | ${True} |
        | ... | Entropy Value For Technitian | 1 |
        | ... | Enable Entropy For Readonly | ${True} |
        | ... | Entropy Value For Readonly | 1 |
        | ... | Enable Entropy For Operator | ${True} |
        | ... | Entropy Value For Operator | 1 |
        | ... | Enable Entropy For Guest | ${True} |
        | ... | Entropy Value For Guest | 1 |
        | ... | Enable Entropy For Helpdesk | ${True} |
        | ... | Entropy Value For Helpdesk | 1 |
        | ... | Enable Entropy For Customrole | ${True} |
        | ... | Entropy Value For Customrole | 1 |

        | Users Edit Account Password Restrictions | ${policies} |
        """
        self.click_button(EDIT_SETTING_BUTTON)

        controller = self._get_account_and_passwords_controller()
        controller.set(restrictions)
        self._click_submit_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def users_external_auth_is_enabled(self):
        """Get External Authentication feature state

        *Return:*
        - True or False depending on current External Authentication Feature state

        *Examples:*
        | ${ext_auth_is_enabled}= | Users External Auth Is Enabled |
        """
        return not self._is_element_present(EXT_AUTH_CUSTOMER_ENABLE_BUTTON)

    @go_to_page(PAGE_PATH)
    def users_external_auth_enable(self, settings):
        """Enable External Authentication feature and sets
        additional settings for it. In case this feature is already
        enabled only its settings will be changed.

        *Parameters:*
        - `settings`: dictionary containing External Authentication Feature
        settings. Possible items are:
        | `Authentication Type` | External Authentication type. Either LDAP or
        RADIUS or SAML. Mandatory |
        | `Group Mapping` | dictionary containing LDAP/RADIUS external groups to
        local roles mapping. Mandatory. Can be omitted only if `Authentication Type` is
        set to RADIUS and `Group Mapping to Local` is set to
        "Map all externally authenticated users to the Administrator role" |
        | `External Authentication Attribute Name Map` | The Attribute Name and Value depends on what
        | `External Authentication Cache Timeout` | external authentication cache timeout
        in seconds |
        | `LDAP External Authentication Query` | name of ldap external authentication query
        defined in one of existing LDAP profiles. Applicable only if `Authentication Type`
        is set to LDAP |
        | `Timeout To Wait For Valid Response From Server` | timeout to wait for valid
        response from LDAP server in seconds. Applicable only if `Authentication Type`
        is set to LDAP |
        | `Group Mapping to Local` | whether to map external RADIUS groups to local. Either
        "Map externally authenticated users to multiple local roles" or
        "Map all externally authenticated users to the Administrator role". Applicable
        only if `Authentication Type` is set to RADIUS |
        | `RADIUS Server Information` | list containing available RADIUS servers.
        Format of one list item is
        <host name>,<port number>,<shared secret>,<timeout>,<protocol>. <host name> and
        <shared secret> are mandatory, all other parameters can be replaced with empty string
        if you want to leave them by default |

        *Examples:*
        | ${ldap_group_mapping}= | Create Dictionary |
        | ... | ${LDAP_GROUP_ADMINS} | Administrator |
        | ... | ${LDAP_GROUP_OPERATORS} | Operator |
        | ${ldap_ext_auth_settings}= | Create Dictionary |
        | ... | Authentication Type | LDAP |
        | ... | External Authentication Cache Timeout | 5 |
        | ... | LDAP External Authentication Query | ${LDAP_PROFILE_NAME}.externalauth |
        | ... | Timeout To Wait For Valid Response From Server | 10 |
        | ... | Group Mapping | ${ldap_group_mapping} |
        | ${is_enabled}= | Users External Auth Is Enabled |
        | Run Keyword If | not ${is_enabled} |
        | ... | Users External Auth Enable | ${ldap_ext_auth_settings} |
        | Set To Dictionary | ${ldap_group_mapping} | ${LDAP_GROUP_RO_USERS} | Read-Only Operator |
        | Users External Auth Edit | ${ldap_ext_auth_settings} |
        | Users External Auth Disable |

        | ${radius_group_mapping}= | Create Dictionary |
        | ... | ${LDAP_GROUP_ADMINS} | Administrator |
        | ... | ${LDAP_GROUP_OPERATORS} | Operator |
        | @{radius_servers}= | Create List |
        | ... | sma19.sma,1812,asdfghjkl,5,PAP |
        | ... | sma19.sma,1813,bsdfghjkl,10,CHAP |
        | ${radius_ext_auth_settings}= | Create Dictionary |
        | ... | Authentication Type | RADIUS |
        | ... | External Authentication Cache Timeout | 5 |
        | ... | Group Mapping to Local | Map externally authenticated users to multiple local roles |
        | ... | RADIUS Server Information | ${radius_servers} |
        | ... | Group Mapping | ${radius_group_mapping} |
        | ${is_enabled}= | Users External Auth Is Enabled |
        | Run Keyword If | not ${is_enabled} |
        | ... | Users External Auth Enable | ${radius_ext_auth_settings} |
        | Append to List | ${radius_servers} |
        | ... | sma19.sma,1814,asdfghjkl,, |
        | Users External Auth Edit | ${radius_ext_auth_settings} |
        | Users External Auth Disable |

        | ${saml_group_mapping}=                           | Create Dictionary                      |
        | ... | ${SAML_GROUP_ADMINS}                       | Administrator                          |
        | ... | ${SAML_GROUP_OPERATORS}                    | Operator                               |
        | ${enable_customer_ext_auth_settings}=            | Create Dictionary                      |
        | ... | Authentication Type                        | SAML                                   |
        | ... | External Authentication Attribute Name Map | mailRoutingAddress                     |
        | ... | Group Mapping                              | ${saml_group_mapping}                  |
        | Users External Auth Enable                       | ${enable_customer_ext_auth_settings}   |
        """
        self.click_button(EXT_AUTH_CUSTOMER_ENABLE_BUTTON)
        self._get_ext_auth_controller().set(settings)
        self._handle_continue_on_submit()

    def users_external_auth_edit(self, settings):
        """Edit External Authentication feature settings.
        In case this feature is disabled an exception will be raised

        *Parameters:*
        - `settings`: dictionary containing External Authentication Feature
        settings. Possible items are:
        | `Authentication Type` | External Authentication type. Either LDAP or
        RADIUS or SAML. Mandatory |
        | `Group Mapping` | dictionary containing LDAP/RADIUS external groups to
        local roles mapping. Mandatory. Can be omitted only if `Authentication Type` is
        set to RADIUS and `Group Mapping to Local` is set to
        "Map all externally authenticated users to the Administrator role" |
        | `External Authentication Attribute Name Map` | The Attribute Name and Value depends on what
        | `External Authentication Cache Timeout` | external authentication cache timeout
        in seconds |
        | `LDAP External Authentication Query` | name of ldap external authentication query
        defined in one of existing LDAP profiles. Applicable only if `Authentication Type`
        is set to LDAP |
        | `Timeout To Wait For Valid Response From Server` | timeout to wait for valid
        response from LDAP server in seconds. Applicable only if `Authentication Type`
        is set to LDAP |
        | `Group Mapping to Local` | whether to map external RADIUS groups to local. Either
        "Map externally authenticated users to multiple local roles" or
        "Map all externally authenticated users to the Administrator role". Applicable
        only if `Authentication Type` is set to RADIUS |
        | `RADIUS Server Information` | list containing available RADIUS servers.
        Format of one list item is
        <host name>,<port number>,<shared secret>,<timeout>,<protocol>. <host name> and
        <shared secret> are mandatory, all other parameters can be replaced with empty string
        if you want to leave them by default |

        *Exceptions:*
        - `ConfigError`: if External Authentication feature is disabled

        *Examples:*
        | ${ldap_group_mapping}= | Create Dictionary |
        | ... | ${LDAP_GROUP_ADMINS} | Administrator |
        | ... | ${LDAP_GROUP_OPERATORS} | Operator |
        | ${ldap_ext_auth_settings}= | Create Dictionary |
        | ... | Authentication Type | LDAP |
        | ... | External Authentication Cache Timeout | 5 |
        | ... | LDAP External Authentication Query | ${LDAP_PROFILE_NAME}.externalauth |
        | ... | Timeout To Wait For Valid Response From Server | 10 |
        | ... | Group Mapping | ${ldap_group_mapping} |
        | ${is_enabled}= | Users External Auth Is Enabled |
        | Run Keyword If | not ${is_enabled} |
        | ... | Users External Auth Enable | ${ldap_ext_auth_settings} |
        | Set To Dictionary | ${ldap_group_mapping} | ${LDAP_GROUP_RO_USERS} | Read-Only Operator |
        | Users External Auth Edit | ${ldap_ext_auth_settings} |
        | Users External Auth Disable |

        | ${radius_group_mapping}= | Create Dictionary |
        | ... | ${LDAP_GROUP_ADMINS} | Administrator |
        | ... | ${LDAP_GROUP_OPERATORS} | Operator |
        | @{radius_servers}= | Create List |
        | ... | sma19.sma,1812,asdfghjkl,5,PAP |
        | ... | sma19.sma,1813,bsdfghjkl,10,CHAP |
        | ${radius_ext_auth_settings}= | Create Dictionary |
        | ... | Authentication Type | RADIUS |
        | ... | External Authentication Cache Timeout | 5 |
        | ... | Group Mapping to Local | Map externally authenticated users to multiple local roles |
        | ... | RADIUS Server Information | ${radius_servers} |
        | ... | Group Mapping | ${radius_group_mapping} |
        | ${is_enabled}= | Users External Auth Is Enabled |
        | Run Keyword If | not ${is_enabled} |
        | ... | Users External Auth Enable | ${radius_ext_auth_settings} |
        | Append to List | ${radius_servers} |
        | ... | sma19.sma,1814,asdfghjkl,, |
        | Users External Auth Edit | ${radius_ext_auth_settings} |
        | Users External Auth Disable |

        | ${saml_group_mapping}=                           | Create Dictionary      |
        | ... | ${SAML_GROUP_HELPDESK                      | Helpdesk               |
        | ... | ${SAML_GROUP_GUEST}                        | Guest                  |
        | Users External Auth Edit                         |                        |
        | ... | Authentication Type                        | SAML                   |
        | ... | External Authentication Attribute Name Map | mailLocalAddress       |
        | ... | Group Mapping                              | ${saml_group_mapping}  |
        """
        if not self.users_external_auth_is_enabled():
            raise guiexceptions.ConfigError('External Authentication ' \
                                            'feature should be enabled in order to edit its settings')
        self.click_button(EXT_AUTH_CUSTOMER_EDIT_BUTTON)
        self._get_ext_auth_controller().set(settings)
        self._handle_continue_on_submit()

    @set_speed(0)
    def users_external_auth_disable(self):
        """Disable External Authentication feature.
        Will do nothing is the feature is already disabled

        *Examples:*
        | Users External Auth Disable |
        """
        if not self.users_external_auth_is_enabled():
            return
        self.click_button(EXT_AUTH_CUSTOMER_EDIT_BUTTON)
        self._unselect_checkbox(EXT_AUTH_ENABLED_CHECKBOX)
        self._click_submit_button(skip_wait_for_title=True)

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
            raise guiexceptions.ConfigError('External Authentication for Devops ' \
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
            self._unselect_checkbox(EXT_AUTH_ENABLED_CHECKBOX)
            self._click_submit_button(skip_wait_for_title=True)
        else:
            print '*DEBUG* External Authentication for DevOps is already disabled'

    @go_to_page(PAGE_PATH)
    def users_dlp_tracking_privileges_edit(self, settings):
        """Set DLP Tracking Privileges for different roles

        *Parameters:*
        - `settings`: dictionary containing DLP privilege settings for
        different available roles, e.g. key is role name and
        value is either ${True} or ${False} (enbale or disable this
        privilege for this role). Role name can be also custom role
        name and it should be spelled exactly the same way as it is spelled
        on the DLP Tracking Privileges settings page.

        *Examples:*
        | ${privileges_map}= | Create Dictionary |
        | ... | Administrator | ${True} |
        | ... | Operator | ${False} |
        | ... | Read-Only Operator | ${False} |
        | ... | Help Desk User | ${True} |
        | ... | My Cusom Role | ${False} |
        | Users DLP Tracking Privileges Edit | ${privileges_map} |
        """
        self.click_button(EDIT_DLP_TRACKING_PRIV_BUTTON)
        DlpTrackingPrivSettings(self).set(settings)
        self._click_submit_button()

    @set_speed(0)
    @go_to_page(PAGE_PATH)
    def users_url_logging_privileges_edit(self, settings):
        """Set URL Logging Privileges for different roles

        *Parameters:*
        - `settings`: dictionary containing URL logging privilege settings for
        different available roles, e.g. key is role name and
        value is either ${True} or ${False} (enbale or disable this
        privilege for this role). Role name can be also custom role
        name and it should be spelled exactly the same way as it is spelled
        on the URL Logging Privileges settings page.

        *Examples:*
        | ${url_logging_privileges_map}= | Create Dictionary |
        | ... | Administrator | ${True} |
        | ... | Operator | ${False} |
        | ... | Read-Only Operator | ${False} |
        | ... | Help Desk User | ${True} |
        | ... | My Custom Role | ${False} |
        | Users URL Logging Privileges Edit | ${url_logging_privileges_map} |
        """
        self.click_button(EDIT_URL_LOGGING_PRIV_BUTTON)
        UrlLoggingPrivSettings(self).set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def users_sf_auth_is_enabled(self):
        """Get Two Factor Authentication feature state

        *Return:*
        - True or False depending on current Two Factor Feature state

        *Examples:*
        | ${sf_auth_is_enabled}= | Users sf Auth Is Enabled |
        """
        SF_AUTH_NOT_ENABLED_MARK = 'Two-Factor Authentication is disabled.'
        return not self._is_text_present(SF_AUTH_NOT_ENABLED_MARK)

    @go_to_page(PAGE_PATH)
    def users_sf_auth_enable(self, settings):
        """Enable Two Factor Authentication feature and sets
        additional settings for it. In case this feature is already
        enabled only its settings will be changed.

        *Parameters:*
        - `settings`: dictionary containing Two Factor Authentication Feature
        settings. Possible items are:
        "Map all externally authenticated users to the Administrator role". Applicable
        only if `Authentication Type` is set to RADIUS |
        | `RADIUS Server Information` | list containing available RADIUS servers.
        Format of one list item is
        <host name>,<port number>,<shared secret>,<timeout>,<protocol>. <host name> and
        <shared secret> are mandatory, all other parameters can be replaced with empty string
        if you want to leave them by default |

        *Examples:*
        | @{radius_servers}= | Create List |
        | ... | sma19.sma,1812,asdfghjkl,5,PAP |
        | ... | sma19.sma,1813,bsdfghjkl,10,CHAP |
        | ${radius_sf_auth_settings}= | Create Dictionary |
        | ... | Authentication Type | RADIUS |
        | ... | RADIUS Server Information | ${radius_servers} |
        | ${is_enabled}= | Users SF Auth Is Enabled |
        | Run Keyword If | not ${is_enabled} |
        | ... | Users Sf Auth Enable | ${radius_sf_auth_settings} |
        """
        self.click_button(SF_AUTH_EDIT_BUTTON)
        self._get_sf_auth_controller().set(settings)
        self._handle_continue_on_submit()

    @go_to_page(PAGE_PATH)
    def users_sf_auth_edit(self, settings):
        """Edit Two Factor Authentication feature settings.
        In case this feature is disabled an exception will be raised

        *Parameters:*
        - `settings`: dictionary containing External Authentication Feature
        settings. Possible items are:
        | `RADIUS Server Information` | list containing available RADIUS servers.
        Format of one list item is
        <host name>,<port number>,<shared secret>,<timeout>,<protocol>. <host name> and
        <shared secret> are mandatory, all other parameters can be replaced with empty string
        if you want to leave them by default |

        *Exceptions:*
        - `ConfigError`: if External Authentication feature is disabled

        *Examples:*
        | ${radius_group_mapping}= | Create Dictionary |
        | ... | ${LDAP_GROUP_ADMINS} | Administrator |
        | ... | ${LDAP_GROUP_OPERATORS} | Operator |
        | @{radius_servers}= | Create List |
        | ... | sma19.sma,1812,asdfghjkl,5,PAP |
        | ... | sma19.sma,1813,bsdfghjkl,10,CHAP |
        | ${radius_sf_auth_settings}= | Create Dictionary |
        | ... | RADIUS Server Information | ${radius_servers} |
        | ${is_enabled}= | Users External Auth Is Enabled |
        | Run Keyword If | not ${is_enabled} |
        | ... | Users sf Auth Enable | ${radius_sf_auth_settings} |
        | Append to List | ${radius_servers} |
        | ... | sma19.sma,1814,asdfghjkl,, |
        | Users sf Auth Edit | ${radius_sf_auth_settings} |
        """
        if not self.users_sf_auth_is_enabled():
            raise guiexceptions.ConfigError('Two-Factor Authentication ' \
                                            'feature should be enabled in order to edit its settings')
        self.click_button(SF_AUTH_EDIT_BUTTON)
        self._get_sf_auth_controller().set(settings)
        self._handle_continue_on_submit()

    @go_to_page(PAGE_PATH)
    def users_sf_auth_privileges(self, settings):
        """Set Two-Factor Auth Privileges for different roles

        *Parameters:*
        - `settings`: dictionary containing Two-Factor Auth privilege settings for
        different available roles, e.g. key is role name and
        value is either ${True} or ${False} (enbale or disable this
        privilege for this role). Role name can be also custom role
        name and it should be spelled exactly the same way as it is spelled
        on the Two Factor Privileges settings page.

        *Examples:*
        | ${privileges_map}= | Create Dictionary |
        | ... | Administrator | ${True} |
        | ... | Operator | ${False} |
        | ... | Read-Only Operator | ${False} |
        | ... | Help Desk User | ${True} |
        | ... | My Cusom Role | ${False} |
        | Users Sf Auth Privileges | ${privileges_map} |
        """

        if not self.users_sf_auth_is_enabled():
            raise guiexceptions.ConfigError('Two-Factor Authentication ' \
                                            'feature should be enabled in order to assign privileges')
        self.click_button(SF_AUTH_EDIT_BUTTON)
        SecondFactorPrivSettings(self).set(settings)
        self._click_submit_button()

    @go_to_page(PAGE_PATH)
    def users_sf_auth_disable(self):
        """Disable Two Factor Authentication feature.
        Will do nothing is the feature is already disabled

        *Examples:*
        | Users Sf Auth Disable |
        """
        if not self.users_sf_auth_is_enabled():
            return
        self.click_button(SF_AUTH_EDIT_BUTTON)
        self._unselect_checkbox(SF_AUTH_ENABLED_CHECKBOX)
        self._click_submit_button(skip_wait_for_title=True)

    def _handle_continue_on_submit(self):
        """ Handles continue button if it appears after submit"""

        try:
            prev_timeout = self.set_selenium_timeout(10)
            self._click_submit_button(skip_wait_for_title=True)
        except Exception as e:
            self._click_continue_button()
        finally:
            self.set_selenium_timeout(prev_timeout)

    @go_to_page(PAGE_PATH)
    def navigate_to_saml_profile(self, profile):

        """This keyword to navigate from user page to saml page customer /devops
        :param: user | devops
        """

        is_navigation_successful = True
        if profile == 'user':
            if self.users_external_auth_is_enabled():
                try:
                    self.click_button(EXT_AUTH_CUSTOMER_EDIT_BUTTON)
                    self.click_button(SAML_PROFILE_PATH)
                    if not 'System Administration > SAML' in self.get_title():
                        is_navigation_successful = False
                except Exception as e:
                    is_navigation_successful = False
            else:
                raise guiexceptions.GuiError('User External Authentication is not Enabled for user')
        elif profile == 'devops':
            if self.users_external_auth_devops_is_enabled():
                try:
                    self.click_button(EXT_AUTH_DEVOPS_EDIT_BUTTON)
                    self.click_button(SAML_PROFILE_PATH)
                    if not 'System Administration > SAML' in self.get_title():
                        is_navigation_successful = False
                except Exception as e:
                    is_navigation_successful = False
            else:
                raise guiexceptions.GuiError('User External Authentication is not Enabled for devops')
        else:
            raise guiexceptions.GuiError('Invalid option provided for navigating saml profiles')
        if not is_navigation_successful:
            raise guiexceptions.GuiError('SAML profile page cant be navigated')
        return is_navigation_successful
