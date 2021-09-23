#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/admin/users_def/password_and_account_settings.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs

LOCK_ACCOUNT_AFTER_CHECKBOX = ('Lock Account After',
                               "//input[@id='enable_failed_login_lock']")
ACCOUNT_LOCK_THRESHOLD = ('Account Lock Threshold',
                          "//input[@id='account_lock_threshold']")
DISPLAY_LOCKED_MSG_CHECKBOX = ('Display Locked Message',
                               "//input[@id='display_account_locked_message']")
ACCOUNT_LOCKED_MSG = ('Account Locked Message',
                      "//textarea[@id='account_locked_message']")
FORCE_PW_CHANGE_ON_ADMIN_RESET_CHECKBOX = ('Force Password Change on Admin Reset',
                                           "//input[@id='force_pw_change_on_admin_reset']")
ENABLE_PASSWORD_EXPIRATION_CHECKBOX = ('Enable Password Expiration',
                                       "//input[@id='enable_password_expiration']")
PASSWORD_EXPIRATION_PERIOD = ('Password Expiration Period',
                              "//input[@id='password_expiration_period']")
ENABLE_PASSWORD_EXPIRATION_WARNING_CHECKBOX = ('Enable Password Expiration Warning',
                                               "//input[@id='enable_password_expiration_warning']")
PASSWORD_EXPIRATION_WARNING_PERIOD = ('Password Expiration Warning Period',
                                      "//input[@id='password_expiration_warning_period']")

ENABLE_PASSWORD_GRACE_PERIOD_CHECKBOX = ('Enable Password Grace Period',
                                         "//input[@id='enable_password_grace']")
PASSWORD_GRACE_PERIOD = ('Password Grace Period',
                         "//input[@id='password_grace_period']")
PASSWORD_MIN_LENGTH = ('Minimum Password Length',
                       "//input[@id='password_min_length']")
PASSWORD_REQUIRE_UPPER_LOWER_CHECKBOX = ('Password Require Upper and Lower Letters',
                                         "//input[@id='password_require_upper_lower']")
PASSWORD_REQUIRE_NUMERIC_CHAR_CHECKBOX = ('Password Require Numbers',
                                          "//input[@id='password_require_numeric_char']")
PASSWORD_REQUIRE_SPECIAL_CHAR_CHECKBOX = ('Password Require Special Char',
                                          "//input[@id='password_require_special_char']")
PASSWORD_NO_USERNAME_RESEMBLANCE_CHECKBOX = \
    ('Ban Usernames and Their Variations as Passwords',
     "//input[@id='password_no_username_resemblance']")
PASSWORD_REJECT_RECENT_CHECKBOX = ('Ban Reuse of the Recent Passwords',
                                   "//input[@id='password_reject_recent']")
PASSWORD_NUM_RECENT_REJECTED = ('Count of Recent Passwords',
                                "//input[@id='password_num_recent_rejected']")
WORDS_TO_DISALLOW_CHECKBOX = ('Words To Disallow',
                              "//input[@id='password_dict_check']")
ENABLE_ENTROPY_ADMIN_CHECKBOX = ('Enable Entropy For Admin',
                                 "//input[@id='base_entropy_admin']")
ENTROPY_VALUE_FOR_ADMIN = ('Entropy Value For Admin',
                           "//input[@id='base_entropy_admin_value']")
ENABLE_ENTROPY_TECHNITIAN_CHECKBOX = ('Enable Entropy For Technitian',
                                      "//input[@id='base_entropy_technician']")
ENTROPY_VALUE_FOR_TECHNITIAN = ('Entropy Value For Technitian',
                                "//input[@id='base_entropy_technician_value']")
ENABLE_ENTROPY_READONLY_CHECKBOX = ('Enable Entropy For Readonly',
                                    "//input[@id='base_entropy_readonly']")
ENTROPY_VALUE_FOR_READONLY = ('Entropy Value For Readonly',
                              "//input[@id='base_entropy_readonly_value']")
ENABLE_ENTROPY_OPERATOR_CHECKBOX = ('Enable Entropy For Operator',
                                    "//input[@id='base_entropy_operators']")
ENTROPY_VALUE_FOR_OPERATOR = ('Entropy Value For Operator',
                              "//input[@id='base_entropy_operators_value']")
ENABLE_ENTROPY_GUEST_CHECKBOX = ('Enable Entropy For Guest',
                                 "//input[@id='base_entropy_guest']")
ENTROPY_VALUE_FOR_GUEST = ('Entropy Value For Guest',
                           "//input[@id='base_entropy_guest_value']")
ENABLE_ENTROPY_HELPDESK_CHECKBOX = ('Enable Entropy For Helpdesk',
                                    "//input[@id='base_entropy_helpdesk']")
ENTROPY_VALUE_FOR_HELPDESK = ('Entropy Value For Helpdesk',
                              "//input[@id='base_entropy_helpdesk_value']")
ENABLE_ENTROPY_CUSTOMROLE_CHECKBOX = ('Enable Entropy For Customrole',
                                      "//input[@id='base_entropy_delegatedadmin']")
ENTROPY_VALUE_FOR_CUSTOMROLE = ('Entropy Value For Customrole',
                                "//input[@id='base_entropy_delegatedadmin_value']")


class PasswordAndAccountSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    @set_speed(0, 'gui')
    def set(self, new_value):
        self._set_checkboxes(new_value,
                             LOCK_ACCOUNT_AFTER_CHECKBOX,
                             DISPLAY_LOCKED_MSG_CHECKBOX,
                             FORCE_PW_CHANGE_ON_ADMIN_RESET_CHECKBOX,
                             ENABLE_PASSWORD_EXPIRATION_CHECKBOX,
                             ENABLE_PASSWORD_EXPIRATION_WARNING_CHECKBOX,
                             ENABLE_PASSWORD_GRACE_PERIOD_CHECKBOX,
                             PASSWORD_REQUIRE_UPPER_LOWER_CHECKBOX,
                             PASSWORD_REQUIRE_NUMERIC_CHAR_CHECKBOX,
                             PASSWORD_REQUIRE_SPECIAL_CHAR_CHECKBOX,
                             PASSWORD_NO_USERNAME_RESEMBLANCE_CHECKBOX,
                             PASSWORD_REJECT_RECENT_CHECKBOX,
                             WORDS_TO_DISALLOW_CHECKBOX,
                             ENABLE_ENTROPY_ADMIN_CHECKBOX,
                             ENABLE_ENTROPY_TECHNITIAN_CHECKBOX,
                             ENABLE_ENTROPY_READONLY_CHECKBOX,
                             ENABLE_ENTROPY_OPERATOR_CHECKBOX,
                             ENABLE_ENTROPY_GUEST_CHECKBOX,
                             ENABLE_ENTROPY_HELPDESK_CHECKBOX,
                             ENABLE_ENTROPY_CUSTOMROLE_CHECKBOX)

        self._set_edits(new_value,
                        ACCOUNT_LOCK_THRESHOLD,
                        ACCOUNT_LOCKED_MSG,
                        PASSWORD_EXPIRATION_PERIOD,
                        PASSWORD_EXPIRATION_WARNING_PERIOD,
                        PASSWORD_GRACE_PERIOD,
                        PASSWORD_MIN_LENGTH,
                        PASSWORD_NUM_RECENT_REJECTED,
                        ENTROPY_VALUE_FOR_ADMIN,
                        ENTROPY_VALUE_FOR_TECHNITIAN,
                        ENTROPY_VALUE_FOR_READONLY,
                        ENTROPY_VALUE_FOR_OPERATOR,
                        ENTROPY_VALUE_FOR_GUEST,
                        ENTROPY_VALUE_FOR_HELPDESK,
                        ENTROPY_VALUE_FOR_CUSTOMROLE)

    def get(self):
        raise NotImplementedError()
