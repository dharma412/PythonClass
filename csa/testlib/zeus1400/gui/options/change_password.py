#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/gui/options/change_password.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $


from common.gui.guicommon import GuiCommon

OLD_PASSWORD_TEXTBOX='name=old_pwd'
NEW_PASSWORD_TEXTBOX='name=passwdv'
RETYPE_NEW_PASSWORD_TEXTBOX='name=repasswd'


class ChangePassword(GuiCommon):

    """
        Keyword for menu Options -> Change Password
    """

    def get_keyword_names(self):
        return ['change_password',
                ]

    def _open_page(self):
        self._navigate_to('Options', 'Change Passphrase')

    def _fill_lines(self, old_password, new_password, generate_passphrase):

        RADIO_BUTTON_GENERATE = 'sys_gen'
        RADIO_BUTTON_CHANGE = 'change'
        BUTTON_GENERATE = "//input[@value='Generate']"
        TEXT_GENERATED_PASSWD = "//input[@id='sysgen']"
        self.input_text(OLD_PASSWORD_TEXTBOX, old_password)
        if generate_passphrase is not None and \
                (str(generate_passphrase).lower() == 'y' or \
                 str(generate_passphrase).lower() =='yes'):
            if self._is_element_present(RADIO_BUTTON_CHANGE):
                self._click_radio_button(RADIO_BUTTON_CHANGE)
            self._click_radio_button(RADIO_BUTTON_GENERATE)
            self.click_button(BUTTON_GENERATE)

            return self.get_value(TEXT_GENERATED_PASSWD)

        else:
            self.input_text(NEW_PASSWORD_TEXTBOX, new_password)
            self.input_text(RETYPE_NEW_PASSWORD_TEXTBOX, new_password)

    def change_password(self, old_password, new_password=None, generate_passphrase=None):
        """ Change user password.

        *Parameters*
            - `old_password`: current password.
            - `new_password`: new password.

        *Return*
            None.

        *Exceptions*
            None.

        *Examples*
	    | Change Password | strong_pass | stronger_pass |
            | Change Password | long_pass | longer_pass |
            | ${sys_gen_passwd}= | Change Password | generate_passphrase=yes |
        """

        self._open_page()

        sys_gen_passwd = self._fill_lines(old_password, new_password, generate_passphrase)
        self._click_submit_button()
        return sys_gen_passwd

