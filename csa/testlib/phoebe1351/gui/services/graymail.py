#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/services/graymail.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

import functools
import re

from common.gui.decorators import set_speed
from common.gui.guicommon import GuiCommon, Wait
import common.gui.guiexceptions as guiexceptions

GRAYMAIL_PAGE_PATH = ('Security Services', 'IMS and Graymail')

GRAYMAIL_XPATH         = "//*[@id='content']/form/dl/dd/table/tbody/tr[1]/td"

GRAYMAIL_ENABLED_XPATH = "//*[@id='content']/form/dl[1]/dd/table/tbody/tr[1]/td"
MAXIMUM_MSG_SIZE_XPATH = "//*[@id='content']/form/dl[1]/dd/table/tbody/tr[2]/td"
MSG_SCAN_TIMEOUT_XPATH = "//*[@id='content']/form/dl[1]/dd/table/tbody/tr[3]/td"
UNSUBSCRIPTION_XPATH   = "//*[@id='content']/form/dl[1]/dd/table/tbody/tr[4]/td"
AUTO_UPDATE_XPATH      = "//*[@id='content']/form/dl[1]/dd/table/tbody/tr[5]/td"

EDIT_SETTINGS_BUTTON  = "//input[@value='Edit Graymail Settings']"
MAXIMUM_MSG_SIZE      = "//input[@id='max_msg_size']"
MSG_SCAN_TIMEOUT      = "//input[@id='timeout']"
CANCEL_BUTTON         = "//input[@name='CancelSettings']"
ACCEPT_EULA           = "//input[@name='action:AcceptLicense']"
UPDATE_NOW_BUTTON     = "//input[@name='action:UpdateNow']"
UPDATE_RESULTS        = "//div[@id='status']"
UPDATE_RUNNING_MARK   = 'Getting update status'
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


def go_to_graymail(func):
    """
    This decorator is used to navigate and check GrayMail feature.

    *Exceptions:*
    - `GuiFeatureDisabledError`: if corresponding feature is disabled
    """

    @functools.wraps(func)
    def worker(self, *args, **kwargs):
        self._debug('Opening "%s" page' % (' -> '.join(GRAYMAIL_PAGE_PATH),))
        self._navigate_to(*GRAYMAIL_PAGE_PATH)

        if self._is_text_present(IPAS_OR_IMS_DISABLED_MARK):
            raise guiexceptions.GuiFeatureDisabledError('"GrayMail" feature '\
                'could not be enabled because IPAS or IMS is not enabled')

        return func(self, *args, **kwargs)
    return worker


class GrayMail(GuiCommon):
    """Keywords for ESA GUI interaction with
    Security Services -> Graymail Detection and Safe Un-Subscription
    """

    def get_keyword_names(self):
        return ['graymail_is_enabled',
                'graymail_enable',
                'graymail_disable',
                'graymail_edit_settings',
                'graymail_get_details',
                'graymail_update_now']

    @go_to_graymail
    @set_speed(0)
    def graymail_is_enabled(self):
        """
        Returns GrayMail feature state

        *Parameters:*
        None

        *Return:*
        True if GrayMail is enabled or False otherwise

        *Exceptions:*
        - `GuiFeaturekeyMissingError`: if corresponding feature key is not installed
        - `GuiFeatureDisabledError`: if corresponding feature is disabled

        *Examples:*
        | ${graymail_state}= | Graymail Is Enabled |
        """
        result = False
        graymail_detection = self.get_text(GRAYMAIL_XPATH)
        if graymail_detection.lower() != 'disabled':
            result = True
        return result

    @go_to_graymail
    @set_speed(0)
    def graymail_enable(self, **settings):
        """
        Enables GrayMail feature.

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
        | Graymail Enable |
        | Graymail Enable | enable_unsubscription=${True}  |
        | Graymail Enable | enable_unsubscription=${False} |
        | Graymail Enable | enable_autoupdate=${True} |
        """
        if not settings:
            settings['enable_unsubscription'] = False
        if self._is_element_present(EDIT_SETTINGS_BUTTON):
            self.click_button(EDIT_SETTINGS_BUTTON)
            self._select_checkbox(GRAYMAIL_DETECTION_ENABLE_CHECKBOX)
            self._click_submit_button()

            if settings.has_key('enable_unsubscription'):
                if settings['enable_unsubscription']:
                    gm_unsubscribe_status = self.get_text(UNSUBSCRIPTION_XPATH)
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

    @go_to_graymail
    @set_speed(0)
    def graymail_disable(self):
        """
        Disables GrayMail feature.

        *Exceptions:*
        - `GuiFeaturekeyMissingError`: if corresponding feature key is not installed
        - `GuiFeatureDisabledError`: if corresponding feature is disabled

        *Examples:*
        | Graymail Disable |
        """
        if self._is_element_present(EDIT_SETTINGS_BUTTON):
            self.click_button(EDIT_SETTINGS_BUTTON)
            self._unselect_checkbox(GRAYMAIL_DETECTION_ENABLE_CHECKBOX)
            self._click_submit_button()

    @go_to_graymail
    @set_speed(0)
    def graymail_edit_settings(self, **settings):
        """
        Edit Graymail settings

        *Parameters:*
        - `maximum_message_size`: Maximum Message Size to Scan
                                  Add a trailing K or M to indicate units.
                                  Recommended setting is 1024K(1MB) or less
        - `message_scanning_timeout`: Timeout for Scanning Single Message (seconds)
                                  Accepts integer value between 1 and 60.
        - `enable_unsubscription`: Boolean flag to enable Safe Un-subscription.
        - `enable_autoupdate`: Boolean paramter to enable or disable automatic update for Graymail.

        *Exceptions:*
        - `GuiFeaturekeyMissingError`: if corresponding feature key is not installed
        - `GuiFeatureDisabledError`: if corresponding feature is disabled

        *Examples:*
        | Graymail Edit Settings              |
        | ... | maximum_message_size=512K     |
        | ... | message_scanning_timeout=30   |
        | ... | enable_unsubscription=${True} |
        | ... | enable_autoupdate=${False} |
        """
        if settings:
            if self._is_element_present(EDIT_SETTINGS_BUTTON):
                self.click_button(EDIT_SETTINGS_BUTTON)
                if settings.has_key('maximum_message_size') and settings['maximum_message_size']:
                    self.input_text(MAXIMUM_MSG_SIZE, settings['maximum_message_size'])
                if settings.has_key('message_scanning_timeout') and settings['message_scanning_timeout']:
                    self.input_text(MSG_SCAN_TIMEOUT, settings['message_scanning_timeout'])
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

    @go_to_graymail
    @set_speed(0)
    def graymail_get_details(self):
        """
        Get GrayMail settings details.

        *Parameters:*
        None

        *Return:*
        Returns a dictionary containing the following keys:
            'Graymail Detection',
            'Maximum Message Size to Scan',
            'Timeout for Scanning Single Message',
            'Safe Un-subscription'
            'Auto Update'

        *Exceptions:*
        - `GuiFeaturekeyMissingError`: if corresponding feature key is not installed
        - `GuiFeatureDisabledError`: if corresponding feature is disabled

        *Examples:*
        | ${graymail_details} | Graymail Get Details |
        | Log Dictionary      | ${graymail_details}  |
        """
        details_dict = {}
        graymail_detection = self.get_text(GRAYMAIL_ENABLED_XPATH)
        details_dict['Graymail Detection'] = graymail_detection
        if graymail_detection.lower() != 'disabled':
            details_dict['Maximum Message Size to Scan'] = self.get_text(MAXIMUM_MSG_SIZE_XPATH)
            details_dict['Timeout for Scanning Single Message'] = self.get_text(MSG_SCAN_TIMEOUT_XPATH)
            details_dict['Safe Un-subscription'] = self.get_text(UNSUBSCRIPTION_XPATH)
            details_dict['Auto Update'] = self.get_text(AUTO_UPDATE_XPATH)
        return details_dict

    @go_to_graymail
    @set_speed(0)
    def graymail_update_now(self):
        """Force Graymail engine update

        *Parameters:* None

        *Examples:*
        | ${result}= | Graymail Update Now |
        """
        if self._is_element_present(UPDATE_NOW_BUTTON):
            self.click_button(UPDATE_NOW_BUTTON)
            Wait(until=self._is_text_present,
                msg='Update result has not been shown within 30 seconds timeout',
                timeout=30).\
                    wait(UPDATE_RUNNING_MARK)
            return self.get_text(UPDATE_RESULTS).strip()
        else:
            raise GuiControlNotFoundError('"Graymail" feature'\
                ' cannot be updated manually')
