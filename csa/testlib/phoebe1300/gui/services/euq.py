#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/gui/services/euq.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.gui.guicommon import GuiCommon
from common.util.sarftime import CountDownTimer
import time

ENABLE_BUTTON = "action:FormEditQuarantine"
ENABLE_CHECKBOX = "esq_enabled"
COMMON_SUBMIT_BUTTON = "//*[@type='submit' and @value='Submit']"
COMMON_CONFIRM_DIALOG = "//*[@id='confirmation_dialog']"
COMMON_CONFIRM_OK_CANCEL_BUTTON = lambda text: "%s//button[text()='%s']" % (COMMON_CONFIRM_DIALOG, text)


class euq(GuiCommon):

    def get_keyword_names(self):
        return ['euq_enable',
                'euq_disable',
                'euq_edit_settings']

    def _open_page(self):
        self._info('Opening External Spam Quarantine page')
        self._navigate_to('Security Services', 'Spam Quarantine')

    def euq_enable(self, name, euq_host, port=None, enable_slbl=None, action=None):
        """
            Enables External Spam Quarantine

            *Parameter*:
              - `name` - name for EUQ service, string
              - `euq_host` - ip address of external host, ipaddress format
              - `port` - port on which euq host is listening, integer
              - `enable_slbl` - True to Enable End User Safelist/Blocklist Feature and
                        False to disable it.
              `action` - Blocklist action, String

            *Return*:
              None

            *Examples*:

              | EUQ Enable | Spam_Quarantine | 10.1.1.1 | 6025 | True | Delete |
              | EUQ Enable | euq_test | 10.1.1.2 |
        """
        self._info("Enabling External Spam Quarantine")
        if self._is_enabled():
            self._info("External Spam Quarantine is already enabled")
            return
        self.click_button(ENABLE_BUTTON)
        self._select_checkbox(ENABLE_CHECKBOX)
        self._edit_settings(name, euq_host, port, enable_slbl, action)

    def euq_disable(self):
        """
           Disables External Spam Quarantine

           *Parameter*:
             None

           *Return*:
             None

           *Examples*:

             | EUQ Disable |   |
        """

        self._info("Disabling External Spam Quarantine")
        if not self._is_enabled():
            self._info("External Spam Quarantine is already disabled")
            return
        self.click_button(ENABLE_BUTTON)
        self._unselect_checkbox(ENABLE_CHECKBOX)
        self._click_submit_button()

    def _is_enabled(self):
        self._info("Checking if External Spam Quarantine is enabled")
        self._open_page()
        return not self._is_text_present("No external spam quarantine is defined.")

    def euq_edit_settings(self, name=None, euq_host=None, port=None, enable_slbl=None, action=None):
        """
            Edit External Spam Quarantine

            *Parameter*:
              - `name` - name for EUQ service, string
              - `euq_host` - ip address of external host, ipaddress format
              - `port` - port on which euq host is listening, integer
              - `enable_slbl` - True to Enable End User Safelist/Blocklist Feature and
                        False to disable it.
              - `action` - Blocklist action, String

            *Return*:
              None

            *Examples*:

              | EUQ Edit Settings | action=delete |   |   |   |   |
              | EUQ Edit Settings | My EUQ | 10.1.1.2 | 6025 | True | Quarantine |
        """
        self._info("Editing External Spam Quarantine settings")
        self._open_page()
        self.click_button(ENABLE_BUTTON)
        self._edit_settings(name, euq_host, port, enable_slbl, action)

    def _edit_settings(self, name, euq_host, port, enable_slbl, action):
        NAME = 'name'
        HOST = 'host'
        PORT = 'port'
        SLBL = 'enable_slbl'
        ACTION = 'slbl_blocklist_action'
        if name:
            self.input_text(NAME, name)
        if euq_host:
            self.input_text(HOST, euq_host)
        if port:
            self.input_text(PORT, port)
        if enable_slbl != None:
            if enable_slbl:
                self._select_checkbox(SLBL)
            else:
                self._unselect_checkbox(SLBL)
        if action:
            self.select_from_list(ACTION, action.title())
        self.click_button(COMMON_SUBMIT_BUTTON, "don't wait")

        tmr = CountDownTimer(5).start()
        while tmr.is_active():
            time.sleep(1)
            if self._is_element_present(COMMON_CONFIRM_DIALOG) and \
                    self._is_visible(COMMON_CONFIRM_DIALOG):
                self.click_button \
                    (COMMON_CONFIRM_OK_CANCEL_BUTTON('Continue'))
                break
