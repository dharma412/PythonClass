#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/reporting/web_tracking.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

import time
import sal.time

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

WEB_PROXY_TAB = '//a[@href="#proxy_services_tab"]'
L4TM_TAB = '//a[@href="#traffic_monitor_tab"]'
SOCKS_TAB = '//a[@href="#socks_tab"]'
CLEAR_BUTTON = 'id=cancel_button'
ADVANCED_SETTINGS_BUTTON = 'xpath=//div[@class="arrow_closed"]'
SEARCH_BUTTON = 'id=search_button'
DISPLAY_DETAILS_BUTTON = 'xpath=//a[@id="display_details"]'
NEXT_BUTTON = '//div[@class="clickable" and contains(text(), "Next")]'
TIME_RANGE_LIST = 'id=date_range'
CLIENT_USER_IP_TEXTBOX = 'id=user'
L4TM_CLIENT_IP_TEXTBOX = 'id=client_ip'
WEBSITE_TEXTBOX = 'id=website'
L4TM_WEBSITE_TEXTBOX = 'id=destination'
PORT_TEXTBOX = 'id=port'
TRANSACTION_TYPE_LIST = 'id=transaction_type'
L4TM_TRANSACTION_TYPE_LIST = 'id=connection_type'
URL_CAT_FILTER_RADIO = lambda value: 'id=url_category_filter_%s' % (value,)
URL_CATEGORY_NAME_TEXTBOX = 'id=url_category'
APP_FILTER_RADIO = lambda value: 'id=application_application_type_filter_%s' % \
                                 (value,)
APP_NAME_TEXTBOX = 'id=application'
APP_TYPE_TEXTBOX = 'id=application_type'
POLICY_FILTER_RADIO = lambda value: 'id=policy_filter_%s' % (value,)
POLICY_NAME_TEXTBOX = 'id=policy'
MALWARE_CAT_FILTER_RADIO = lambda value: 'id=malware_category_filter_%s' % \
                                         (value,)
MALWARE_THREAT_FILTER_RADIO = lambda value: 'id=malware_filter_%s' % (value,)
MALWARE_THREAT_TEXTBOX = 'id=malware'
AMP_FILE_NAME_RADIO = lambda value: 'id=file_name_filter_%s' % (value,)
AMP_FILE_NAME_TEXTBOX = 'id=file_name'
AMP_SHA_256_RADIO = lambda value: 'id=file_sha256_filter_%s' % (value,)
AMP_SHA_256_TEXTBOX = 'id=file_sha256'
MALWARE_CAT_LIST = 'id=malware_category'
WBRS_SCORE_FILTER_RADIO = lambda value: {
    0: 'id=wbrs_filter_disabled',
    1: 'id=wbrs_filter_enabled',
    2: 'id=no_wbrs_score'}[value]
WBRS_LOW_SELECT = 'id=wbrs_from'
WBRS_HIGH_SELECT = 'id=wbrs_to'
WBRS_THREAT_FILTER_RADIO = lambda value: 'id=web_reputaion_filter_%s' % (value,)
WBRS_THREAT_NAME_TEXTBOX = 'id=web_reputaion'
MUS_FILTER_RADIO = lambda value: 'id=mus_access_type_filter_%s' % (value,)
MUS_LOCATION_LIST = 'id=mus_access_type'
APPL_FILTER_RADIO = lambda value: 'id=wsa_serial_filter_%s' % (value,)
L4TM_APPL_FILTER_RADIO = lambda value: 'id=l4tm_wsa_serial_filter_%s' % (value,)
APPL_NAME_LIST = 'id=wsa_serial'
L4TM_APPL_NAME_LIST = 'id=l4tm_wsa_serial'
USER_REQ_FILTER = lambda value: {
    0: 'user_request_enabled_id',
    1: 'user_request_disable_id'}[value]
LIST_LABEL = lambda label: 'label=%s' % (label,)
RESULT_TABLE = "//tbody[@class='yui-dt-data']"
TABLE_CELL_DATA = lambda row, column: "%s/tr[%s]/td[%s]" % \
                                      (RESULT_TABLE, row, column)
SOCKS_TRANSACTION_TYPE_SELECT = 'id=socks_decision_result'
SOCKS_PROTOCOL_SELECT = 'id=socks_protocol'
SOCKS_CLIENT_IP_TEXTBOX = 'id=socks_user'
SOCKS_WEBSITE_TEXTBOX = 'id=socks_host'
SOCKS_PORT_TEXTBOX = 'id=socks_port'


class WebTracking(GuiCommon):
    """Web Tracking page interaction class.

    This class designed to interact with GUI elements of Web -> Reporting
     -> Web Tracking page. Use keywords, listed below, to manipulate
    with Web Tracking page.
    """

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['web_tracking_search',
                'web_tracking_l4tm_search',
                'web_tracking_socks_search'
                ]

    def _open_page(self):
        self._navigate_to('Web', 'Reporting', 'Web Tracking')

    def _select_item_from_list(self, select_list, item, list_name, strict=False):
        options = self.get_list_items(select_list)

        for option in options:
            if strict and item == option:
                self.select_from_list(select_list, LIST_LABEL(option))
                break
            elif not strict and item in option:
                self.select_from_list(select_list, LIST_LABEL(option))
                break
        else:
            raise ValueError('No %s option was found in %s select list' % \
                             (item, list_name))

    def _configure_filter_with_select_list(self, filter_value, filter_switch,
                                           list_loc, filter_name):
        if filter_value is None:
            return

        if filter_value:
            self._click_radio_button(filter_switch(1))
            self._select_item_from_list(list_loc, filter_value, filter_name)
        else:
            self._click_radio_button(filter_switch(0))

    def _configure_filter_with_textbox(self, filter_value, filter_switch,
                                       textbox_loc):
        if filter_value is None:
            return

        if filter_value:
            self._click_radio_button(filter_switch(1))
            self.input_text(textbox_loc, filter_value)
        else:
            self._click_radio_button(filter_switch(0))

    def _select_time_range(self, time_range):
        if time_range is not None:
            self._select_item_from_list(TIME_RANGE_LIST, time_range,
                                        'time range')

    def _fill_ip_addr_textbox(self, ip_addr):
        if ip_addr is not None:
            self.input_text(CLIENT_USER_IP_TEXTBOX, ip_addr)

    def _fill_website_textbox(self, website):
        if website is not None:
            self.input_text(WEBSITE_TEXTBOX, website)

    def _fill_l4tm_ip_addr_textbox(self, ip_addr):
        if ip_addr is not None:
            self.input_text(L4TM_CLIENT_IP_TEXTBOX, ip_addr)

    def _fill_l4tm_website_textbox(self, website):
        if website is not None:
            self.input_text(L4TM_WEBSITE_TEXTBOX, website)

    def _fill_port_textbox(self, port):
        if port is not None:
            self.input_text(PORT_TEXTBOX, port)

    def _select_transaction_type_filter(self, transaction_type):
        if transaction_type is not None:
            self._select_item_from_list(TRANSACTION_TYPE_LIST,
                                        transaction_type, 'transaction type')

    def _select_l4tm_transaction_type_filter(self, transaction_type):
        if transaction_type is not None:
            self._select_item_from_list(L4TM_TRANSACTION_TYPE_LIST,
                                        transaction_type, 'transaction type')

    def _select_url_filter(self, url_filter):
        self._configure_filter_with_textbox(url_filter, URL_CAT_FILTER_RADIO,
                                            URL_CATEGORY_NAME_TEXTBOX)

    def _select_application_filter(self, application_filter):
        if application_filter is None:
            return

        if application_filter == False:
            self._click_radio_button(APP_FILTER_RADIO(0))
            return

        application_filter = self._convert_to_tuple(application_filter)
        if not (isinstance(application_filter, tuple) and
                len(application_filter) == 2):
            raise ValueError('Application filter must be a tuple of length 2')

        filter_type, value = application_filter
        if filter_type == 'app_name':
            self._click_radio_button(APP_FILTER_RADIO(1))
            self.input_text(APP_NAME_TEXTBOX, value)
        elif filter_type == 'app_type':
            self._click_radio_button(APP_FILTER_RADIO(2))
            self.input_text(APP_TYPE_TEXTBOX, value)
        else:
            raise ValueError('Unknown %s application filter type' % \
                             (filter_type,))

    def _select_policy_filter(self, policy_filter):
        self._configure_filter_with_textbox(policy_filter, POLICY_FILTER_RADIO,
                                            POLICY_NAME_TEXTBOX)

    def _select_malware_category_filter(self, malware_category_filter):
        self._configure_filter_with_select_list(malware_category_filter,
                                                MALWARE_CAT_FILTER_RADIO,
                                                MALWARE_CAT_LIST,
                                                'Malware Category')

    def _select_malware_threat_filter(self, malware_threat_filter):
        self._configure_filter_with_textbox(malware_threat_filter,
                                            MALWARE_THREAT_FILTER_RADIO,
                                            MALWARE_THREAT_TEXTBOX)

    def _select_amp_filename(self, amp_filename):
        self._configure_filter_with_textbox(amp_filename,
                                            AMP_FILE_NAME_RADIO,
                                            AMP_FILE_NAME_TEXTBOX)

    def _select_amp_sha256(self, amp_sha256):
        self._configure_filter_with_textbox(amp_sha256,
                                            AMP_SHA_256_RADIO,
                                            AMP_SHA_256_TEXTBOX)

    def _select_wbrs_score_filter(self, wbrs_score_filter):
        if wbrs_score_filter is None:
            return

        if wbrs_score_filter == False:
            self._click_radio_button(WBRS_SCORE_FILTER_RADIO(0))
            return

        if wbrs_score_filter == True:
            self._click_radio_button(WBRS_SCORE_FILTER_RADIO(2))
            return

        wbrs_score_filter = self._convert_to_tuple(wbrs_score_filter)
        if not isinstance(wbrs_score_filter, tuple):
            raise ValueError('WBRS score filter must be a tuple')

        if len(wbrs_score_filter) == 2:
            self._click_radio_button(WBRS_SCORE_FILTER_RADIO(1))
            for score, locator in zip(wbrs_score_filter,
                                      (WBRS_LOW_SELECT, WBRS_HIGH_SELECT)):
                self._select_item_from_list(locator, str(score), 'WBRS Score',
                                            True)
        else:
            raise ValueError('Wrong input was provided for WBRS score filter')

    def _select_wbrs_threat_filter(self, wbrs_threat_filter):
        self._configure_filter_with_textbox(wbrs_threat_filter,
                                            WBRS_THREAT_FILTER_RADIO,
                                            WBRS_THREAT_NAME_TEXTBOX)

    def _select_mus_filter(self, mus_filter):
        self._configure_filter_with_select_list(mus_filter, MUS_FILTER_RADIO,
                                                MUS_LOCATION_LIST,
                                                'MUS user location')

    def _select_appl_filter(self, appl_filter):
        self._configure_filter_with_select_list(appl_filter, APPL_FILTER_RADIO,
                                                APPL_NAME_LIST, 'Web Appliance')

    def _select_l4tm_appl_filter(self, appl_filter):
        self._configure_filter_with_select_list(appl_filter,
                                                L4TM_APPL_FILTER_RADIO,
                                                L4TM_APPL_NAME_LIST,
                                                'Web Appliance')

    def _fill_socks_ip_addr_textbox(self, ip_addr):
        if ip_addr is not None:
            self.input_text(SOCKS_CLIENT_IP_TEXTBOX, ip_addr)

    def _fill_socks_website_textbox(self, website):
        if website is not None:
            self.input_text(SOCKS_WEBSITE_TEXTBOX, website)

    def _fill_socks_port_textbox(self, port):
        if port is not None:
            self.input_text(SOCKS_PORT_TEXTBOX, port)

    def _select_socks_transaction_type_filter(self, transaction_type):
        if transaction_type is not None:
            self._select_item_from_list(SOCKS_TRANSACTION_TYPE_SELECT,
                                        transaction_type, 'transaction type')

    def _select_socks_protocol(self, protocol):
        if protocol is not None:
            self._select_item_from_list(SOCKS_PROTOCOL_SELECT,
                                        protocol, 'protocol')

    def _user_request_filter(self, user_request_filter):
        if user_request_filter is None:
            return

        if user_request_filter == True:
            self._click_radio_button(USER_REQ_FILTER(0))
        elif user_request_filter == False:
            self._click_radio_button(USER_REQ_FILTER(1))
        else:
            raise ValueError('Unknown %s user request filter type' % \
                             (user_request_filter,))

    def _get_results(self):
        locators_dict = {
            'time_stamp': lambda row: TABLE_CELL_DATA(row, 1),
            'website': lambda row: TABLE_CELL_DATA(row, 2) + \
                                   "//tr[@name='full_url']",
            'count': lambda row: TABLE_CELL_DATA(row, 2) + \
                                 "//tr[@name='full_url']//tbody//td[2]",
            'content_type': lambda row: TABLE_CELL_DATA(row, 2) + \
                                        "//tr[@name='transaction_content_type']//td[1]",
            'url_category': lambda row: TABLE_CELL_DATA(row, 2) + \
                                        "//tr[@name='transaction_url_category']//td[1]",
            'destination_ip': lambda row: TABLE_CELL_DATA(row, 2) + \
                                          "//tr[@name='transaction_destination_ip']//td[1]",
            'host': lambda row: TABLE_CELL_DATA(row, 2) + \
                                "//tr[@name='transaction_destination_ip']//td[2]",
            'details': lambda row: TABLE_CELL_DATA(row, 2) + \
                                   "//tr[@name='transaction_details']//div",
            'disposition': lambda row: TABLE_CELL_DATA(row, 3),
            'bandwidth': lambda row: TABLE_CELL_DATA(row, 4),
            'ip': lambda row: TABLE_CELL_DATA(row, 5)
        }

        result = []

        # waiting for table to be generated
        # waiting for table cell(1, 2) to be generated
        timer = sal.time.CountDownTimer(timeout=10).start()
        while timer.is_active():
            if self._is_element_present(TABLE_CELL_DATA(1, 2)):
                break
            else:
                time.sleep(1)
        else:
            return result
        # waiting for whole table to be generated
        time.sleep(10)

        self.click_element(DISPLAY_DETAILS_BUTTON, "don't wait")

        done = False
        while not done:

            # Data may be still loading in some rows.
            # waiting for data to be loading, until 'Loading' message is present
            timer = sal.time.CountDownTimer(10).start()
            while timer.is_active():
                if not self._is_text_present('Loading'):
                    break
                time.sleep(2)

            # waiting for data to be loading, in some cases data need more time
            # to load, e.g. you have 10 pages with 100 items
            time.sleep(20)
            rows = int(self.get_matching_xpath_count(TABLE_CELL_DATA('*', 2)))

            for row in xrange(1, rows + 1):
                result_dict = {}
                for attribute, locator in locators_dict.iteritems():
                    if attribute == 'count':
                        if self._is_element_present(locator(row)):
                            value = self.get_text(locator(row))
                            value = int(value.strip('()'))
                        else:
                            value = 1
                    elif attribute == 'website':
                        value = self.get_text(locator(row)).split('\n')[0]
                    else:
                        value = self.get_text(locator(row))

                    result_dict[attribute] = value

                result.append(str(TrackingSearchResult(**result_dict)))

            if not self._is_element_present(NEXT_BUTTON):
                done = True
            else:
                self.click_button(NEXT_BUTTON, "don't wait")

        return result

    def _get_l4tm_results(self):
        data_row = "//tr[contains(@id, 'yui-rec')]"
        L4TM_TABLE_CELL_DATA = lambda row, column: \
            "//tr[%s][contains(@id, 'yui-rec')]/td[%s]" % (row, column)
        locators_dict = {
            'time_stamp': lambda row: L4TM_TABLE_CELL_DATA(row, 1),
            'destination_ip': lambda row: L4TM_TABLE_CELL_DATA(row, 2) + \
                                          "//tr[@name='truncated_url']",
            'domain': lambda row: L4TM_TABLE_CELL_DATA(row, 3),
            'disposition': lambda row: L4TM_TABLE_CELL_DATA(row, 4),
            'port': lambda row: L4TM_TABLE_CELL_DATA(row, 5),
            'client_ip': lambda row: L4TM_TABLE_CELL_DATA(row, 6),
        }

        result = []

        # waiting for table to be generated
        # waiting for table cell(1, 2) to be generated
        timer = sal.time.CountDownTimer(timeout=10).start()
        while timer.is_active():
            if self._is_element_present(L4TM_TABLE_CELL_DATA(1, 2)):
                break
            else:
                time.sleep(1)
        else:
            return result

        done = False
        while not done:

            # Data may be still loading in some rows.
            # waiting for data to be loading, until 'Loading' message is present
            timer = sal.time.CountDownTimer(10).start()
            while timer.is_active():
                if not self._is_text_present('Loading'):
                    break
                time.sleep(2)

            # waiting for data to be loading, in some cases data need more time
            # to load, e.g. you have 10 pages with 100 items
            time.sleep(20)
            rows = int(self.get_matching_xpath_count(L4TM_TABLE_CELL_DATA('*', 2)))

            for row in xrange(1, rows + 1):
                result_dict = {}

                for attribute, locator in locators_dict.iteritems():
                    value = self.get_text(locator(row))
                    result_dict[attribute] = value

                result.append(str(L4TMTrackingSearchResult(**result_dict)))

            if not self._is_element_present(NEXT_BUTTON):
                done = True
            else:
                self.click_button(NEXT_BUTTON, "don't wait")

        return result

    def _get_socks_results(self):
        SOCKS_TABLE_CELL_DATA = lambda row, column: \
            "//tr[%s][contains(@id, 'yui-rec')]/td[%s]" % (row, column)
        locators_dict = {
            'time_stamp': lambda row: SOCKS_TABLE_CELL_DATA(row, 1),
            'destination': lambda row: SOCKS_TABLE_CELL_DATA(row, 2),
            'details': lambda row: SOCKS_TABLE_CELL_DATA(row, 2) + \
                                   "//tr[@name='socks_details']/td[1]/text()[2]",
            'disposition': lambda row: SOCKS_TABLE_CELL_DATA(row, 3),
            'bandwidth': lambda row: SOCKS_TABLE_CELL_DATA(row, 4),
            'protocol': lambda row: SOCKS_TABLE_CELL_DATA(row, 5),
            'client_ip': lambda row: SOCKS_TABLE_CELL_DATA(row, 6),
        }

        result = []

        # waiting for table to be generated
        # waiting for table cell(1, 2) to be generated
        timer = sal.time.CountDownTimer(timeout=10).start()
        while timer.is_active():
            if self._is_element_present(SOCKS_TABLE_CELL_DATA(1, 2)):
                break
            else:
                time.sleep(1)
        else:
            return result

        done = False
        while not done:

            # Data may be still loading in some rows.
            # waiting for data to be loading, until 'Loading' message is present
            timer = sal.time.CountDownTimer(10).start()
            while timer.is_active():
                if not self._is_text_present('Loading'):
                    break
                time.sleep(2)

            # waiting for data to be loading, in some cases data need more time
            # to load, e.g. you have 10 pages with 100 items
            time.sleep(20)
            rows = int(self.get_matching_xpath_count(SOCKS_TABLE_CELL_DATA('*', 2)))

            for row in xrange(1, rows + 1):
                result_dict = {}

                for attribute, locator in locators_dict.iteritems():
                    value = self.get_text(locator(row))
                    result_dict[attribute] = value

                result.append(str(SOCKSTrackingSearchResult(**result_dict)))

            if not self._is_element_present(NEXT_BUTTON):
                done = True
            else:
                self.click_button(NEXT_BUTTON, "don't wait")

        return result

    def web_tracking_search(self,
                            time_range=None,
                            ip_addr=None,
                            website=None,
                            transaction_type=None,
                            url_filter=None,
                            application_filter=None,
                            policy_filter=None,
                            amp_filename=None,
                            amp_sha256=None,
                            malware_cat_filter=None,
                            malware_threat_filter=None,
                            wbrs_score_filter=None,
                            wbrs_threat_filter=None,
                            mus_filter=None,
                            appl_filter=None,
                            user_req_filter=None,
                            clear_previous_search=True
                            ):
        """Perform Web tracking search.

        Parameters:
            - `time_range`: time range to track. Can be one of _Day_, _Week_,
            _30 days_, _90 days_, _Yesterday (00:00 to 23:59)_,
            _Previous Calendar Month_.
            - `ip_addr`: user or client IP address to track information for.
            e.g. 12.23.34.45
            - `website`: website to track information for.
            e.g. google.com or 90.87.76.65
            - `transaction_type`: type of transaction to track. Can be one of
            _Completed_, _Blocked_, _Monitored_, _Warned_ and _All_
            - `url_filter`: filtering by URL category. String of URL category
            name to enable filtering, _False_ to disable filtering.
            - `application_filter`: filtering by application. Accepts a comma
            separated string or list of filter_type and value.
            e.g filter_type, value. Filter type can be one of _app_name_ or
            _app_type_. Value is a string containing either name or type of the
            application. _False_ to disable filter.
            - `policy_filter`: filtering by policy name. String of policy name
            to enable filtering, _False_ to disable.
            - `malware_cat_filter`: filtering by malware category. String of
            malware category name to enable filtering, _False_ to disable.
            - `malware_threat_filter`: filtering by malware threat. String of
            threat name to enable filtering, _False_ to disable. e.g. Adware
            - `wbrs_score_filter`: filtering by WBRS score. Accepts a comma
            separated string or list of WBRS scores, each score value can be in
            range of (-10, 10). _True_ enable filter and not use any scores.
            _False_ to disable filter.
            - `wbrs_threat_filter`: filtering by reputation threat. String of
            reputation threat name to enable filtering, _False_ to disable filter.
            - `mus_filter`: filtering by MUS. String of user location to enable
            filtering. Can be _Remote access_ or _Local access_.
             _False_ to disable filter.
            - `appl_filter`: filter by web appliance. String of web appliance
            name to enable filtering. _False_ to disable filter.
            - `user_req_filter`: filter by user request. _True_ to enable filter.
            _False_ to disable filter.
            - `clear_previous_search`: clear the result of previous search
            before doing this one. Default is _True_.

        Return:
            A list of TrackingSearchResult objects.
            Each object has the following attributes:
            - `time_stamp`: a string containing the time the URL was accessed.
            - `website`: url of the transaction website.
            - `count`: the number of the requests.
            - `disposition`: the reason why the transaction was blocked.
            - `bandwidth`: bandwidth used for transaction.
            - `ip`: user/client ip.
            - `content_type`: content type of the request.
            - `url_category`: url category of the transaction.
            - `destination_ip`: destination IP address of the transaction.
            - `host`: host that processed the transaction.
            - `details`: details of the transaction.

        Example:
        | ${results} = | Web Tracking Search |
        | ... | time_range=90 days |
        | ... | ip_addr=1.2.3.4 |
        | ... | website=google.com |
        | ... | transaction_type=Blocked |
        | ... | url_filter=test_url |
        | ... | application_filter=app_name, name1 |
        | ... | policy_filter=test_policy |
        | ... | malware_cat_filter=Worm |
        | ... | malware_threat_filter=test_threat |
        | ... | wbrs_score_filter=${True} |
        | ... | wbrs_threat_filter=wbrs_test_threat |
        | ... | mus_filter=Local access |
        | ... | appl_filter=wsa102 |
        | ... | user_req_filter=${True} |
        | ... | clear_previous_search=${False} |

        | ${results} = | Web Tracking Search |
        | ... | time_range=90 days |
        | ... | ip_addr=1.2.3.4 |
        | ... | website=google.com |
        | ... | transaction_type=Blocked |
        | ... | url_filter=${False} |
        | ... | application_filter=${False} |
        | ... | policy_filter=${False} |
        | ... | malware_cat_filter=${False} |
        | ... | malware_threat_filter=${False} |
        | ... | wbrs_score_filter=-4, 9 |
        | ... | wbrs_threat_filter=${False} |
        | ... | mus_filter=${False} |
        | ... | appl_filter=${False} |
        | ... | user_req_filter=${False} |
        """
        self._open_page()

        if clear_previous_search:
            self.click_button(CLEAR_BUTTON)

        self.click_element(ADVANCED_SETTINGS_BUTTON, "don't wait")
        self._select_time_range(time_range)
        self._fill_ip_addr_textbox(ip_addr)
        self._fill_website_textbox(website)
        self._select_transaction_type_filter(transaction_type)
        self._select_url_filter(url_filter)
        self._select_application_filter(application_filter)
        self._select_policy_filter(policy_filter)
        self._select_amp_filename(amp_filename)
        self._select_amp_sha256(amp_sha256)
        self._select_malware_category_filter(malware_cat_filter)
        self._select_malware_threat_filter(malware_threat_filter)
        self._select_wbrs_score_filter(wbrs_score_filter)
        self._select_wbrs_threat_filter(wbrs_threat_filter)
        self._select_mus_filter(mus_filter)
        self._select_appl_filter(appl_filter)
        self._user_request_filter(user_req_filter)
        self.click_button(SEARCH_BUTTON)

        return self._get_results()

    def web_tracking_l4tm_search(self,
                                 time_range=None,
                                 ip_addr=None,
                                 website=None,
                                 port=None,
                                 transaction_type=None,
                                 appl_filter=None,
                                 clear_previous_search=True
                                 ):
        """Perform Web tracking search.

        Parameters:
            - `time_range`: time range to track. Can be one of _Day_, _Week_,
            _30 days_, _90 days_, _Yesterday (00:00 to 23:59)_,
            _Previous Calendar Month_.
            - `client_ip`: user or client IP address to track information for.
            e.g. 12.23.34.45
            - `website`: website or ip address to track information for.
            e.g. google.com or 90.87.76.65
            - `port`: port to track information for.
            - `transaction_type`: type of transaction to track. Can be one of
            _Block_, _Monitored_ or _All_. None to use default value.
            - `appl_filter`: filter by web appliance. String of web appliance
            name to enable filtering. _False_ to disable filter.
            - `clear_previous_search`: clear the result of previous search
            before doing this one. Default is _True_.

        Return:
            A list of L4TMTrackingSearchResult objects.
            Each object has the following attributes:
            - `time_stamp`: a string containing the time the URL was accessed.
            - `destination_ip`: destination IP address.
            - `domain`: destination domain.
            - `disposition`: transaction verdict.
            - `port`: port of the transaction.
            - `client_ip`: user/client ip.

        Example:
        | ${results} = | Web Tracking L4tm Search |
        | ... | time_range=Week |
        | ... | ip_addr=12.23.34.45 |
        | ... | website=google.com |
        | ... | port=443 |
        | ... | transaction_type=Blocked |
        | ... | appl_filter=wsa102 |

        | ${results} = | Web Tracking L4tm Search |
        | ... | time_range=30 days |
        | ... | ip_addr=12.23.34.45 |
        | ... | website=google.com |
        | ... | port=443 |
        | ... | transaction_type=All |
        | ... | appl_filter=False |
        | ... | clear_previous_search=False |
        """
        self._open_page()
        self.click_button(L4TM_TAB, "don't wait")

        if clear_previous_search:
            self.click_button(CLEAR_BUTTON)

        self.click_button(ADVANCED_SETTINGS_BUTTON, "don't wait")
        self._select_time_range(time_range)
        self._fill_l4tm_ip_addr_textbox(ip_addr)
        self._fill_l4tm_website_textbox(website)
        self._fill_port_textbox(port)
        self._select_l4tm_transaction_type_filter(transaction_type)
        self._select_l4tm_appl_filter(appl_filter)
        self.click_button(SEARCH_BUTTON)

        return self._get_l4tm_results()

    def web_tracking_socks_search(self,
                                  time_range=None,
                                  ip_addr=None,
                                  website=None,
                                  port=None,
                                  protocol=None,
                                  transaction_type=None,
                                  url_filter=None,
                                  policy_filter=None,
                                  mus_filter=None,
                                  clear_previous_search=True
                                  ):
        """Perform Web tracking search.

        Parameters:
            - `time_range`: time range to track. Can be one of _Day_, _Week_,
            _30 days_, _90 days_, _Yesterday (00:00 to 23:59)_,
            _Previous Calendar Month_.
            - `client_ip`: user or client IP address to track information for.
            e.g. 12.23.34.45
            - `website`: website or ip address to track information for.
            e.g. google.com or 90.87.76.65
            - `port`: destination port to track information for.
            - `protocol`: type of protocol to track. Can be one of
            _TCP_, _UDP_ or _All_. None to use default value.
            - `transaction_type`: type of transaction to track. Can be one of
            _Blocked_, _Completed_ or _All_. None to use default value.
            - `url_filter`: filtering by URL category. String of URL category
            name to enable filtering, _False_ to disable filtering.
            - `policy_filter`: filtering by policy name. String of policy name
            to enable filtering, _False_ to disable.
            - `mus_filter`: filtering by MUS. String of user location to enable
            filtering. Can be _Remote access_ or _Local access_.
             _False_ to disable filter.
            - `clear_previous_search`: clear the result of previous search
            before doing this one. Default is _True_.

        Return:
            A list of SOCKSTrackingSearchResult objects.
            Each object has the following attributes:
            - `time_stamp`: a string containing the time the URL was accessed.
            - `destination`: Destination information.
            If host names are resolved by proxy it includes hostname, port and ip.
            E.g. "www.google.com:80 [74.125.239.112]".
            In other case contains only port and ip information.
            E.g. "74.125.239.114:80"
            - `details`: details of the transaction.
            - `disposition`: transaction verdict.
            - `bandwidth`: bandwidth used.
            - `protocol`: protocol of the transaction.
            - `client_ip`: user/client ip.

        Example:
        | ${results} = | Web Tracking SOCKS Search |
        | ... | time_range=Week |
        | ... | website=google.com |
        | ... | port=80 |
        | ... | protocol=TCP |
        | ... | transaction_type=Completed |
        | ... | policy_filter=DefaultGroup |
        | ... | clear_previous_search=True |

        | ${results} = | Web Tracking SOCKS Search |
        | ... | time_range=Day |
        | ... | ip_addr=10.1.2.3 |
        | ... | port=8080 |
        | ... | transaction_type=All |
        | ... | url_filter=Adult |
        | ... | policy_filter=DefaultGroup |
        | ... | mus_filter=Local access |
        | ... | clear_previous_search=False |
        """
        self._open_page()
        self.click_button(SOCKS_TAB, "don't wait")

        if clear_previous_search:
            self.click_button(CLEAR_BUTTON)

        self.click_button(ADVANCED_SETTINGS_BUTTON, "don't wait")
        self._select_time_range(time_range)
        self._fill_socks_ip_addr_textbox(ip_addr)
        self._fill_socks_website_textbox(website)
        self._fill_socks_port_textbox(port)
        self._select_socks_protocol(protocol)
        self._select_socks_transaction_type_filter(transaction_type)
        self._select_url_filter(url_filter)
        self._select_policy_filter(policy_filter)
        self._select_mus_filter(mus_filter)

        self.click_button(SEARCH_BUTTON)

        return self._get_socks_results()


class TrackingSearchResult(object):
    """Container class for holding information about tracking search
    result.

    Attributes:
    - `time_stamp`: a string containing the time the URL was accessed.
    - `website`: url of the transaction website.
    - `count`: the number of the requests.
    - `disposition`: the reason why the transaction was blocked.
    - `bandwidth`: bandwidth used for transaction.
    - `ip`: user/client ip.
    - `content_type`: content type of the request.
    - `url_category`: url category of the transaction.
    - `destination_ip`: destination IP address of the transaction.
    - `host`: host that processed the transaction.
    - `details`: details of the transaction.
    """

    def __init__(self, time_stamp, website, count, disposition, bandwidth,
                 ip, content_type, url_category, destination_ip, host,
                 details):
        self.time_stamp = time_stamp
        self.website = website
        self.count = count
        self.disposition = disposition
        self.bandwidth = bandwidth
        self.ip = ip
        self.content_type = content_type
        self.url_category = url_category
        self.destination_ip = destination_ip
        self.host = host
        self.details = details

    def __str__(self):
        result_str = ('Time Stamp: %s' % (self.time_stamp,),
                      'Website: %s' % (self.website,),
                      'Count: %s' % (self.count,),
                      'Disposition: %s' % (self.disposition,),
                      'Bandwidth: %s' % (self.bandwidth,),
                      'IP: %s' % (self.ip,),
                      'Content Type: %s' % (self.content_type,),
                      'URL Category: %s' % (self.url_category,),
                      'Destination IP: %s' % (self.destination_ip,),
                      'Host: %s' % (self.host,),
                      'Details: %s' % (self.details,),
                      )
        return '; '.join(result_str)


class L4TMTrackingSearchResult(object):
    """Container class for holding information about L4TM tracking search
    result.

    :Attributes:
    - `time_stamp`: a string containing the time the URL was accessed.
    - `destination_ip`: destination IP address.
    - `domain`: destination domain.
    - `disposition`: transaction verdict.
    - `port`: port of the transaction.
    - `client_ip`: user/client ip.
    """

    def __init__(self, time_stamp, destination_ip, domain, disposition,
                 port, client_ip):
        self.time_stamp = time_stamp
        self.destination_ip = destination_ip
        self.domain = domain
        self.disposition = disposition
        self.port = port
        self.client_ip = client_ip

    def __str__(self):
        result_str = ('Time Stamp: %s' % (self.time_stamp,),
                      'Destination IP: %s' % (self.destination_ip,),
                      'Domain: %s' % (self.domain,),
                      'Disposition: %s' % (self.disposition,),
                      'Port: %s' % (self.port,),
                      'Client IP: %s' % (self.client_ip,),
                      )
        return '; '.join(result_str)


class SOCKSTrackingSearchResult(object):
    """Container class for holding information about SOCKS tracking search
    result.

    :Attributes:
    - `time_stamp`: a string containing the time the URL was accessed.
    - `destination`: Destination information.
    If host names are resolved by proxy it includes hostname, port and ip.
    E.g. "www.google.com:80 [74.125.239.112]".
    In other case contains only port and ip information.
    E.g. "74.125.239.114:80"
    - `details`: details of the transaction.
    - `disposition`: transaction verdict.
    - `bandwidth`: bandwidth used.
    - `protocol`: protocol of the transaction.
    - `client_ip`: user/client ip.
    """

    def __init__(self, time_stamp, destination, details, disposition,
                 bandwidth, protocol, client_ip):
        self.time_stamp = time_stamp
        self.destination = destination
        self.details = details
        self.disposition = disposition
        self.bandwidth = bandwidth
        self.protocol = protocol
        self.client_ip = client_ip

    def __str__(self):
        result_str = ('Time Stamp: %s' % (self.time_stamp,),
                      'Destination: %s' % (self.destination,),
                      'Details: %s' % (self.details,),
                      'Disposition: %s' % (self.disposition,),
                      'Bandwidth: %s' % (self.bandwidth,),
                      'Protocol: %s' % (self.protocol,),
                      'Client IP: %s' % (self.client_ip,),
                      )
        return '; '.join(result_str)
