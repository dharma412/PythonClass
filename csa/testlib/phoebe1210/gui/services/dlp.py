#!/usr/bin/env python

import time
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

DEFAULT_PATH = lambda hostname: 'https://%s' % (hostname,)
enable_dlp_wizard_cb = "id=dlp_wizard"
content_tracking_cb = "//input[@id='content_tracking_local']"
disable_dlp_cb = "id=enabled"
enable_dlp_btn = "action:FormEnable"
accept_license_btn = "name=action:AcceptLicense"
edit_settings_btn = "name=action:FormEdit"
dlp_settings_table = "xpath=//table[@class='pairs']"
dlp_mode_dd = "xpath=//select[@id='dlp_mode']"
em_host_port_tb = "name=em_server"
em_lcl_service_port_tb = "name=local_port"
em_enable_ssl_cb = "name=ssl_comunication"
em_server_cert_dd = "id=server_cert"
em_client_cert_dd = "id=client_cert"
em_enable_finger_cb = "id=fingerprinting"


class rsa_email_dlp(GuiCommon):

    def get_keyword_names(self):
        return ['dlp_enable',
                'dlp_disable',
                'dlp_edit_settings',
                'dlp_is_enabled',
                ]

    def _open_page(self):
        self.go_to(DEFAULT_PATH(self.dut))
        self._navigate_to('Security Services', 'Data Loss Prevention')

    def dlp_enable(self, enable_matched_content_logging=None):

        """ This function enables DLP along with configuring global settings.

        *Parameters*
            - `enable_matched_content_logging`: Enable matched content logging
              or not. Boolean.

        *Return*
             None
        """
        self._info('Enabling DLP')

        if not self.dlp_is_enabled():
            self.click_button(enable_dlp_btn)
            if self._is_text_present('License Agreement'):
                self.click_button(accept_license_btn)
        else:
            self.click_button(edit_settings_btn)
        self._click_submit_button()

    def _fill_dlp_page(self, enable_matched_content_logging=None):

        if enable_matched_content_logging is not None:
            if not self._is_element_present(content_tracking_cb):
                raise guiexceptions.GuiFeatureDisabledError(
                    "Message Tracking is disabled")
            self._set_checkbox(enable_matched_content_logging,
                               content_tracking_cb)

    def dlp_disable(self, ):
        """ This function disables DLP.
        """
        if not self.dlp_is_enabled():
            return
        self._info('Disabling DLP')
        self.click_button(edit_settings_btn)
        self.unselect_checkbox(disable_dlp_cb)
        self._click_submit_button()

    def dlp_edit_settings(self, enable_matched_content_logging=None):
        """ This function edits DLP settings.
        *Parameters*
            - `enable_matched_content_logging`: Enable matched content logging
              or not. Boolean.

        *Return*
             None
        """
        self._info('Editing DLP settings')

        if not self.dlp_is_enabled():
            raise guiexceptions.GuiFeatureDisabledError(
                "DLP is not enabled")
        self.click_button(edit_settings_btn)
        self._fill_dlp_page(enable_matched_content_logging)
        self._click_submit_button()

    def dlp_is_enabled(self):

        """ This function returns True if DLP is already enabled.

        *Return*
            True if DLP is enabled else False
        """
        self._open_page()
        enabled_text = self.get_text("%s/tbody/tr[1]/td"
                                     % dlp_settings_table)
        if 'enable' in enabled_text.lower():
            return True
        return False
