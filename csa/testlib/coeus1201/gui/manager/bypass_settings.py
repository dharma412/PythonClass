#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/bypass_settings.py#2 $
# $DateTime: 2020/02/05 22:05:56 $
# $Author: sarukakk $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from constants import applications

PROXY_BYPASS_SETTINGS_BUTTON = 'xpath=//input[@value="Edit Proxy Bypass Settings..."]'
APPLICATION_BYPASS_SETTINGS_BUTTON = 'xpath=//input[@value="Edit Application Bypass Settings..."]'
BYPASS_LIST_TEXTBOX = 'xpath=//textarea[@id="bypass_list"]'
CUSTOM_URL_CATGORIES_LINK = 'xpath=//a[contains(@onclick, \'ListCustomCat\')]'
EDIT_CUSTOM_URL_CATGORIES_BUTTON = 'xpath=//input[@value="Done"]'

APPLICATIONS_MAP = {applications.WEBEX.name: 'id=webex_bypass_enabled'}


class BypassSettings(GuiCommon):
    """Keywords for interaction with 'Web Security Manager -> Bypass Settings'
       page.
    """

    def get_keyword_names(self):
        return ['proxy_bypass_edit',
                'proxy_bypass_edit_url_categories',
                'proxy_bypass_application_edit',
                'proxy_bypass_get_settings',
                ]

    def _open_proxy_bypass_page(self):
        """Open 'Proxy Bypass page'."""
        self._navigate_to('Web Security Manager', 'Bypass Settings')

    def _is_proxy_bypass_available(self):
        return self._is_element_present(PROXY_BYPASS_SETTINGS_BUTTON)

    def _click_edit_proxy_bypass_button(self):
        self.click_button(PROXY_BYPASS_SETTINGS_BUTTON)


    def _fill_bypass_sites(self, bypass_list):
        """Fill in Proxy Bypass List textbox."""
        try:
            text = ', '.join(bypass_list)
        except:
            raise ValueError('bypass_list should be either tuple or '
                             'list of strings')

        self.input_text(BYPASS_LIST_TEXTBOX, text)

    def _click_edit_apps_bypass_button(self):
        self.click_button(APPLICATION_BYPASS_SETTINGS_BUTTON)

    def _click_custom_url_catgories_link(self):
        self.click_element(CUSTOM_URL_CATGORIES_LINK)

    def _edit_apps_scanning_to_bypass(self, apps_dict):
        for application, enable in apps_dict.iteritems():
            if application not in APPLICATIONS_MAP:
                raise ValueError('"%s" application does not exist' %
                                 (application,))
            if enable:
                self.select_checkbox(APPLICATIONS_MAP[application])
            else:
                self.unselect_checkbox(APPLICATIONS_MAP[application])
    def  _select_url_categories(self,url_categories):

        SELECT_ALL_LOCATOR = lambda event: "xpath=//a[contains(@onclick, \'%s\')]" % (event,)

        # Add the code on else part to select individual category .Currently this not requried hence code is not handled that
        for index, category_type in enumerate(url_categories):
            if category_type == 'all':
                # Set which select-all has to be clicked - cust cat or predefined cat
                if index == 0:
                    onclick_event_name = 'memberscustomcat'

                self._wait_until_element_is_present(SELECT_ALL_LOCATOR(onclick_event_name))
                self.click_element(SELECT_ALL_LOCATOR(onclick_event_name))

        self.click_button(EDIT_CUSTOM_URL_CATGORIES_BUTTON)

    def proxy_bypass_edit(self, bypass_list):
        """Edit the proxy bypass list.

        :Parameters:
        - `bypass_list`: a comma separated values of domains/subnets
                         being bypassed.

        Example:
        | Proxy Bypass Edit | 10.7.11.48/24,example.com |
        | Proxy Bypass Edit | crm.example.com |
        """

        self._open_proxy_bypass_page()

        if not self._is_proxy_bypass_available():
            raise self.guiexceptions.GuiFeatureDisabledError('Proxy must be '\
                   'in transparent mode in order to use proxy bypass feature.')

        self._click_edit_proxy_bypass_button()
        self._fill_bypass_sites(self._convert_to_tuple(bypass_list))
        self._click_submit_button()

    def proxy_bypass_edit_url_categories(self, url_categories):
        """Edit the custom url categories.

        :Parameters:
        - `url_categories`: a comma separated values of custom url catgories
                         being bypassed.

        Example:
        | Proxy Bypass Edit URL Categories | all|
        """

        self._open_proxy_bypass_page()

        if not self._is_proxy_bypass_available():
            raise self.guiexceptions.GuiFeatureDisabledError('Proxy must be '\
                   'in transparent mode in order to use proxy bypass feature.')

        self._click_edit_proxy_bypass_button()
        self._click_custom_url_catgories_link()
        self._select_url_categories(self._convert_to_tuple(url_categories))
        self._click_submit_button()

    def proxy_bypass_application_edit(self, apps_bypass):
        """Edit application scanning bypass settings.

        :Parameters:
        - `apps_bypass`: a comma separated values of application
                         names and boolean values separated by ':'. Values are
                         boolean variables which enables or disables bypass
                         scanning for the application to bypass. Example:
                         'WebEx:True, Apps:False, Mcaff:True'
        | Variables | constants.py |
        ...
        | Proxy Bypass Application Edit | ${applications.WEBEX.name}:${True} |
        """

        self._open_proxy_bypass_page()
        self._click_edit_apps_bypass_button()
        apps_dict = {}
        for l in self._convert_to_tuple(apps_bypass):
            apps = [item.strip() for item in l.split(':')]
            apps_dict[str(apps[0])] = eval(apps[-1])
        self._edit_apps_scanning_to_bypass(apps_dict)
        self._click_submit_button()

    def proxy_bypass_get_settings(self):
        """
        Returns a dictionary of proxy bypass settings with the following keys:
        - proxy
        - application_scanning

        Parameters: None

        Example of usage:
        | ${settings}= | Proxy Bypass Get Settings |
        | Log | ${settings} |
        | Should Contain | ${settings}['proxy'] | 10.0.0.1 |
        """
        PROXY_SETTINGS = "xpath=//th[contains(text() , 'Proxy')]/../td"
        APPLICATION_SETTINGS = "xpath=//th[contains(text() , 'Cisco')]/../td"
        result={}
        self._open_proxy_bypass_page()
        result['proxy'] = self._get_text(PROXY_SETTINGS)
        result['application_scanning'] = self._get_text(APPLICATION_SETTINGS)
        return result

