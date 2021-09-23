#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/admin/users_def/user_settings.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.gui.decorators import set_speed
from common.gui.inputs_owner import InputsOwner, get_module_inputs_pairs
from credentials import *
import re

USER_NAME = ('User Name',
             "//input[@name='userName']")
FULL_NAME = ('Full Name',
            "//input[@name='fullName']")
USER_ROLE_RADIO_GROUP = ('User Role',
        {'Predefined': "//input[@id='role_predefined']",
         'Custom': "//input[@id='role_custom']"})
PREDEFINED_ROLE_COMBO = ('Predefined Role',
                         "//select[@id='group']")
CUSTOM_ROLES_COMBO = ('Custom Role',
                      "//select[@id='custom_role']")
NEW_ROLE_NAME = ('New Role Name',
                 "//input[@id='new_role']")
PASSWORD_RADIO_GROUP = ('Password Option',
            {'manual': "//input[@id='manual']",
             'generated': "//input[@id='sys_gen']"})
GENERATE_BUTTON = "//input[@value='Generate']"
PASSWORD = ('Password',
            "//input[@id='passwdv']")
PASSWORD_CONFIRM = ('Retype Password',
                    "//input[@id='repasswd']")
LOCK_ACCOUNT_BUTTONS = ('Lock Account',
                        {True: "//input[@value='Lock Account']",
                         False: "//input[@value='Unlock Account']"})
CHANGE_PASSWORD = "//input[@id='change']"
DO_NOT_CHANGE_PASSWORD = "//input[@id='no_change']"
ADMIN_PASSPHRASE = ('Admin Passphrase',
                    "//input[@id='old_pwd']")

ADMIN_PASSPHRASE_TXT = "//input[@id='old_pwd']"

class UserSettings(InputsOwner):
    def _get_registered_inputs(self):
        return get_module_inputs_pairs(__name__)

    def _fix_password_confirm(self, new_value):
        if new_value.has_key(PASSWORD[0]):
            new_value[PASSWORD_CONFIRM[0]] = new_value[PASSWORD[0]]

    @set_speed(0, 'gui')
    def set(self, new_value):
        if self._set_account_lock_state(new_value):
            return
        self._set_edits(new_value,
                USER_NAME,
                FULL_NAME)
        self._set_radio_groups(new_value,
                        USER_ROLE_RADIO_GROUP)
        self._set_combos(new_value,
                        PREDEFINED_ROLE_COMBO,
                        CUSTOM_ROLES_COMBO)
        self._set_edits(new_value, NEW_ROLE_NAME)
        if new_value.has_key('Admin Passphrase'):
            self._set_edits(new_value,ADMIN_PASSPHRASE)
        else:
            ADMIN_KEYPAIR={'Admin Passphrase':DUT_ADMIN_SSW_PASSWORD}
            self._set_edit_text(ADMIN_KEYPAIR,'Admin Passphrase',ADMIN_PASSPHRASE_TXT)

###Need to uncommented onces system generated password option available###
#        if new_value.has_key('Password Option') and str(new_value['Password Option']) == 'generated':
#            if self.gui._is_element_present(CHANGE_PASSWORD):
#                self.gui._click_radio_button(CHANGE_PASSWORD)
#            self.gui._click_radio_button(PASSWORD_RADIO_GROUP[1]['generated'])
#            self.gui.click_button(GENERATE_BUTTON, "don't wait")
        if new_value.has_key('Password'):
            if self.gui._is_element_present(CHANGE_PASSWORD):
                self.gui._click_radio_button(CHANGE_PASSWORD)
#            self.gui._click_radio_button(PASSWORD_RADIO_GROUP[1]['manual'])

###Need to remove this line once system genereated password is available###
        if new_value.has_key('Password'):
            if self.gui._is_element_present(CHANGE_PASSWORD):
                self.gui._click_radio_button(CHANGE_PASSWORD)
            self._fix_password_confirm(new_value)
            self._set_edits(new_value,
                        PASSWORD,
                        PASSWORD_CONFIRM)
        else:
            if self.gui._is_element_present(DO_NOT_CHANGE_PASSWORD):
                self.gui._click_radio_button(DO_NOT_CHANGE_PASSWORD)

    def _set_account_lock_state(self, new_value):
        """
        *Return:*
        True if lock state was set successfully
        or None otherwise
        """
        caption, locators_dict = LOCK_ACCOUNT_BUTTONS
        if new_value.has_key(caption):
            should_lock = new_value[caption]
            locator = locators_dict[should_lock]
            if not self.gui._is_element_present(locator) or \
               self.gui._is_text_present('uncommited changes'):
                if should_lock:
                    action = 'lock'
                else:
                    action = 'unlock'
                raise ValueError('It is impossible to %s account'\
                                 ' because it does not have such option'\
                                 ' or there are some uncommited changes' % \
                                 (action,))
            if should_lock:
                self.gui.input_text(ADMIN_PASSPHRASE_TXT, DUT_ADMIN_SSW_PASSWORD)
                self.gui.click_button(locator, 'don\'t wait')
                self.gui._click_continue_button()
            else:
                self.gui.input_text(ADMIN_PASSPHRASE_TXT, DUT_ADMIN_SSW_PASSWORD)
                self.gui.click_button(locator)
                self.gui._check_action_result()
            return True

    def get(self):
        raise NotImplementedError()
