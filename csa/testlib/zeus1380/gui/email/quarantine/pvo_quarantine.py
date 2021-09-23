# $Id: //prod/main/sarf_centos/testlib/zeus1380/gui/email/quarantine/pvo_quarantine.py#4 $
# $DateTime: 2020/08/18 21:31:35 $
# $Author: sumitada $

import time

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon
from common.util.sarftime import CountDownTimer


PVO_TABLE = "//table[@class='cols']"
QUARANTINE_MESSAGES = lambda name, col_idx: \
            "%s//td[normalize-space()='%s']/following-sibling::td[%d]" % \
            (PVO_TABLE, name, col_idx)
POLICY_QUARANTINE = "//input[@value='Add Policy Quarantine...']"
POLICY_NAME = "//input[@name='name']"
TODAY_RANGE_RADIO = "xpath=//input[@id='period_today']"
WEEK_RANGE_RADIO = "xpath=//input[@id='period_last_week']"
DATE_RANGE_RADIO = "xpath=//input[@id='period_range']"
DATE_RANGE_TEXTBOXES = ("xpath=//input[@id='period_start']", "xpath=//input[@id='period_end']")
RETENTION_PERIOD = "//input[@name='period']"
RETENTION_UNIT = "//select[@name='periodUnits']"
DEFAULT_ACTION_DELETE= "//input[@id='defaultAction_delete']"
DEFAULT_ACTION_RELEASE= "//input[@id='defaultAction_release']"
SUBMIT = "//input[@class='submit']"
SEARCH_QUARANTINE="//input[@id='search_quarantine']"
SELECT_ALL_CHECKBOX=  "//input[@id='mid']"
DELETE_BUTTON=  "//input[@id='delete_btn']"
RELEASE_BUTTON=  "//input[@id='release_btn']"
CONFIRM_BUTTON= "//button[contains(text(), 'Confirm')]"
MSG_INFO_ROW = lambda row: "//tbody[@class=\'yui-dt-data\']/tr[%s]" % (row)
POLICY_MESSAGE= lambda row: "//table[@class='cols']/tbody/tr[%s]/td[1]" %(row)
POLICY_MESSAGE_NAME= lambda row: "//table[@class='cols']/tbody/tr[%s]/td[1]/a" %(row)
POLICY_MESSAGE_ROW= lambda row: "//table[@class='cols']/tbody/tr[%s]/td[3]/a" % (row)
SEARCH_BUTTON = 'xpath=//input[@value=\'Search\' and @type=\'submit\']'
ESA_IP = 'xpath=//input[@name="esa_ip"]'

class PVOQuarantine(GuiCommon):
    """PVO Quarantine page interaction class.

    This class designed to interact with GUI elements of Email -> Message
    Quarantine -> PVO Quarantine. Use keywords, listed below,
    to manipulate with PVO Quarantine page.

    Note, that you must call 'Spam Quarantine Search Page Open' keyword
    before use quarantine message handling routines
    """
    def get_keyword_names(self):
        return  ['outbreak_messages_count',
                 'policy_messages_count',
                 'virus_messages_count',
                 'add_policy_quarantine',
                 'pvo_policy_get_list',
                 'pvo_delete_policy_message',
                 'pvo_release_policy_message',
                 'pvo_search_policy_message']

    def _open_page(self):
        self._navigate_to('Email', 'Message Quarantine', 'Policy, Virus and Outbreak Quarantines')

        err_msg = 'This feature is currently disabled.'
        if self._is_text_present(err_msg):
            raise guiexceptions.GuiFeatureDisabledError(err_msg)

    def _click_edit_policy_link(self, name):
        no_of_rows= int(self.get_matching_xpath_count(POLICY_MESSAGE('*')))
        for row in range(2, no_of_rows + 2):
            try:
                if self.get_text(POLICY_MESSAGE_NAME(row)).split()[0] == name:
                    self.click_element(POLICY_MESSAGE_ROW(row))
                    break
            except:
                if self.get_text\
                    (POLICY_MESSAGE(row)).split()[0] == name:
                    self.click_element(POLICY_MESSAGE_ROW(row))
                    break

    def _select_date_range(self, date_range):
        if date_range is None:
            return

        date_range_map = {
            'today': TODAY_RANGE_RADIO,
            'week': WEEK_RANGE_RADIO,
        }

        if isinstance(date_range, basestring):
            if date_range in date_range_map:
                self._click_radio_button(date_range_map[date_range])
        elif isinstance(date_range, tuple):
            self._click_radio_button(DATE_RANGE_RADIO)
            if len(date_range) != 2:
                raise ValueError('Date range should be a tuple of 2.')

            for locator, value in zip(DATE_RANGE_TEXTBOXES, date_range):
                self.input_text(locator, value)

        else:
            raise ValueError('Invalid %s date range' % (date_range,))

    def _search_msgs(self, date_range, esa_ip=None):
        date_range_map = {
            'today': TODAY_RANGE_RADIO,
            'week': WEEK_RANGE_RADIO,
        }

        self._select_date_range(date_range)
        if esa_ip is not None:
            self.input_text(ESA_IP,esa_ip)
        time.sleep(2)
        self.click_button(SEARCH_BUTTON)

    def _delete_action(self):
        self.click_button(DELETE_BUTTON, 'don\'t wait')
        self.click_button(CONFIRM_BUTTON)

    def _release_action(self):
        self.click_button(RELEASE_BUTTON, 'don\'t wait')
        self.click_button(CONFIRM_BUTTON)

    def _do_isq_action(self, action_method):
        timeout = 120
        interval = 1
        for i in xrange(100):
            for i in xrange(0, timeout, interval):
                if not (self._is_text_present('Please do not reload')):
                    break
                time.sleep(interval)
            if self._is_text_present('No records found'):
                break
            self._select_checkbox(SELECT_ALL_CHECKBOX)
            action_method()

    def outbreak_messages_count(self):
        self._open_page()
        return  self.get_text(QUARANTINE_MESSAGES("Outbreak",1))

    def policy_messages_count(self):
        self._open_page()
        return  self.get_text(QUARANTINE_MESSAGES("Centralized Policy",1))

    def virus_messages_count(self):
        self._open_page()
        return  self.get_text(QUARANTINE_MESSAGES("Antivirus",1))

    def add_policy_quarantine(self, name=None, retention_period=None, retention_unit=None, default_action=None):
        self._open_page()
        self.click_button(POLICY_QUARANTINE)
        self.input_text(POLICY_NAME, name)
        self.input_text(RETENTION_PERIOD, retention_period)
        self.select_from_list(RETENTION_UNIT, retention_unit)
        if default_action=='delete':
           self._click_radio_button(DEFAULT_ACTION_DELETE)
        else:
           self._click_radio_button(DEFAULT_ACTION_RELEASE)
        self._click_submit_button()

    def pvo_policy_get_list(self):
        self._open_page()
        return self._get_policies()

    def pvo_delete_policy_message(self, name=None, date_range=None):
        self._open_page()
        self._click_edit_policy_link(name)
        self.click_button(SEARCH_QUARANTINE)
        if isinstance(date_range, basestring) and date_range.find(',') > 0:
            date_range = self._convert_to_tuple(date_range)
        self._search_msgs(date_range=date_range)
        delete_action = self._delete_action
        self._do_isq_action(delete_action)

    def pvo_release_policy_message(self, name=None, date_range=None, esa_ip=None):
        self._open_page()
        self._click_edit_policy_link(name)
        self.click_button(SEARCH_QUARANTINE)
        if isinstance(date_range, basestring) and date_range.find(',') > 0:
            date_range = self._convert_to_tuple(date_range)
        self._search_msgs(date_range=date_range, esa_ip=esa_ip)
        release_action = self._release_action
        self._do_isq_action(release_action)

    def pvo_search_policy_message(self, name=None,  date_range=None):
        self._open_page()
        self._click_edit_policy_link(name)
        self.click_button(SEARCH_QUARANTINE)
        if isinstance(date_range, basestring) and date_range.find(',') > 0:
            date_range = self._convert_to_tuple(date_range)
        self._search_msgs(date_range=date_range)
        number_of_rows= int(self.get_element_count(MSG_INFO_ROW('*')))
        return  number_of_rows
