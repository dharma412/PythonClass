#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/services/socks_proxy.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $
import time
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

ENABLE_SOCKS_CHECKBOX = 'enabled'

class SocksProxy(GuiCommon):
    """Socks Proxy Settings page interaction class."""

    def get_keyword_names(self):
        return ['socks_proxy_enable',
                'socks_proxy_disable',
                'socks_proxy_edit_settings',]

    def _open_page(self):
        """Open 'SOCKS Proxy Management page' """
        self._navigate_to('Security Services', 'SOCKS Proxy')

    def socks_proxy_enable(self,
            socks_ports=None,
            udp_request_ports=None,
            tunnel_negotiation_timeout=None,
            ):
        """Enables Socks Proxy Settings.

        Parameters:
        - `socks_ports`: SOCKS Control Ports that may be used by a SOCKS client
          to establish a control connection with the SOCKS proxy. Enter port
          numbers separated by commas.
        - `udp_request_ports`: set ports for udp request.
        - `tunnel_negotiation_timeout`: set timeout in seconds.

        Example:
        | Socks Proxy Enable |
        | Socks Proxy Enable | socks_ports=1200 | udp_request_ports=100-100 |
        """

        enable_socks_button = "xpath=//input[@value='Enable and Edit Settings...']"
        self._open_page()
        if self._check_feature_status(feature='socks_proxy'):
            return
        self.click_button(enable_socks_button)
        self._set_socks_ports(socks_ports)
        self._set_udp_request_ports(udp_request_ports)
        self._set_tunnel_negotiation_timeout(tunnel_negotiation_timeout)
        self._click_submit_button()

    def _set_socks_ports(self, socks_ports=None):

        socks_ports_field = 'ports'
        if socks_ports:
            self.input_text(socks_ports_field, socks_ports)

    def _set_udp_request_ports(self, udp_request_ports=None):

        udp_request_ports_field = 'udp_request_ports'
        if udp_request_ports:
            self.input_text(udp_request_ports_field, udp_request_ports)

    def _set_tunnel_negotiation_timeout(self, tunnel_negotiation_timeout=None):

        timeout_field = 'negotiation_timeout'

        if tunnel_negotiation_timeout:
            self.input_text(timeout_field, tunnel_negotiation_timeout)

    def _confirm_disable(self):
        BUTTON = "xpath=//button[text() = 'Disable SOCKS Proxy']"

        try:
            self._info("confirm button")
            self.click_element(BUTTON, "don't wait")
        except:
            self._info("Expected confirmation screen %s did not appear" % BUTTON)
        time.sleep(3)
        self._check_action_result()

    def socks_proxy_disable(self):
        """Disables Socks proxy.

        Example:
        | Socks Proxy Disable |
        """
        self._open_page()
        if not self._check_feature_status(feature='socks_proxy'):
            return
        self._click_edit_settings_button()
        self.unselect_checkbox(ENABLE_SOCKS_CHECKBOX)
        self._click_submit_button(check_result=False, wait=False)
        self._confirm_disable()

    def socks_proxy_edit_settings(self,
            socks_ports=None,
            udp_request_ports=None,
            tunnel_negotiation_timeout=None,
            ):
        """Edits Socks Proxy Settings.

        Parameters:
        - `socks_ports`: set ports used by a SOCKS client.
        - `udp_request_ports`: set ports for udp request.
        - `tunnel_negotiation_timeout`: set timeout in seconds.

        Example:
        | Socks Proxy Edit Settings  | tunnel_negotiation_timeout=4 | udp_request_ports=16000-16100 |
        """

        self._open_page()
        if not self._check_feature_status(feature='socks_proxy'):
            raise guiexceptions.GuiFeatureDisabledError\
                ('Cannot edit Socks proxy settings as disabled')
        self._click_edit_settings_button()
        self._set_socks_ports(socks_ports)
        self._set_udp_request_ports(udp_request_ports)
        self._set_tunnel_negotiation_timeout(tunnel_negotiation_timeout)
        self._click_submit_button()
