#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/management/administration/feature_keys.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

import re

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon


INSTALLED_KEYS_TABLE = "//table[@class='cols'][1]"
INSTALLED_KEYS_ROW = '%s//tr' % (INSTALLED_KEYS_TABLE,)
PENDING_KEYS_TABLE = "//table[@class='cols'][2]"
PENDING_KEYS_ROW = '%s//tr' % (PENDING_KEYS_TABLE,)
PENDING_KEY_CHECKBOX = lambda index: '%s//tbody//tr[%s]/td/input/' %\
                                    (PENDING_KEYS_TABLE, index+2)
ACTIVATE_KEY_BUTTON = "//input[@value='Activate Selected Key(s)']"
KEY_DOWNLOAD_RESULT_TEXT = 'id=action-results-message'
CHECKNOW_BUTTON = "//input[@value='Check for New Keys']"
FEATURE_KEY_TEXTBOX = 'id=enter_fk'
SUBMIT_KEY_BUTTON = "//input[@value='Submit Key']"
ACCEPT_LICENSE_BUTTON = "//input[@value='Accept']"


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
               'Expiration Date: %s' % (repr(self.description), self.status,
                                        self.time_remaining, self.exp_date)


class FeatureKeys(GuiCommon):

    """Keywords for Management Appliance -> System Administration ->
    Feature Keys
    """

    def get_keyword_names(self):
        return ['feature_keys_get_key',
                'feature_keys_get_all_keys',
                'feature_keys_check_new_keys',
                'feature_keys_activate',
                'feature_keys_submit',
                ]

    def _open_page(self):
        self._navigate_to('Management', 'System Administration',
            'Feature Keys')

    def _get_installed_keys(self):
        result = []
        starting_row = 1
        num_of_rows = int(self.get_matching_xpath_count(INSTALLED_KEYS_ROW))
        num_of_columns = 4
        for row in xrange(starting_row, num_of_rows):
            key_values = map(lambda column: self._get_table_cell('%s.%s.%s'
                                % (INSTALLED_KEYS_TABLE, row, column)),
                                xrange(num_of_columns))
            result += (FeatureKeyInfo(*key_values),)

        return result

    def _get_pending_keys(self):
        starting_row = 1
        num_of_rows = int(self.get_matching_xpath_count(PENDING_KEYS_ROW))
        desc_column = 1
        pending_keys = map(lambda row: self._get_table_cell(
                                       PENDING_KEYS_TABLE, row, desc_column),
                           xrange(starting_row, num_of_rows))
        return pending_keys

    def _click_activate_checkbox(self, keys):
        if self._is_text_present('No feature key activations are pending'):
            raise guiexceptions.ConfigError('Feature keys pending ' +
                                            'activation are not present')

        pending_keys = self._get_pending_keys()
        for key in keys:
            if key not in pending_keys:
                raise guiexception.GuiValueError(
                    '"%s" is not present in pending keys table' % (key,))
            self.select_checkbox(PENDING_KEY_CHECKBOX(pending_keys.index(key)))

    def _click_activate_key_button(self):
        self.click_button(ACTIVATE_KEY_BUTTON)
        self._check_action_result()

    def _click_checknow_button(self):
        self.click_button(CHECKNOW_BUTTON)
        self._check_action_result()

    def _get_downloaded_keys(self):
        keys_dict = {}
        key_patt = re.compile('(.*?)\s+\((\S+?)\)')
        download_result = self._get_text(KEY_DOWNLOAD_RESULT_TEXT)

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

    def feature_keys_get_key(self, key):
        """Get information about installed feature key.

        Parameters:
        - `key`: a description of feature key. String.

        Return:
        An object containing information about found feature key, ${EMPTY}
        otherwise.
        The object has the following attributes:
            - `description`: feature key description.
            - `status`: status of feature key.
            - `time_remaining`: remaining time for feature key to expire.
            - `exp_date`: expiration date of feature key.

        Examples:
        | ${key} = | Feature Keys Get Key |
        | ... | Cisco IronPort Centralized Email Reporting |
        """
        self._open_page()

        installed_keys = self._get_installed_keys()

        for key_info in installed_keys:
            if key in key_info.description:
                return key_info
        return ''

    def feature_keys_get_all_keys(self):
        """Get information about all installed feature keys.

        Return:
        A list of objects containing information about installed keys.
        Each object has the following attributes:
            - `description`: feature key description.
            - `status`: status of feature key.
            - `time_remaining`: remaining time for feature key to expire.
            - `exp_date`: expiration date of feature key.


        Examples:
        | @keys = | Feature Keys Get All Keys |
        """
        self._open_page()

        return self._get_installed_keys()

    def feature_keys_check_new_keys(self):
        """Check for new feature keys.

        Return:
        A dictionary of {key_name: key_value} of new keys, empty dictionary if
        no keys were downloaded.

        Example:
        | ${new_keys} = | Feature Keys Check New Keys |
        """
        self._open_page()

        self._click_checknow_button()

        return self._get_downloaded_keys()

    def feature_keys_activate(self, keys):
        """Activate pending feature key(s).

        Parameters:
        - `keys`: a string of comma-separated keys names to activate.

        Examples:
        | Feature Keys Activate | Cisco IronPort Centralized Web Reporting |
        | Feature Keys Activate | Cisco IronPort Centralized Web Reporting, Cisco IronPort Spam Quarantine |

        Exceptions:
        - `GuiValueError`: in case any of the keys is not present in the
           pending activation table.
        - `ConfigError`: in case there are no feature keys pending
           activation.
        """
        self._open_page()

        self._click_activate_checkbox(self._convert_to_tuple(keys))

        self._click_activate_key_button()

        self._accept_license()

    def feature_keys_submit(self, key):
        """Submit new feature key.

        Parameters:
        - `key`: feature key to submit.

        Examples:
        | Feature Keys Submit |
        | ... | VvCdi-cpGQU-ap6wI-Bhsg2-or/sM-lOmpZ-uaIAf-RAbT4-lYg= |

        Exceptions:
        - `GuiValueError`: in case feature key is malformed.
        """
        self._open_page()

        self._fill_feature_key_textbox(key)

        self._click_submit_key_button()

        self._accept_license()


