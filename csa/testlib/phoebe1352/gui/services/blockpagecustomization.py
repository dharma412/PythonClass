#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/services/blockpagecustomization.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $
from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon

ENABLE_BUTTON =  "//input[@value='Enable...']"
ENABLE_CHECKBOX = "//input[@id='eun_enabled']"
LOGO_URL = "//input[@name='logo']"
COMPANY_NAME = "//input[@name='company_name']"
CONTACT_INFORMATION = "//input[@name='contact_info']"
DEFAULT_LANGUAGE = "//select[@name='lang']"
SETTINGS_BUTTON = "//input[@value='Edit Settings...']"
SERVICE_DISABLED_FLAG = '//dl[@class="box"]//div[@class="text-info"]'
SETTINGS_TABLE = "//table[@class='cols']"

class blockPageCustomization(GuiCommon):
    """Keywords are used to disable/enable
       Block Page Customization and to edit its settings
    """

    def get_keyword_names(self):
        return ['block_page_customization_enable',
                'block_page_customization_disable',
                'block_page_customization_is_enabled',
                'block_page_customization_edit_settings',
                'block_page_customization_get_details']

    def _open_page(self):
        self._navigate_to('Security Services', "Block Page Customization")

    def block_page_customization_enable(self, logo_url=None, company_name=None, contact_info=None, default_lang=None):
        """Enables Block Page Customization Service with details

        Parameters:
         - logo_url: Enter the logo in URL
         - company_name: Enter the Company name
         - contact_info: Enter the Contact Information
         - default_lang: Select the Default language
         *Example*:
         | Block Page Customization Enable | logo_url=http://cisco.com | company_name=Cisco | contact_info=1234 | default_lang=en-us |
        """
        self._info('Enabling Block Page Customization')
        self._open_page()
        if self.block_page_customization_is_enabled():
            self._info('Block Page Customization is already enabled')
            return
        self.click_button(ENABLE_BUTTON)
        self._select_checkbox(ENABLE_CHECKBOX)
        self._edit_settings(logo_url, company_name, contact_info, default_lang)

    def block_page_customization_disable(self):
        """Disables Block Page Customization Service
        *Example*:
        | Block Page Customization Disable |
        """
        self._info('Disabling Block Page Customization Service')
        self._open_page()
        if not self.block_page_customization_is_enabled():
            self._info('Block Page Customization is already disabled')
            return
        self.click_button(SETTINGS_BUTTON)
        self._unselect_checkbox(ENABLE_CHECKBOX)
        self._click_submit_button()

    def block_page_customization_is_enabled(self):
        """Check whether Block Page Customization is enabled or not
        Return:
            Boolean True or False
        *Example*:
        | Block Page Customization Is Enabled |
        """
        self._info('Checking if Block Page Customization service is enabled')
        self._open_page()
        return not self._is_element_present(SERVICE_DISABLED_FLAG)

    @set_speed(0)
    def block_page_customization_edit_settings(self, logo_url=None, company_name=None, contact_info=None, default_lang=None):
        """Edits Block Page Customization Service settings

        Parameters:
         - logo_url: Enter the logo in URL
         - company_name: Enter the Company name
         - contact_info: Enter the Contact Information
         - default_lang: Select the Default language
        *Example*:
        | Block Page Customization Edit Settings | logo_url=http://abc.com | company_name=abc | contact_info=6578 | default_lang=it |
        """
        self._info("Editing Block Page Customization Service settings")
        self._open_page()
        self.click_button(SETTINGS_BUTTON)
        self._edit_settings(logo_url, company_name, contact_info, default_lang)

    def _edit_settings(self, logo_url=None, company_name=None, contact_info=None, default_lang=None):
        if logo_url is not None:
            self.input_text(LOGO_URL, logo_url)
        if company_name is not None:
            self.input_text(COMPANY_NAME, company_name)
        if contact_info is not None:
            self.input_text(CONTACT_INFORMATION, contact_info)
        if default_lang is not None:
            self.select_from_list(DEFAULT_LANGUAGE, default_lang)
        self._click_submit_button()

    def block_page_customization_get_details(self):
        """Collects information related to Block Page Customization Service

        *Return:*
        Dictionary where keys are:

        | Logo URL |
        | Company Name |
        | Contact Information |
        | Default Language |

        *Examples:*
        | ${details}= | Block Page Customization Get Details |
        | ${settings}= | Get From Dictionary | ${details} | Settings |
        | Log | ${settings} |
        """
        self._open_page()
        if not self.block_page_customization_is_enabled():
            self._info('Block Page Customization is disabled')
            return
        status_info = {}
        status_info['Settings'] = self._get_settings()
        return status_info

    def _get_settings(self):
        settings = {}
        for row in xrange(1, 5):
            key = self.get_text("%s/tbody/tr[%d]/th" % \
                                (SETTINGS_TABLE, row)).strip()
            value = self.get_text("%s/tbody/tr[%d]/td" % \
                                (SETTINGS_TABLE, row)).strip()
            settings[key] = value
        return settings
