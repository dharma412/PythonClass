#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/manager/custom_url_categories.py#2 $
# $DateTime: 2020/02/28 02:14:38 $
# $Author: kathirup $

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
import time

class CustomUrlCategories(GuiCommon):
    """Custom Url Categories Settings page interaction class.
    'Web Security Manager -> Custom Url Categories' section.
    """

    name_column = 2
    view_content_column = 5
    delete_column = 6

    table_id = "//table[@class='cols']"

    def get_keyword_names(self):
        return ['custom_url_category_add',
                'custom_url_category_delete',
                'custom_url_category_edit',
                'custom_url_category_get_list',
                'external_custom_url_category_view_content',
                ]

    def custom_url_category_get_list(self):
        """
        Returns: list of custom url categories

        Examples:

        | ${policies}= | Custom URL Category Get List |
        | Should Be True | len(${policies}) == 2 |
        | Should Be True | 'category1' in ${policies} |
        """
        self._open_page()
        return self._get_policies().keys()

    def custom_url_category_add(self,
                                name,
                                sites=None,
                                order=1,
                                regexes=None,
                                feed_type="local",
                                route="Management",
                                ext_feed_type="cisco_feed",
                                protocol="https",
                                ext_feed_location=None,
                                ext_feed_server_auth=None,
                                start_test="false",
                                ext_feed_auto_update=None):
        """Adds the custom URL category

        Parameters:
        - `feed_type`: local or external
        - `route`: Management or Data
        - `ext_feed_type`: external feed type, values either cisco_feed or office_365
        - `name`: name of the custom URL category. Mandatory.
        - `order`: processing order. Optional, '1' by default.
        - `sites`: partial urls or IP addresses the category should match.
                A string with comma separated values. Define either a URL
                or regular expression. At least one of these
                fields must contain a value.
        - `regexes`: regular expressions for the urls the category
                should match. A string with comma separated values. Define either a URL
                or regular expression. At least one of these
                fields must contain a value.
        - `protocol` : Protocol type
        - `ext_feed_location`: External feed location or url
        - `ext_feed_server_auth`: Specify if external feed server required authentication
                in terms of username#password or none
        - `start_test` : If set to true then performs start test and retun the result, else
                false
        - `ext_feed_auto_update`: External feed autoupdate frequency in hours or none

        Return:
        Returns start test results as a string if start_test is set to true

        Example:
        | Custom Url Category Add | nameOfCategory | site1.com, site2.com | order=1 |
        | Custom Url Category Add | nameOfCategory | order=1 | regexes=regex1, regex2 |
        | Custom Url Category Add | nameOfCategory | feed_type=external | ext_feed_type=office_365 | admin#Cisco123 | 2 |
        """

        #xpaths required for selecting feed type
        FEED_TYPE_LOCATOR = "xpath=//select[@id='category_type']"
        ROUTING_TABLE_DROPDOWN = "xpath=//select[@id='interface_option']"

        feed_map = {'local':'0',
                    'external':'1',
                   }

        route_map = {'Management':'0',
                     'Data':'1',
                    }
        self._open_page()
        self._click_add_custom_cat_button()

        self._fill_name(name)
        self._fill_order(int(order))

        start_test_result = None

        #Check the feed type i.e. local or external
        if feed_type == "local":
            #Select from the list local feed option
            self.select_from_list(FEED_TYPE_LOCATOR, feed_map['local'])
            if sites is not None:
                self._fill_sites(sites)
            if regexes is not None:
                self._fill_regexes(regexes)
        elif feed_type == "external":
            #Set the external feed settings here
            self.select_from_list(FEED_TYPE_LOCATOR, feed_map['external'])
            if self._is_element_present(ROUTING_TABLE_DROPDOWN):
                self.select_from_list(ROUTING_TABLE_DROPDOWN,route_map[route])

            start_test_result = self._set_external_feed(ext_feed_type,
                                    protocol,
                                    ext_feed_location,
                                    ext_feed_server_auth,
                                    start_test,
                                    ext_feed_auto_update,
                                    sites)
        else:
            #Raise exception if invalid exception is set
            raise guiexceptions.ConfigError('Invalid feed type')

        #Click the submit button
        self._click_submit_button()

        if start_test_result:
            return start_test_result

    def _set_external_feed(self,
                           ext_feed_type="cisco_feed",
                           protocol=None,
                           ext_feed_location=None,
                           ext_feed_server_auth=None,
                           start_test="false",
                           ext_feed_auto_update=None,
                           sites=None):

        #Set the external feed in custom category

        #xpaths required for setting external feed

        EXT_FEED_TYPE_LOCATOR = lambda feed_type: "xpath=//*[@id='%s']" % (feed_type,)
        PROTOCOL_LOCATOR = "xpath=//*[@id='protocol_type']"
        SERVER_URL_LOCATOR = "xpath=//input[@id='feed_location']"
        ADVANCE_LINK_LOCATOR = "xpath=//*[@id='auth_arrow_closed']"
        AUTH_SERVER_UNAME_LOCATOR = "xpath=//input[@id='user_name']"
        AUTH_SERVER_PSWD_LOCATOR = "xpath=//input[@id='authPassword']"
        AUTH_SERVER_RETYPE_PSWD_LOCATOR = "xpath=//input[@id='authRetypePassword']"
        VIEW_CAT_CONTENT_LOCATOR = "xpath=//a[@id='category_content_dialog_link']"
        START_TEST_BUTTON_LOCATOR = "xpath=//input[@id='ExtFeed_start_test']"
        START_TEST_RESULT_LOCATOR = "xpath=//*[@id='ExtFeed_container']"
        NO_AUTO_UPDATE_LOCATOR = "xpath=//*[@id='no_auto_update']"
        AUTO_UPDATE_LOCATOR = "xpath=//*[@id='auto_update_freq']"
        UPDATE_FREQUENCY_VALUE_LOCATOR = "xpath=//input[@id='auto_update_freq_text']"

        protocol_map = {'https':'0',
                        'http':'1',
        }
        if sites is not None:
            self._fill_exception_sites(sites)

        #Select the external feed type either cisco_feed or office_365
        self.click_element(EXT_FEED_TYPE_LOCATOR(ext_feed_type), "don't wait")

        if ext_feed_type == "cisco_feed": #Protocol will selected only when its cisco_feed
            #Select protocol type from the list
            self.select_from_list(PROTOCOL_LOCATOR, protocol_map[protocol])

        #enter the external feed url location
        if self._is_visible(SERVER_URL_LOCATOR):
           self.input_text(SERVER_URL_LOCATOR, ext_feed_location)

        if ext_feed_server_auth:
           #Retrieve username and password
           username, password = ext_feed_server_auth.split('#')

           #Click on the advance link location
           self.click_element(ADVANCE_LINK_LOCATOR,"don't wait")

           #Enter the username and password for the external feed server
           self.input_text(AUTH_SERVER_UNAME_LOCATOR, username)

           self.input_text(AUTH_SERVER_PSWD_LOCATOR, password)

           self.input_text(AUTH_SERVER_RETYPE_PSWD_LOCATOR, password)

        #Place holder for start test results
        start_test_result = None
        if start_test == "true":

           #Click on the GetFile button to start downloading the external file
           self.click_element(START_TEST_BUTTON_LOCATOR)

           while not self._is_visible(START_TEST_BUTTON_LOCATOR):
	       pass

           start_test_result =  self.get_text(START_TEST_RESULT_LOCATOR)
           self._info(start_test_result)

        #Set the auto update of the external feed
        if ext_feed_auto_update:
            self._click_radio_button(AUTO_UPDATE_LOCATOR)
            self.input_text(UPDATE_FREQUENCY_VALUE_LOCATOR, ext_feed_auto_update)
        else:
            self._click_radio_button(NO_AUTO_UPDATE_LOCATOR)

        if start_test == "true":
            return start_test_result

    def _view_external_feed_file_content(self):
        pass

    def custom_url_category_edit(self,
                                 name,
                                 sites=None,
                                 order=None,
                                 regexes=None,
                                 feed_type="local",
                                 route="Management",
                                 ext_feed_type="cisco_feed",
                                 protocol="https",
                                 ext_feed_location=None,
                                 ext_feed_server_auth=None,
                                 start_test="false",
                                 ext_feed_auto_update=None):

        """Updates the custom URL category

        Parameters:
        - `feed_type`: local or external
        - `route`: Management or Data
        - `ext_feed_type`: external feed type, values either cisco_feed or office_365
        - `name`: name of the custom URL category. Mandatory.
        - `order`: processing order. Optional, '1' by default.
        - `sites`: partial urls or IP addresses the category should match.
                A string with comma separated values. Define either a URL
                or regular expression. At least one of these
                fields must contain a value.
        - `regexes`: regular expressions for the urls the category
                should match. A string with comma separated values. Define either a URL
                or regular expression. At least one of these
                fields must contain a value.
        - `protocol` : Protocol type
        - `ext_feed_location`: External feed location or url
        - `ext_feed_server_auth`: Specify if external feed server required authentication
                in terms of username#password or none
        - `start_test` : If set to true then performs start test and retun the result, else
                false
        - `ext_feed_auto_update`: External feed autoupdate frequency in hours or none

        Return:
        Returns start test results as a string if start_test is set to true

        Example:
        | Custom Url Category Edit | nameOfCategory | site1.com, site2.com | order=1 |
        | Custom Url Category Edit | nameOfCategory | order=1 | regexes=regex1 |
        | Custom Url Category Edit | nameOfCategory | feed_type=external | ext_feed_type=cisco_feed | admin#Cisco123 | 2 |
        """

        self._open_page()
        self._click_edit_link(name)

        start_test_result = None

        #Check the feed type i.e. local or external
        if feed_type == "local":
            if order is not None:
                self._fill_order(str(order))
            if sites is not None:
                self._fill_sites(sites)
            if regexes is not None:
                self._fill_regexes(regexes)
        elif feed_type == "external":
            route_map = {'Management':'0',
                         'Data':'1',
                        }
            ROUTING_TABLE_DROPDOWN = "xpath=//select[@id='interface_option']"
            if self._is_element_present(ROUTING_TABLE_DROPDOWN):
                self.select_from_list(ROUTING_TABLE_DROPDOWN,route_map[route])

            start_test_result = self._set_external_feed(ext_feed_type,
                                    protocol,
                                    ext_feed_location,
                                    ext_feed_server_auth,
                                    start_test,
                                    ext_feed_auto_update)

        self._click_submit_button(wait=False)

        if start_test_result:
            return start_test_result

    def custom_url_category_delete(self, name):
        """Deletes the custom URL category

        Parameters:
        - `name`: The name of the edited policy. String. Mandatory.

        Example:
        | Custom Url Category Delete | nameOfCategory |
        | Custom Url Category Delete | name=nameOfCategory |
        """

        self._open_page()
        self._click_delete_link(name)

    def external_custom_url_category_view_content(self, name):
        """Retrieves Custom url category external feed file content and returns as string
        One limitation with this keyword is that we can only use this when one external feed is configured else it will fail

        Parameters:
        - `name`: name of the custom URL category. Mandatory.

        Return:
        Returns view content text as a string

        Example:
        | ${output}=  External Custom Url Category View Content | ${custom_url_category_name}
        """

        VIEW_CONTENT_TEXTBOX_LOCATOR = "xpath=//div[@id='category_content_container']"
        CONTAINER_OK_BUTOON_LOCATOR = "xpath=//button[contains(., 'OK')]"

        self._open_page()
        self._click_view_content(name)

        view_content_text = None

        self._wait_until_element_is_present(VIEW_CONTENT_TEXTBOX_LOCATOR)
        view_content_text = self.get_text(VIEW_CONTENT_TEXTBOX_LOCATOR)
        self._info(view_content_text)

        self.click_element(CONTAINER_OK_BUTOON_LOCATOR)

        return view_content_text

    def _click_add_custom_cat_button(self):
        """Click 'Add Custom Category...' button"""
        button = "xpath=//input[@name='AddCustomCategory']"
        self.click_button(button)

    def _get_table_row_index(self, name):
        table_rows = self.get_matching_xpath_count('%s//tr' %\
                                                    (self.table_id,))
        for i in xrange(2, int(table_rows)+1):
            policy_name = self.get_text('%s//tr[%s]//td[%s]' % \
                        (self.table_id, i, self.name_column)).split(' \n')[0]
            if policy_name == name:
                return i
        return None

    def _click_view_content(self, name):
        row = self._get_table_row_index(name)
        if row is None:
            raise guiexceptions.GuiControlNotFoundError(name,
                                            'Custom URL Categories')
        cell_id = 'xpath=%s//tr[%s]//td[%s]/a' %\
                    (self.table_id, row, self.view_content_column)

        self.click_element(cell_id)

    def _click_edit_link(self, name):

        row = self._get_table_row_index(name)
        if row is None:
            raise guiexceptions.GuiControlNotFoundError(name,
                                            'Custom URL Categories')
        cell_id = 'xpath=%s//tr[%s]//td[%s]/a' %\
                    (self.table_id, row, self.name_column)

        self.click_element(cell_id)

    def _click_delete_link(self, name):

        start_time = time.time()
        while time.time() - start_time < 60: # max possible timeout for worst scenario
            policy_row = self._get_table_row_index(name)
            if not policy_row is None:
                break
        else:
            raise guiexception.GuiControlNotFoundError('Custom URL category instance: \
                   "%s" missing' % (name,))
        row = self._get_table_row_index(name)
        if row is None:
            raise guiexceptions.GuiControlNotFoundError(
                    'Custom URL category "%s" missing' % (name,),
                    'Custom URL categories')
        cell_id = 'xpath=%s//tr[%s]//td[%s]//img' % \
                (self.table_id,row, self.delete_column)
        self.click_element(cell_id, "don't wait")
        self.click_button("xpath=//button[text()='Delete']")

    def _fill_name(self, name):

        self.input_text("//input[@id='cat_name']", name)

    def _fill_order(self, order):

        self.input_text("//input[@id='cat_order']", order)

    def _fill_sites(self, sites):

        self.input_text("//textarea[@name='category_urls']",
                               ', '.join(self._convert_to_tuple(sites)))
    def _fill_exception_sites(self, sites):

        self.input_text("//textarea[@name='category_exception_urls']",
                               ', '.join(self._convert_to_tuple(sites)))

    def _fill_regexes(self, regexes):

        self.input_text("//textarea[@name='category_urls_regex']",
                               '\n'.join(self._convert_to_tuple(regexes)))

    def _open_page(self):
        """Open 'Custom URL Categories' page """
        self._navigate_to('Web Security Manager', 'Custom and External URL Categories')
