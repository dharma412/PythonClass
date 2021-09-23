#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/gui/options/change_password.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

from common.gui.guicommon import GuiCommon

OLD_PASSWORD_TEXTBOX = "//input[@name='old_pwd']"
MANUAL_PASSWORD_RADIO = "//input[@id='manual']"
NEW_PASSWORD_TEXTBOX = "//input[@name='passwdv']"
RETYPE_NEW_PASSWORD_TEXTBOX = "//input[@name='repasswd']"
SYSTEM_GENERATED_PASSWORD_RADIO = "//input[@id='sys_gen']"
GENERATE_PASSWORD_BUTTON = "//input[@value='Generate']"
SYSTEM_GENERATED_PASSWORD = "//input[@id='sysgen']"


class ChangePassword(GuiCommon):
    """
        Keyword for menu Options -> Change Passphrase
    """

    def get_keyword_names(self):
        return ['change_password',
                ]

    def _open_page(self):
        self._navigate_to('Options', 'Change Passphrase')

    def _fill_lines(self, old_password, new_password):
        self.input_text(OLD_PASSWORD_TEXTBOX, old_password)
        self.input_text(NEW_PASSWORD_TEXTBOX, new_password)
        self.input_text(RETYPE_NEW_PASSWORD_TEXTBOX, new_password)

    def change_password(self, password_option="manual_password", old_password=None, new_password=None):
        """ Change user password.

        *Parameters*
            - `password_option`: two options - 'generate_password' and 'manual_password'.
               Default is 'manual_password'.
            - `old_password`: current password.
            - `new_password`: new password. If 'password option' is 'manual_password',
               then only applicable.

        *Return*
            password : Returns system generated password, when password_option is selected
                       as generated_password else returns 'None'.

        *Exceptions*
            None.

        *Examples*
            | Change Password | old_password=strong_pass | new_password=stronger_pass |

            | ${password} = | Change Password | password_option=manual_password |
            | ... | old_password=long_pass | new_password=longer_pass |

            | ${sys_generated_pass}= | Change Password | password_option=generate_password |
            | ... | old_password=long_pass |
        """
        self._open_page()
        if password_option == "manual_password":
            self._click_radio_button(MANUAL_PASSWORD_RADIO)
            self._fill_lines(old_password, new_password)
            self._click_submit_button()
        else:
            self.input_text(OLD_PASSWORD_TEXTBOX, old_password)
            self._click_radio_button(SYSTEM_GENERATED_PASSWORD_RADIO)
            self.click_button(GENERATE_PASSWORD_BUTTON, "don't wait")
            password = self.get_value(SYSTEM_GENERATED_PASSWORD)
            self._click_submit_button()
            return password
