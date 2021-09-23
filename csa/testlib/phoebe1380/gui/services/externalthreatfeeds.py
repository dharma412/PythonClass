#!/usr/bin/env python

import time
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

DEFAULT_PATH = lambda hostname: 'https://%s' % (hostname,)

EDIT_SETTINGS_BUTTON  = "//input[@value='Edit Settings...']"
EXTERNAL_THREATFEEDS_CB = "//*[@id='enable_etf']"
EXTERNAL_THREATFEEDS_SETTINGS_TABLE="xpath=//table[@class='pairs']"
ETF_CUSTOM_HEADER_YES = "//*[@id='add_header_enabled']"
ETF_CUSTOM_HEADER_NO = "//*[@id='add_header_disabled']"
ETF_HEADER_VALUE = "id=custom_header_value"
ETF_HEADER_NAME = "id=custom_header_name"
SUBMIT_BUTTON= "//*[@type='button' and @value='Submit']"

class external_threatfeeds(GuiCommon):

    def get_keyword_names(self):
        return ['external_threatfeeds_enable',
                'external_threatfeeds_disable',
                'external_threatfeeds_is_enabled',
               ]

    def _open_page(self):
        self.go_to(DEFAULT_PATH(self.dut))
        self._navigate_to('Security Services', 'External Threat Feeds')


    def external_threatfeeds_enable(self, *args):

        """ This function enables External threatfeeds  along with configuring global settings.

        *Parameters*
            - `custom_header`: Do you want to use custom header?
            - `header_name`: Header name
            - `header_value`: Header Value

        *Return*
             None
        """
        self._info('Enabling External Threat Feeds')

        settings = self._parse_args(args)
        if not self.external_threatfeeds_is_enabled():
            self.click_button(EDIT_SETTINGS_BUTTON)
            self.click_button(EXTERNAL_THREATFEEDS_CB, "don't wait")
            if settings.has_key('custom_header'):
                if 'yes' in settings['custom_header'].lower():
                    self._click_radio_button(ETF_CUSTOM_HEADER_YES)
                    if settings.has_key('header_name'):
                        self.input_text(ETF_HEADER_NAME, settings['header_name'])
                    if settings.has_key('header_value'):
                        self.input_text(ETF_HEADER_VALUE, settings['header_value'])
                else:
                    self._click_radio_button(ETF_CUSTOM_HEADER_NO)
            self.click_button(SUBMIT_BUTTON, "don't wait")

    def external_threatfeeds_disable(self, *args):
        """ This function disables External Threatfeeds.
        """

        settings = self._parse_args(args)
        if not self.external_threatfeeds_is_enabled():
            return
        self._info('Disabling External Threatfeeds')
        self.click_button(EDIT_SETTINGS_BUTTON)
        if settings.has_key('custom_header'):
            if 'no' in settings['custom_header'].lower():
                self._click_radio_button(ETF_CUSTOM_HEADER_NO)
        self.unselect_checkbox(EXTERNAL_THREATFEEDS_CB)
        #self.click_button(EXTERNAL_THREATFEEDS_CB, "don't wait")
        self.click_button(SUBMIT_BUTTON, "don't wait")

    def external_threatfeeds_is_enabled(self):

        """ This function returns True if external threatfeeds is already enabled.

        *Return*
            True if external threatfeed is enabled else False
        """
        self._open_page()
        enabled_text = self.get_text("%s/tbody/tr[1]/td"
          %EXTERNAL_THREATFEEDS_SETTINGS_TABLE)
        if 'enabled' in enabled_text.lower():
            return True
        return False
