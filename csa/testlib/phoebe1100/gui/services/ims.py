#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/services/ims.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon

ENABLE_BUTTON = '//input[@value="Enable..."]'
ACCEPT_LICENSE = 'action:AcceptLicense'
ENABLE_CHECKBOX = 'enabled'
EDIT_BUTTON = '//input[@value="Edit Global Settings..."]'
SAVE_SETTINGS_BUTTON = 'SaveSettings'
UPDATE_BUTTON = 'action:UpdateNow'
RESULTS_MESSAGE = 'action-results-message'
SMALL_MSG_SIZE = 'adv_msg_size'
MAX_MSG_SIZE = 'max_msg_size'
TIMEOUT = 'timeout'
REG_SCAN = lambda reg_scan: 'region_enable_%s' % reg_scan
REGION_ENABLE_ON = 'region_enable_on'
REGION = 'region'
SCAN_REGION = lambda scan_region: 'label=%s' % scan_region


class Ims(GuiCommon):
    """
    This libarary is designed to interact with GUI elements of
    Security Services -> IMS page
    """

    def get_keyword_names(self):
        return ['ims_enable',
                'ims_disable',
                'ims_update',
                'ims_edit']

    def _open_page(self):
        self._info('Opening IMS page')
        self._navigate_to('Security Services', 'IronPort Intelligent Multi-Scan')

    def _is_enabled(self):
        self._open_page()
        disabled_str = "IronPort Intelligent Multi-Scan is currently disabled globally."
        return not self._is_text_present(disabled_str)

    @set_speed(0)
    def ims_enable(self):
        """
            Enables IronPort Intelligent Multi-Scan

            *Parameter*:
              None

            *Return*:
              None

            *Examples*:
              | IMS Enable |
        """
        self._info("Enabling IronPort Intelligent Multi-Scan")
        if self._is_enabled():
            self._info("IronPort Intelligent Multi-Scan is already enabled")
            return
        self.click_button(ENABLE_BUTTON)
        if self._is_text_present('License Agreement'):
            self.click_button(locator=ACCEPT_LICENSE)

    @set_speed(0)
    def ims_disable(self):
        """
           Disables IronPort Intelligent Multi-Scan

           *Parameter*:
             None

           *Return*:
             None

           *Examples*:

             | IMS Disable |
        """

        self._info("Disabling IronPort Intelligent Multi-Scan")
        if not self._is_enabled():
            self._info("IronPort Intelligent Multi-Scan is already disabled")
            return
        self.click_button(EDIT_BUTTON)
        self._unselect_checkbox(ENABLE_CHECKBOX)
        self.click_button(locator=SAVE_SETTINGS_BUTTON)

    @set_speed(0)
    def ims_update(self):
        """initiate manual update of IMS

           *Parameter*:
             None

            *Return*:
            Result message of update action if action is successful else none.

           *Examples*:
               | IMS Update |
        """
        if self._is_enabled():
            self.click_button(locator=UPDATE_BUTTON)
            return self.get_text(locator=RESULTS_MESSAGE)
        else:
            return None

    @set_speed(0)
    def ims_edit(self,
                 small_mesg_size=None,
                 max_mesg_size=None,
                 timeout=None,
                 reg_scan=None,
                 reg_scan_region=None):
        """Edit IMS settings.

           *Parameters*:
            - `small_mesg_size` : Always scan messages smaller than
            - `max_mesg_size` : Never scan messages larger than
            - `timeout` : Timeout for Scanning Single Message
            - `reg_scan` : Regional Scanning. on or off
            - `reg_scan_region` : Regional Scanning Region
                  Values can be China

           *Return*:
             None

           *Examples*:
           | IMS EDIT | small_mesg_size=256k | max_mesg_size=512k |
           | IMS EDIT | timeout=120 | reg_scan=on | reg_scan_region=China |
        """
        if self._is_enabled():
            self.click_button(EDIT_BUTTON)
            if small_mesg_size:
                self.input_text(locator=SMALL_MSG_SIZE, text=small_mesg_size)
            if max_mesg_size:
                self.input_text(locator=MAX_MSG_SIZE, text=max_mesg_size)
            if timeout:
                self.input_text(locator=TIMEOUT, text=timeout)
            if reg_scan:
                # phoebe 7.6.0-444 has these options, while phoebe 7.6.1-022 does not
                if self._is_element_present(REG_SCAN(reg_scan.lower())):
                    self._click_radio_button(REG_SCAN(reg_scan.lower()))
                    if reg_scan_region and self._is_checked(locator=REGION_ENABLE_ON):
                        self.select_from_list(REGION, SCAN_REGION(reg_scan_region))
            self.click_button(SAVE_SETTINGS_BUTTON)
