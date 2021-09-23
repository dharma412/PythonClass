#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/gui/help/remote_access.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

ENABLE_BUTTON='xpath=//input[@value="Enable..."]'
DISABLE_BUTTON='xpath=//input[@value="Disable"]'
PASSWORD_TEXTBOX='id=password_id'
SECURE_TUNNEL_CHECKBOX='id=tunnel_id'
SECURE_TUNNEL_PORT_TEXTBOX='id=port_id'
GENERATE_SEED_STRING= 'id=seed_string_gen'
USER_SEED_STRING= 'id=seed_string_user'

class RemoteAccess(GuiCommon):

    """
        Keyword library for menu Help and Support -> RemoteAccess
    """

    def get_keyword_names(self):
        return ['remote_access_enable',
                'remote_access_disable',
               ]

    def _open_page(self):
        self._navigate_to('Help and Support', 'Remote Access')

    def _click_enable(self):
        if self._is_element_present(DISABLE_BUTTON) :
            raise guiexceptions.ConfigError, ("Remote support already has"
                +" been enabled")
        else:
            self.click_button(ENABLE_BUTTON, "don't wait")

    def _click_disable(self):
        if self._is_element_present(ENABLE_BUTTON) :
            raise guiexceptions.ConfigError, ("Remote support already has"
                +" been disabled")
        else:
            self.click_button(DISABLE_BUTTON, "don't wait")

    def _fill_passwd(self, password):
        self.input_text(PASSWORD_TEXTBOX, password)

    def _secure_tunnel(self, enable, port):
        if isinstance(enable, bool):
            if enable:
                self.select_checkbox(SECURE_TUNNEL_CHECKBOX)
                self.input_text(SECURE_TUNNEL_PORT_TEXTBOX, int(port))
            else:
                self.unselect_checkbox(SECURE_TUNNEL_CHECKBOX)
        else:
            raise ValueError ('secure_tunnel value must be boolean object or'+
                    ' None. Given argument is %s' % (enable,))

    def remote_access_disable(self):
        """Disable Remote Access to your appliance.

        *Parameters*
            None.

        *Return*
            None.

        *Exceptions*
            - `ConfigError`: if remote support already have been disabled.

        *Examples*
            | Remote Access Disable |
        """
        self._open_page()

        self._click_disable()

    def remote_access_enable(self,seed_string= None , password="default_pass",
             secure_tunnel=None, port=25):
        """Remote Access gives Cisco IronPort Support remote access to your
            appliance.

        *Parameters*
            - `password`: password for remote access.
                Password must satisfy password policy.
                Default password is default_pass
            - `secure_tunnel`: enable or disable securetunnel.
                Put boolean object as argument to enable or disable
                Secure Tunel. None to left this option unchanged. Default
                value is None
            - `port`: use this argument only if securetunnel is enabled.

        *Return*
            None.

        *Exceptions*
            - `ConfigError`: if remote support already have been enabled.
            - `ValueError` : if secure_tunnel isn't boolean or None object.

        *Examples*
            | Remote Access Enable | password=password | secure_tunnel=${True} |
            | ... | port=45 |
            | Remote Access Enable | password=password | secure_tunnel=${None} |
            | Remote Access Enable |
        """
        self._open_page()

        self._click_enable()

        if seed_string == None:
           self._click_radio_button(GENERATE_SEED_STRING)

        if seed_string == 'user':
           self._click_radio_button(USER_SEED_STRING)
           self._fill_passwd(password)

        if secure_tunnel != None :
            self._secure_tunnel(secure_tunnel, port)

        self._click_submit_button()
