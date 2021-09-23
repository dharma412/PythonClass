#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/admin/feature_keys.py#1 $

import re
import time
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon

INSTALLED_KEYS_TABLE = '//table[@id="installed_feature_keys"]'
INSTALLED_KEYS_ROW = '%s//tr' % (INSTALLED_KEYS_TABLE,)
PENDING_KEYS_TABLE = '//table[@class=\'cols\'][2]'
PENDING_KEYS_ROW = '%s//tr' % (PENDING_KEYS_TABLE,)
PENDING_KEY_CHECKBOX = lambda index: '%s//tbody//tr[%s]/td/input' % \
                                    (PENDING_KEYS_TABLE, index + 2)
ACTIVATE_KEY_BUTTON = 'xpath=//input[@value="Activate Selected Key(s)"]'
KEY_DOWNLOAD_RESULT_TEXT = 'id=action-results-message'
CHECKNOW_BUTTON = 'xpath=//input[@value="Check for New Keys"]'
FEATURE_KEY_TEXTBOX = 'id=enter_fk'
SUBMIT_KEY_BUTTON = 'xpath=//input[@value="Submit Key"]'


class FeatureKeyInfo:

    """Container for holding information regarding installed feature keys.

    :Attributes:
        - `description`: feature key description.
        - `status`: status of feature key.
        - `time_remaining`: remaining time for feature key to expire.
        - `exp_date`: expiration date of feature key.
    """

    def __init__(self, description, status, time_remaining, exp_date):
        self.description = description
        self.status = status
        self.time_remaining = time_remaining
        self.exp_date = exp_date

    def __str__(self):
        return 'Description: %s, Status: %s, Time Remaining: %s, '\
               'Expiration Date: %s' % (self.description, self.status,
                                        self.time_remaining, self.exp_date)

class FeatureKeys(GuiCommon):
    """Keywords for interaction with 'System Administration -> Feature Keys'
       page.
    """

    def get_keyword_names(self):
        return ['feature_keys_get_key',
                'feature_keys_get_all_keys',
                'feature_keys_check_new_keys',
                'feature_keys_activate',
                'feature_keys_submit'
                ]

    def _open_feature_keys_page(self):
        #self._navigate_to('System Administration', 'Feature Keys')
        ###navigate to feature keys page is failing, adding temp fix till a permenant fix is applied.
        self.mouse_over("//a[contains(text(),'System Administration')]")
        self.click_link("xpath=//a[contains(text(),'Feature Keys')]")

    def _get_installed_keys(self):
        result = ()
        starting_row = 1
        num_of_rows = int(self.get_matching_xpath_count(INSTALLED_KEYS_ROW))

        num_of_columns = 4
        try:
            old_speed = self.set_selenium_speed(0)
            for row in xrange(starting_row, num_of_rows):
                key_values = map(lambda column: self._get_table_cell('%s.%s.%s'\
                    % ('xpath=' + INSTALLED_KEYS_TABLE, row, column)),
                        xrange(num_of_columns))

                result += (FeatureKeyInfo(*key_values),)
        finally:
            self.set_selenium_speed(old_speed)

        return result

    def _get_pending_keys(self):
        starting_row = 1
        num_of_rows = int(self.get_matching_xpath_count(PENDING_KEYS_ROW))
        desc_column = 1
        try:
            old_speed = self.set_selenium_speed(0)
            pending_keys = map(lambda row: self._get_table_cell('%s.%s.%s'\
                % ('xpath=' + PENDING_KEYS_TABLE, row, desc_column)),
                    xrange(starting_row, num_of_rows))
        finally:
            self.set_selenium_speed(old_speed)

        return pending_keys

    def _click_activate_checkbox(self, keys):
        if self._is_text_present('No feature key activations are '
                                 'pending'):
            raise guiexceptions.ConfigError('Feature keys pending activation '
                                            'are not present')

        pending_keys = self._get_pending_keys()
        for key in keys:
            if key not in pending_keys:
                raise ValueError('"%s" is not present in pending keys table' % \
                                 (key,))
            self.select_checkbox(PENDING_KEY_CHECKBOX(pending_keys.index(key)))

    def _click_activate_key_button(self):
        self.click_button(ACTIVATE_KEY_BUTTON)
        self._check_action_result()

    def _click_checknow_button(self):
        self.click_button(CHECKNOW_BUTTON)
        self._check_action_result()

    def _get_downloaded_keys(self):
        keys_dict = {}
        # regexp that matches 'feature-key-string (component)'
        key_patt = re.compile('(.*?)\s+\((\S+?)\)')
        download_result = self.get_text(KEY_DOWNLOAD_RESULT_TEXT)

        for line in download_result.splitlines():
            result = key_patt.search(line)
            if result:
                key_name, key_value = result.groups()[::-1]
                keys_dict[key_name] = key_value
        return keys_dict

    def _fill_feature_key_textbox(self, key):
        self.input_text(FEATURE_KEY_TEXTBOX, key)

    def _click_submit_key_button(self):
        self.click_button(SUBMIT_KEY_BUTTON)
        self._check_action_result()

    def feature_keys_get_key(self, key):
        """Get information about installed feature key.

        Parameters:
        - `key`: a description of feature key.

        Returns information as string: 'Description: text, Status: text,
        Time Remaining: text, Expiration Date: text', or None if there is no
        such key.

        Example:
        | ${output}= | Feature Keys Get Key | Cisco IronPort L4 Traffic Monitor |
        """

        self._open_feature_keys_page()
        installed_keys = self._get_installed_keys()
        for key_info in installed_keys:
            if key in key_info.description:
                return key_info.__str__()
        return None

    def feature_keys_get_all_keys(self, dictionary=False):
        """Get information about all installed feature keys.

        Parameters:
        - `dictionary`: Default ${False} to returns a string with result.
         If ${True} then returned result will be dictionary.

        Return:
         Information about all installed feature keys as string
         separated by ';': 'Description: text, Status: text, Time Remaining: text,
         Expiration Date: text;Description: text, Status: text,
         Time Remaining: text, Expiration Date: text;...'
         If `dictionary` parameter is ${True} then return dictionary where
         feature key description is a key and value is a list of text strings
         containing other parameters: Status, Time Remaining and Expiration Date.

        Example:
        | ${output}= | Feature Keys Get All Keys |
        | ${output}= | Feature Keys Get All Keys | dictionary=${True} |
        """

        self._open_feature_keys_page()
        installed_keys = self._get_installed_keys()
        if not(dictionary):
            result = ()
            for key in installed_keys:
                result += (key.__str__(),)
            return ';'.join(result)
        else:
            result = {}
            for key in installed_keys:
                str = key.__str__()
                temp = str.split(',')
                for index in range(len(temp)):
                    temp[index] = temp[index].split(':',1)[1]
                result[temp[0]] = temp[1:]
            return result

    def feature_keys_check_new_keys(self):
        """Check for new feature keys.

        Parameters:
            None.

        Returns string in the form: 'Description: text, Duration: text;...'
        of new keys, empty string if no keys were downloaded.

        Example:
        | ${output}= | Feature Keys Check New Keys |
        """

        self._open_feature_keys_page()
        self._click_checknow_button()
        downloaded_keys = self._get_downloaded_keys()
        result = ()
        for key_name in downloaded_keys:
            result += ('Description: %s, Duration: %s'\
                        % (key_name, downloaded_keys[key_name]),)
        return ';'.join(result)

    def feature_keys_activate(self, keys):
        """Activate pending feature key(s).

        Parameters:
        - `keys`: a comma separated values of key descriptions to activate.

        Example:
        | Feature Keys Activate | Cisco IronPort Web Proxy & DVS(TM) Engine,Cisco IronPort L4 Traffic Monitor |
        """

        accept_license_button = 'action:AcceptLicense'
        self._open_feature_keys_page()
        self._click_activate_checkbox(self._convert_to_tuple(keys))
        self._click_activate_key_button()
        if self._is_text_present('License Agreement'):
            self.click_button(accept_license_button)

    def feature_keys_submit(self, key):
        """Submit new feature key.

        Parameters:
        - `key`: key to submit.

        Example:
        | Feature Keys Submit | generated key |
        """

        accept_license_button = 'action:AcceptLicense'
        self._open_feature_keys_page()
        self._fill_feature_key_textbox(key)
        self._click_submit_key_button()
        if self._is_text_present('License Agreement'):
                self.click_button(accept_license_button)
