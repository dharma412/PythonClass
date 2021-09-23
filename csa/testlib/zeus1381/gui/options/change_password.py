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

    def _fill_lines(self, old_password, new_password):
        self.input_text(OLD_PASSWORD_TEXTBOX, old_password)
        self.input_text(NEW_PASSWORD_TEXTBOX, new_password)
        self.input_text(RETYPE_NEW_PASSWORD_TEXTBOX, new_password)

    def change_password(self, old_password, new_password):
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
        """
        self._open_page()

        self._fill_lines(old_password, new_password)

	self._click_submit_button()
