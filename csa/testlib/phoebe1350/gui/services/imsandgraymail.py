#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/services/imsandgraymail.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

import functools
import re
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon, Wait

GRAYMAIL_XPATH        = "//*[@id='content']/form/dl[1]/dd/table/tbody/tr[1]/td"
IMS_AND_GRAYMAIL_PATH = "//*[@id='content']/form/dl[2]/dd/table/tbody/tr[1]/td"
IMS_GLOBAL_SETTING_HEADER = "//*[@id='content']/form/dl[1]/dt"
IMS_AND_GRAYMAIL_ENABLED_PATH = "//*[@id='content']/form/dl[2]/dd/table/tbody/tr[1]/td"
GRAYMAIL_UNSUBSCRIPTION_XPATH   = "//*[@id='content']/form/dl[1]/dd/table/tbody/tr[2]/td"
IMS_AND_GRAYMAIL_UNSUBSCRIPTION_XPATH = "//*[@id='content']/form/dl[2]/dd/table/tbody/tr[2]/td"
AUTO_UPDATE_XPATH      = "//*[@id='content']/form/dl[1]/dd/table/tbody/tr[3]/td"
IMS_AND_AUTO_UPDATE_XPATH      = "//*[@id='content']/form/dl[2]/dd/table/tbody/tr[3]/td"
MAXIMUM_MSG_SIZE_XPATH = "//*[@id='content']/form/dl[2]/dd/table/tbody/tr[1]/td"
IMS_AND_MAXIMUM_MSG_SIZE_XPATH = "//*[@id='content']/form/dl[3]/dd/table/tbody/tr[1]/td"
MSG_SCAN_TIMEOUT_XPATH = "//*[@id='content']/form/dl[2]/dd/table/tbody/tr[2]/td"
IMS_AND_MSG_SCAN_TIMEOUT_XPATH = "//*[@id='content']/form/dl[3]/dd/table/tbody/tr[2]/td"
IMS_LABEL_XPATH = "//*[@id='content']/form/dl[1]/dd/table/tbody/tr/th"
IMS_ENABLE_BUTTON = "//input[@value='Enable...']"
ACCEPT_LICENSE='action:AcceptLicense'
ENABLE_CHECKBOX='enabled'
SAVE_SETTINGS_BUTTON='SaveSettings'
REG_SCAN = lambda reg_scan: 'region_enable_%s' %reg_scan
REGION_ENABLE_ON='region_enable_on'
REGION='region'
SCAN_REGION= lambda scan_region: 'label=%s' %scan_region
EDIT_IMS_SETTINGS  = "//input[@value='Edit IMS Settings']"
EDIT_SETTINGS_BUTTON  = "//input[@value='Edit Graymail Settings']"
EDIT_GLOBAL_SETTINGS_BUTTON  = "//input[@value='Edit Global Settings']"
MAXIMUM_MSG_SIZE      = "//input[@id='max_msg_size']"
SMALL_MSG_SIZE        = "//input[@id='adv_msg_size']"
MSG_SCAN_TIMEOUT      = "//input[@id='timeout']"
CANCEL_BUTTON         = "//input[@name='CancelSettings']"
ACCEPT_EULA           = "//input[@name='action:AcceptLicense']"
UPDATE_NOW_BUTTON     = "//input[@name='action:UpdateNow']"
UPDATE_RESULTS        = "//div[@id='status']"
UPDATE_RUNNING_MARK   = 'Updates in progress.'
ENABLE_SAFE_UNSUBSCRIBE_BUTTON  = "//input[@value='Enable']"
GRAYMAIL_DETECTION_ENABLE_CHECKBOX = \
    "//input[contains(@id, 'enabled_detection') and @type='checkbox']"
GRAYMAIL_UNSUBSCRIPTION_ENABLE_CHECKBOX = \
    "//input[contains(@id, 'enabled_unsubscription') and @type='checkbox']"
GRAYMAIL_AUTOMATIC_UPDATES_CHECKBOX = \
    "//input[contains(@id, 'enable_autoupdate') and @type='checkbox']"
NO_FKEY_MARK              = 'The feature key for this feature has expired or is unavailable'
GM_UNSUBSCRIBE_DISABLED   = 'Graymail Safe Unsubscribing is currently disabled'
IPAS_OR_IMS_DISABLED_MARK = 'This feature cannot be used until the Ironport Anti-Spam is enabled'
IMS_DISABLED = 'IronPort Intelligent Multi-Scan is currently disabled globally'
IMS_AND_GRAYMAIL_PAGE_PATH = ('Security Services', 'IMS and Graymail')

def go_to_ims_and_graymail(func):
    """
    This decorator is used to navigate and check IMS and GrayMail feature.
    *Exceptions:*
    - `GuiFeatureDisabledError`: if corresponding feature is disabled
    """
    @functools.wraps(func)
    def worker(self, *args, **kwargs):
        self._debug('Opening "%s" page' % (' -> '.join(IMS_AND_GRAYMAIL_PAGE_PATH),))
        self._navigate_to(*IMS_AND_GRAYMAIL_PAGE_PATH)
        if self._is_text_present(IPAS_OR_IMS_DISABLED_MARK):
            raise guiexceptions.GuiFeatureDisabledError('"IMS/GrayMail". '\
                'This feature cannot be used until the Ironport Anti-Spam is enabled')
        return func(self, *args, **kwargs)
    return worker


class ImsGraymail(GuiCommon):
    """Keywords for ESA GUI interaction with
    Security Services -> IMS and Graymail Detection
    """
    def get_keyword_names(self):
        return ['ims_and_graymail_graymail_is_enabled',
                'ims_and_graymail_graymail_enable',
                'ims_and_graymail_graymail_disable',
                'ims_and_graymail_graymail_edit_settings',
                'ims_and_graymail_graymail_get_details',
                'ims_and_graymail_update_now',
                'ims_and_graymail_ims_is_enabled',
                'ims_and_graymail_ims_enable',
                'ims_and_graymail_ims_edit_settings',
                'ims_and_graymail_ims_global_settings_exists',
                'ims_and_graymail_global_edit_settings',
                'ims_and_graymail_ims_disable',
                'ims_and_graymail_get_rule_details']

    @go_to_ims_and_graymail
    def ims_and_graymail_ims_is_enabled(self):
        """
        Check the IMS feature is enabled on IMS and Graymail
        :return:
        """
        if self._is_text_present(IMS_DISABLED):
            return False
        if 'Ironport Intelligent Multi-Scan' in self.get_text(IMS_LABEL_XPATH) \
                and self.get_text(GRAYMAIL_XPATH).lower() != 'disabled':
            return True
        else:
            return False

    @go_to_ims_and_graymail
    def ims_and_graymail_ims_enable(self):
        """
            Enables IronPort Intelligent Multi-Scan
            *Parameter*:
              None

            *Return*:
              None

            *Examples*:
              | IMS and Graymail IMS Enable |
        """
        self._info("Enabling IronPort Intelligent Multi-Scan")
        if self.ims_and_graymail_ims_is_enabled():
            self._info("IronPort Intelligent Multi-Scan is already enabled")
            return True
        self.click_button(locator=IMS_ENABLE_BUTTON)
        if self._is_text_present('License Agreement'):
            self.click_button(locator=ACCEPT_LICENSE)

    @go_to_ims_and_graymail
    def ims_and_graymail_ims_disable(self):
        """
           Disables IronPort Intelligent Multi-Scan

           *Parameter*:
             None

           *Return*:
             None

           *Examples*:

             | IMS and Graymail IMS Disable |
        """

        self._info("Disabling IronPort Intelligent Multi-Scan")
        if not self.ims_and_graymail_ims_is_enabled():
            self._info("IronPort Intelligent Multi-Scan is already disabled")
            return True
        self.click_button(locator=EDIT_IMS_SETTINGS)
        self._unselect_checkbox(ENABLE_CHECKBOX)
        self.click_button(locator=SAVE_SETTINGS_BUTTON)

    @go_to_ims_and_graymail
    def ims_and_graymail_ims_global_settings_exists(self):
        """
        Checks the IMS Global settings is visible

        :return: True or False
        """
        if 'IMS Global Settings' in self.get_text(IMS_GLOBAL_SETTING_HEADER):
            return True
        else:
            return False

    @go_to_ims_and_graymail
    def ims_and_graymail_ims_edit_settings(self,
                 timeout=None,
                 reg_scan=None,
                 reg_scan_region=None):
        """Edit IMS settings on IMS and Graymail.
           *Parameters*:
            - `reg_scan` : Regional Scanning. on or off
            - `reg_scan_region` : Regional Scanning Region
                  Values can be China
           *Return*:
             None

           *Examples*:
           | IMS and Graymail IMS EDIT SETTINGS| reg_scan=on | reg_scan_region=China |
        """
        if self.ims_and_graymail_ims_is_enabled():
            self.click_button(EDIT_IMS_SETTINGS)
            if reg_scan:
               if self._is_element_present(REG_SCAN(reg_scan.lower())):
                   self._click_radio_button(REG_SCAN(reg_scan.lower()))
                   if reg_scan_region and self._is_checked(locator=REGION_ENABLE_ON):
                       self.select_from_list(REGION,SCAN_REGION(reg_scan_region))
            self.click_button(SAVE_SETTINGS_BUTTON)
        else:
            raise guiexceptions.GuiError(IMS_DISABLED)

    @go_to_ims_and_graymail
    def ims_and_graymail_graymail_is_enabled(self):
        """
        Returns Graymail Detection enabled or disabled on IMS and GrayMail.

        *Parameters:*
        None

        *Return:*
        True if GrayMail is enabled or False otherwise

        *Exceptions:*
        - `GuiFeaturekeyMissingError`: if corresponding feature key is not installed
        - `GuiFeatureDisabledError`: if corresponding feature is disabled

        *Examples:*
        | ${graymail_state}= | IMS and Graymail Graymail Is Enabled |
        """
        result = False
        if self.ims_and_graymail_ims_global_settings_exists() :
            graymail_detection = self.get_text(IMS_AND_GRAYMAIL_PATH)
        else:
            graymail_detection = self.get_text(GRAYMAIL_XPATH)
        if graymail_detection.lower() != 'disabled':
            result = True
        return result

    @go_to_ims_and_graymail
    def ims_and_graymail_graymail_enable(self, **kwargs):
        """
        Enables Graymail feature on IMS and Graymail.

        *Parameters:*
        - `enable_unsubscription`: Boolean flag to enable
           Safe Un-Subscription feature with GrayMail.
           Default value: ${False}
        - `enable_autoupdate`: Boolean paramter to enable
           or disable automatic update for Graymail.

        *Exceptions:*
        - `GuiFeaturekeyMissingError`: if corresponding feature key is not installed
        - `GuiFeatureDisabledError`: if corresponding feature is disabled

        *Examples:*
        | IMS and Graymail Graymail Enable |
        | IMS and Graymail Graymail Enable | enable_unsubscription=${True}  |
        | IMS and Graymail Graymail Enable | enable_unsubscription=${False} |
        | IMS and Graymail Graymail Enable | enable_autoupdate=${True} |
        """
        settings = self._parse_args(kwargs)
        if not settings:
            settings['enable_unsubscription'] = False

        if self.ims_and_graymail_ims_global_settings_exists() :
            GRAYMAIL_UNSUBSCRIPTION_XPATH = IMS_AND_GRAYMAIL_UNSUBSCRIPTION_XPATH

        if self._is_element_present(EDIT_SETTINGS_BUTTON):
            self.click_button(EDIT_SETTINGS_BUTTON)
            self._select_checkbox(GRAYMAIL_DETECTION_ENABLE_CHECKBOX)
            self._click_submit_button()

            if settings.has_key('enable_unsubscription'):
                if settings['enable_unsubscription']:
                    gm_unsubscribe_status = self.get_text(GRAYMAIL_UNSUBSCRIPTION_XPATH)
                    if re.search(NO_FKEY_MARK, gm_unsubscribe_status, re.I):
                        raise guiexceptions.GuiFeaturekeyMissingError(
                            '"GrayMail Safe-Unsubscribe" feature could not be reached' \
                            ' because the corresponding feature key is not installed')

                    elif re.search(GM_UNSUBSCRIBE_DISABLED, gm_unsubscribe_status, re.I):
                        if self._is_element_present(ENABLE_SAFE_UNSUBSCRIBE_BUTTON):
                            self.click_button(ENABLE_SAFE_UNSUBSCRIBE_BUTTON)
                            if self._is_text_present('License Agreement'):
                                self.click_button(ACCEPT_EULA)

                    elif re.search('Disabled', gm_unsubscribe_status, re.I):
                        self.click_button(EDIT_SETTINGS_BUTTON)
                        if self._is_element_present(GRAYMAIL_UNSUBSCRIPTION_ENABLE_CHECKBOX):
                            self._select_checkbox(GRAYMAIL_UNSUBSCRIPTION_ENABLE_CHECKBOX)
                            self._click_submit_button()
                    elif re.search('Enabled', gm_unsubscribe_status, re.I):
                        self._info('INFO: Graymail Safe-Unsubscribe is already enabled')
                    else:
                        raise guiexceptions.GuiError("Unknown status for 'Safe-Unsubscribe' feature.")
                else:
                    self.click_button(EDIT_SETTINGS_BUTTON)
                    if self._is_element_present(GRAYMAIL_UNSUBSCRIPTION_ENABLE_CHECKBOX):
                        self._unselect_checkbox(GRAYMAIL_UNSUBSCRIPTION_ENABLE_CHECKBOX)
                    self._click_submit_button()

            if settings.has_key('enable_autoupdate'):
                self.click_button(EDIT_SETTINGS_BUTTON)
                if settings['enable_autoupdate']:
                    self._select_checkbox(GRAYMAIL_AUTOMATIC_UPDATES_CHECKBOX)
                else:
                    self._unselect_checkbox(GRAYMAIL_AUTOMATIC_UPDATES_CHECKBOX)
                self._click_submit_button()
        elif self._is_element_present(CANCEL_BUTTON):
            self.click_button(CANCEL_BUTTON)
        else:
            raise guiexceptions.GuiError('Unknown page')


    @go_to_ims_and_graymail
    def ims_and_graymail_graymail_disable(self):
        """
        Disables Graymail feature on  IMS and GrayMail feature.

        *Exceptions:*
        - `GuiFeaturekeyMissingError`: if corresponding feature key is not installed
        - `GuiFeatureDisabledError`: if corresponding feature is disabled

        *Examples:*
        | IMS and Graymail Graymail Disable |
        """
        if self._is_element_present(EDIT_SETTINGS_BUTTON):
            self.click_button(EDIT_SETTINGS_BUTTON)
            self._unselect_checkbox(GRAYMAIL_DETECTION_ENABLE_CHECKBOX)
            self._click_submit_button()

    @go_to_ims_and_graymail
    def ims_and_graymail_graymail_edit_settings(self, **kwargs):
        """
        Edit Graymail setting on IMS and Graymail.

        *Parameters:*
        - `enable_unsubscription`: Boolean flag to enable Safe Un-subscription.
        - `enable_autoupdate`: Boolean paramter to enable or disable automatic update for Graymail.

        *Exceptions:*
        - `GuiFeaturekeyMissingError`: if corresponding feature key is not installed
        - `GuiFeatureDisabledError`: if corresponding feature is disabled

        *Examples:*
        | IMS And Graymail Graymail Edit Settings|
        | ... | enable_unsubscription=${True} |
        | ... | enable_autoupdate=${False} |
        """
        settings = self._parse_args(kwargs)
        if settings:
            if self._is_element_present(EDIT_SETTINGS_BUTTON):
                self.click_button(EDIT_SETTINGS_BUTTON)
                if settings.has_key('enable_unsubscription'):
                    if settings['enable_unsubscription']:
                        self._select_checkbox(GRAYMAIL_UNSUBSCRIPTION_ENABLE_CHECKBOX)
                    else:
                        self._unselect_checkbox(GRAYMAIL_UNSUBSCRIPTION_ENABLE_CHECKBOX)
                if settings.has_key('enable_autoupdate'):
                    if settings['enable_autoupdate']:
                        self._select_checkbox(GRAYMAIL_AUTOMATIC_UPDATES_CHECKBOX)
                    else:
                        self._unselect_checkbox(GRAYMAIL_AUTOMATIC_UPDATES_CHECKBOX)
                self._click_submit_button()
            elif self._is_element_present(CANCEL_BUTTON):
                self.click_button(CANCEL_BUTTON)
            else:
                raise guiexceptions.GuiError('Unknown page')

    @go_to_ims_and_graymail
    def ims_and_graymail_global_edit_settings(self, **kwargs):
        """
        Edit IMS and Graymail Global Settings

        *Parameters:*
        - `maximum_message_size`: Maximum Message size threshold
        - `message_scanning_timeout` : Message Scannig Timeout
        - `small_message_size`: Smaller Message size threshold

        *Examples:*
        | IMS And Graymail Global Edit Settings  |
        | ... | maximum_message_size=1M |
        | ... | small_message_size=512K |
        | ... | message_scanning_timeout=60 |
        """
        settings = self._parse_args(kwargs)
        if settings:
            if self._is_element_present(EDIT_GLOBAL_SETTINGS_BUTTON):
                self.click_button(EDIT_GLOBAL_SETTINGS_BUTTON)
                if settings.has_key('maximum_message_size') and settings['maximum_message_size']:
                    self.input_text(MAXIMUM_MSG_SIZE, settings['maximum_message_size'])
                if settings.has_key('small_message_size') and settings['small_message_size']:
                    self.input_text(SMALL_MSG_SIZE, settings['small_message_size'])
                if settings.has_key('message_scanning_timeout') and settings['message_scanning_timeout']:
                    self.input_text(MSG_SCAN_TIMEOUT, settings['message_scanning_timeout'])
                self._click_submit_button()
            elif self._is_element_present(CANCEL_BUTTON):
                self.click_button(CANCEL_BUTTON)
            else:
                raise guiexceptions.GuiError('Unknown page')

    @go_to_ims_and_graymail
    def ims_and_graymail_graymail_get_details(self):
        """
        Get IMS and GrayMail settings details.

        *Parameters:*
        None

        *Return:*
        Returns a dictionary containing the following keys:
            'Graymail Detection',
            'Message Scanning Thresholds',
            'Timeout for Scanning Single Message',
            'Safe Un-subscription'
            'Auto Update'

        *Exceptions:*
        - `GuiFeaturekeyMissingError`: if corresponding feature key is not installed
        - `GuiFeatureDisabledError`: if corresponding feature is disabled

        *Examples:*
        | ${graymail_details} | IMS and Graymail Graymail Get Details |
        | Log Dictionary      | ${graymail_details}  |
        """
        details_dict = {}

        if self.ims_and_graymail_ims_global_settings_exists():
            GRAY_MAIL_DETECTION = IMS_AND_GRAYMAIL_ENABLED_PATH
            UNSUBSCRIPTION_XPATH = IMS_AND_GRAYMAIL_UNSUBSCRIPTION_XPATH
            AUTO_UPDATE_XPATH = IMS_AND_AUTO_UPDATE_XPATH
            MSG_SCAN_TIMEOUT_XPATH = IMS_AND_MSG_SCAN_TIMEOUT_XPATH
            MAXIMUM_MSG_SIZE_XPATH = IMS_AND_MAXIMUM_MSG_SIZE_XPATH
        else:
            GRAY_MAIL_DETECTION = GRAYMAIL_XPATH
            UNSUBSCRIPTION_XPATH = GRAYMAIL_UNSUBSCRIPTION_XPATH


        graymail_detection = self.get_text(GRAY_MAIL_DETECTION)
        details_dict['Graymail Detection'] = graymail_detection
        if graymail_detection.lower() != 'disabled':
            details_dict['Message Scanning Thresholds'] = self.get_text(MAXIMUM_MSG_SIZE_XPATH)
            details_dict['Timeout for Scanning Single Message'] = self.get_text(MSG_SCAN_TIMEOUT_XPATH)
            details_dict['Safe Un-subscription'] = self.get_text(UNSUBSCRIPTION_XPATH)
            details_dict['Auto Update'] = self.get_text(AUTO_UPDATE_XPATH)
        return details_dict

    @go_to_ims_and_graymail
    def ims_and_graymail_update_now(self):
        """Force IMS and Graymail engine update
        *Parameters:* None
        *Examples:*
        | ${result}= | IMS and Graymail Update Now |
        """
        if self._is_element_present(UPDATE_NOW_BUTTON):
            self.click_button(UPDATE_NOW_BUTTON)
            Wait(until=self._is_text_present,
                msg='Update result has not been shown within 60 seconds timeout',
                timeout=120).\
                    wait(UPDATE_RUNNING_MARK)
            return self.get_text(UPDATE_RESULTS).strip()
        else:
            raise guiexceptions.GuiControlNotFoundError('Update now option is not visible/active')

    @go_to_ims_and_graymail
    def ims_and_graymail_get_rule_details(self):
        """Return IMS and Graymail Rule Details
        *Return:*
        Dictionary which items are:
        each list item is dictionary and has the format:
        | `File Type` | <name of item> |
        | `Last Update` | <timestamp of last update> |
        | `Current Version` | <current item's version> |
        | `New Update`      | <New update status> |
        *Examples:*
        | ${details}= | IMS and Graymail Get Rule Details |
        | Log Many | {details} |
        """
        INFO_TABLE = "//table[@class='cols']"
        INFO_TABLE_ROWS = "%s//tr" % (INFO_TABLE,)
        INFO_TABLE_HEADERS_MAP = {'File Type': 1, 'Last Update': 2, 'Current Version': 3, 'New Update': 4}
        INFO_TABLE_CELL = lambda header, row: "%s//tr[%d]/td[%d]" % \
                                              (INFO_TABLE, row, INFO_TABLE_HEADERS_MAP[header])
        details_dict = {}
        info_rows_count = int(self.get_matching_xpath_count(INFO_TABLE_ROWS)) - 1
        for row_num in xrange(2, 2 + info_rows_count):
            one_row_dict = {}
            for col_name in INFO_TABLE_HEADERS_MAP.iterkeys():
                one_row_dict[col_name] = self.get_text(INFO_TABLE_CELL(col_name, row_num)).strip()
            file_type = one_row_dict['File Type']
            one_row_dict.pop('File Type')
            details_dict[file_type] = one_row_dict
        return details_dict
