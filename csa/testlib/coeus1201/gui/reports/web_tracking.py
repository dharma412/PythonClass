# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/reports/web_tracking.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.gui.reports_base import ReportsBase
import time

import sal.time

NEXT_BUTTON = "//div[@class='clickable' and contains(text(), 'Next')]"
RESULT_TABLE = "//tbody[@class='yui-dt-data']"
TABLE_CELL_DATA = lambda row, column: "%s/tr[%s]/td[%s]" %(RESULT_TABLE, row, column)
DISPLAY_DETAILS_BUTTON = "xpath=//a[@id='display_details']"

class WebTracking(ReportsBase):
    """Keywords for Reporting -> Web Tracking
    """

    def get_keyword_names(self):
        return [
                "report_web_tracking_proxy_services_search",
                "report_web_tracking_l4tm_search",
                "report_web_tracking_socksproxy_search",
               ]

    def _open_page(self,
        tstTab):
        """
        Navigate to the Web Tracking page and specified Tab:
        Parameters:
        - 'tstTab': the tab on the Web Tracking page to be opened.
           for example self._open_page('SOCKS Proxy')
        """
        TAB = "//em[text()='{tab}']"
        self._navigate_to('Reporting', 'Web Tracking')
        self.click_element(TAB.format(tab=tstTab), "don't wait")


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

            for row in xrange(1, rows+1):
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
                        value = str(self.get_text(locator(row)))
                        value = value.replace("\n", "")
                        value = value.replace("\r", "")

                    result_dict[attribute] = value
                result.append(str(TrackingSearchResult(**result_dict)))

            if not self._is_element_present(NEXT_BUTTON):
                done = True
            else:
                self.click_button(NEXT_BUTTON, "don't wait")

        return result

    def report_web_tracking_proxy_services_search(self,
        time_range=None,
        user=None,
        website=None,
        transaction_type=None,
        checks=None,
        ):
        """
        Search in Report Web Tracking under TAB 'Proxy Services'

        Parameters:
        - `time_range`: if specified, change time range;
          examples: day, week, month
          See more details about setting time range in reports_base        - ``:
        - `user`: User/Client IPv4 or IPv6:
         (e.g. jdoe, DOMAIN\jdoe, 10.1.1.0, or 2001:420:80:1::5)
        - `website`: (e.g. google.com)
        - `transaction_type`: All Transactions, Completed, Blocked, ...
        - `checks`: one or several checks in the resulting table,
         separated by '#'

        Examples:
        Report Web Tracking Proxy Services Search
        ...    time_range=week
        ...    user=10.4.6.132
        ...    website=google.com
        ...    checks=google.com#10.4.6.132

        Exceptions:
        - RuntimeError: "{check}" was not detected
        """

        USER_FIELD = "//input [@id='user']"
        WEBSITE_FIELD = "//input [@id='website']"
        TRANSACTION_TYPE_LIST = "//select [@id='transaction_type']"
        SEARCH_BUTTON = "//input [@id='search_button']"

        CONTAINER = 'dl[@class="header"]'
        TABLE = "//" + CONTAINER + "//span[contains(text(), 'Results')]"\
            + "/ancestor::" + CONTAINER
        VERIFICATION = lambda check: TABLE + \
        "//* [contains(text(), '{check}')]".format(check=check)

        self._open_page('Proxy Services')

        if time_range:
            self._select_time_range(time_range)
        self._input_text_if_not_none(USER_FIELD, user)
        self._input_text_if_not_none(WEBSITE_FIELD, website)
        if transaction_type:
            self.select_from_list(TRANSACTION_TYPE_LIST, transaction_type)
        self.click_button(SEARCH_BUTTON, "don't wait")
        try:
            if checks:
                for check in checks.split('#'):
                    self._wait_until_element_is_present(VERIFICATION(check))
        except:
            raise RuntimeError(
                '"{check}" was not detected.\n'.format \
                   (check=check) + VERIFICATION(check))
        return self._get_results()

    def report_web_tracking_l4tm_search(self,
        time_range=None,
        source=None,
        destination=None,
        port=None,
        connection_type=None,
        checks=None,
        ):
        """
        Search in Report Web Tracking under TAB L4 Traffic Monitor

        Parameters:
        - `time_range`: if specified, change time range;
          examples: day, week, month
          See more details about setting time range in reports_base        - ``:
        - `source`: Source/Client IPv4 or IPv6:
         (e.g. 12.23.34.45 or 2001:420:80:1::5)
        - `destination`: Website/Destination IPv4 or IPv6:
         (e.g. google.com, 90.87.76.65 or 2001:db8::1)
        - `port`: Port:
        - `connection_type`: Detected (All), Blocked, or Monitored
        - `checks`: one or several checks in the resulting table,
         separated by '#'

        Examples:
        Report Web Tracking L4tm Search
        ...    time_range=week
        ...    source=10.4.6.132
        ...    destination=http://etcom.co.kr
        ...    checks=etcom.co.kr#10.4.6.132

        Exceptions:
        - RuntimeError: "{check}" was not detected
        """

        SOURCE_FIELD = "//input [@id='client_ip']"
        DESTINATION_FIELD = "//input [@id='destination']"
        PORT_FIELD = "//input [@id='port']"
        CONNECTION_TYPE_LIST = "//select [@id='connection_type']"

        CONTAINER = 'dl[@class="header"]'
        L4TM_SEARCH_BUTTON = "//input[@id='l4_search_button']"
        TABLE = "//" + CONTAINER + "//span[contains(text(), 'Results')]"\
            + "/ancestor::" + CONTAINER
        VERIFICATION = lambda check: TABLE + \
        "//* [contains(text(), '{check}')]".format(check=check)

        self._open_page('L4 Traffic Monitor')

        if time_range:
            self._select_time_range(time_range)
        self._input_text_if_not_none(SOURCE_FIELD, source)
        self._input_text_if_not_none(DESTINATION_FIELD, destination)
        self._input_text_if_not_none(PORT_FIELD, port)
        if connection_type:
            self.select_from_list(CONNECTION_TYPE_LIST, connection_type)
        self.click_button(L4TM_SEARCH_BUTTON, "don't wait")
        try:
            if checks:
                for check in checks.split('#'):
                    self._wait_until_element_is_present(VERIFICATION(check))
        except:
            raise RuntimeError(
                '"{check}" was not detected.\n'.format \
                   (check=check) + VERIFICATION(check))

    def report_web_tracking_socksproxy_search(self,
        time_range=None,
        userclient=None,
        destination=None,
        port=None,
        protocol=None,
        transaction_disposition=None,
        checks=None,
        ):
        """
        Search in Report Web Tracking under TAB SOCKS Proxy

        Parameters:
        - `time_range`: if specified, change time range;
          examples: day, week, month
          See more details about setting time range in reports_base        - ``:
        - `userclient`: User/Client IPv4 or IPv6:
         (e.g. jdoe or DOMAIN\jdoe)
        - `destination`: Destination Domain or IPv4 or IPv6:
         (e.g. example.com, 10.0.0.1 or 2001:420:80:1::5)
        - `port`: Destination Port:
        - `protocol`: Protocol: TCP, or UDP
        - `transaction_disposition`: Transaction Disposition: Blocked or Completed
        - `checks`: one or several checks in the resulting table,
         separated by '#'

        Examples:
        Report Web Tracking Socksproxy Search
        ...    time_range=week
        ...    userclient=jdoe
        ...    destination=http://etcom.co.kr
        ...    protocol=TCP
        ...    transaction_disposition=Blocked
        ...    checks=etcom.co.kr#10.4.6.132

        Exceptions:
        - RuntimeError: "{check}" was not detected
        """

        SOURCE_FIELD = "//input [@id='socks_user']"
        DESTINATION_FIELD = "//input [@id='socks_host']"
        PORT_FIELD = "//input [@id='socks_port']"
        PROTOCOL_LIST = "//select [@id='socks_protocol']"
        TRANSACTION_LIST = "//select [@id='socks_decision_result']"
        SEARCH_BUTTON = "//input [@id='socks_search_button']"
        CONTAINER = "dl[@class='header']"
        TABLE = "//" + CONTAINER + "//span[contains(text(), 'Results')]"\
            + "/ancestor::" + CONTAINER
        VERIFICATION = lambda check: TABLE + \
        "//* [contains(text(), '{check}')]".format(check=check)

        self._open_page('SOCKS Proxy')
        if time_range:
            self._select_time_range(time_range)
        self._input_text_if_not_none(SOURCE_FIELD, userclient)
        self._input_text_if_not_none(DESTINATION_FIELD, destination)
        self._input_text_if_not_none(PORT_FIELD, port)
        if protocol:
            self.select_from_list(PROTOCOL_LIST, protocol)
        if transaction_disposition:
            self.select_from_list(TRANSACTION_LIST, transaction_disposition)
        self.click_button(SEARCH_BUTTON, "don't wait")
        try:
            if checks:
                for check in checks.split('#'):
                    self._wait_until_element_is_present(VERIFICATION(check))
        except:
            raise RuntimeError(
                '"{check}" was not detected.\n'.format \
                   (check=check) + VERIFICATION(check))

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
