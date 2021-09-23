#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/services/antivirus.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $


import functools

from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

ENABLE_BUTTON = "//input[@value='Enable...']"
ENABLE_CHECKBOX = "//input[@id='enabled']"
ACCEPT_LICENCE_BUTTON = "//input[@name='action:AcceptLicense']"
EDIT_SETTINGS_BUTTON = "//input[@value='Edit Global Settings...']"
TIMEOUT_EDIT = "//input[@id='timeout_id']"
UPDATENOW_BUTTON = "//input[@name='action:UpdateNow']"
ACTION_RESULTS = "//td[@id='action-results-message']"
AUTO_UPDATE_CHECKBOX = "//input[@id='autoupdate_enabled']"


def check_antivirus_feature(need_to_raise_exc):
    """This decorator is used to navigate and check Antivirus -> Sophos
    and Antivirus -> McAfee features. Decorator can be applied only to
    Antivirus class methods whose first parameter is provider name
    (either Sophos or McAfee)

    *Parameters:*
    - `need_to_raise_exc`: whether to raise GuiFeatureDisabledError if
    antivirus feature is disabled. Either True or False

    *Exceptions:*
    - `GuiFeatureDisabledError`: if corresponding feature is disabled
    and need_to_raise_exc is set to True
    """

    def decorator(func):
        @functools.wraps(func)
        def worker(self, provider, *args, **kwargs):
            if not self.antivirus_is_enabled(provider):
                if need_to_raise_exc:
                    raise guiexceptions.GuiFeatureDisabledError(
                        '%s antivirus feature is not enabled' % \
                        (provider,))
            return func(self, provider, *args, **kwargs)

        return worker

    return decorator


class Antivirus(GuiCommon):
    """Keywords for ESA GUI interaction with Security Services ->
    Sophos Anti-Virus and Security Services -> McAfee Anti-Virus
    pages
    """

    def get_keyword_names(self):
        return ['antivirus_is_enabled',
                'antivirus_enable',
                'antivirus_disable',
                'antivirus_edit_settings',
                'antivirus_update_now',
                'antivirus_get_details']

    def antivirus_is_enabled(self, provider):
        """Return antivirus feature state

        *Parameters:*
        - `provider`: name of antivirus provider. Either Sophos
        or McAfee

        *Exceptions:*
        - `ValueError`: if unknown provider name is passed

        *Return:*
        True if antivirus feature is enabled or False otherwise

        *Examples:*
        | ${sophos_state}= | Antivirus Is Enabled | Sophos |
        """
        SOPHOS_PAGE_PATH = ('Security Services', 'Sophos')
        MCAFEE_PAGE_PATH = ('Security Services', 'McAfee')

        if provider.lower() == 'sophos':
            PAGE_PATH = SOPHOS_PAGE_PATH
        elif provider.lower() == 'mcafee':
            PAGE_PATH = MCAFEE_PAGE_PATH
        else:
            raise ValueError('Unknown provider name is passed: "%s"' % \
                             (provider,))
        self._debug('Opening "%s" page' % (' -> '.join(PAGE_PATH),))
        self._navigate_to(*PAGE_PATH)

        DISABLED_MARK = 'is currently disabled globally.'
        return not self._is_text_present(DISABLED_MARK)

    @check_antivirus_feature(False)
    def antivirus_enable(self, provider):
        """Enable antivirus feature.
        Ignore state when featuer is already enabled.

        *Parameters:*
        - `provider`: name of antivirus provider to be enabled.
        Either Sophos or McAfee

        *Examples:*
        | Antivirus Enable | McAfee |
        """
        LICENSE_AGREEMENT_MARK = 'License Agreement'

        if self._is_element_present(ENABLE_BUTTON):
            self.click_button(ENABLE_BUTTON)
            if self._is_text_present(LICENSE_AGREEMENT_MARK):
                self.click_button(ACCEPT_LICENCE_BUTTON)
            self._check_action_result()

    @check_antivirus_feature(False)
    def antivirus_disable(self, provider):
        """Disable antivirus feature.
        Ignore state when feature is already enabled.

        *Parameters:*
        - `provider`: name of antivirus provider to be disabled.
        Either Sophos or McAfee

        *Examples:*
        | Antivirus Disable | McAfee |
        """
        if self._is_element_present(EDIT_SETTINGS_BUTTON):
            self.click_button(EDIT_SETTINGS_BUTTON)
            self._unselect_checkbox(ENABLE_CHECKBOX)
            self._click_submit_button()

    @check_antivirus_feature(True)
    def antivirus_update_now(self, provider):
        """Force antivirus update

        *Parameters:*
        - `provider`: name of antivirus provider to be updated.
        Either Sophos or McAfee

        *Exceptions:*
        - `GuiFeatureDisabledError`: if corresponding feature is disabled
        - `ValueError`: if provider name is not correct

        *Return:*
        Result message of update action

        *Examples:*
        | ${msg}= | Antivirus Update Now | McAfee |
        | Log | ${msg} |
        """
        self.click_button(UPDATENOW_BUTTON)
        return self.get_text(ACTION_RESULTS)

    @check_antivirus_feature(True)
    def antivirus_edit_settings(self, provider, scan_timeout=None, enable_auto_update=True):
        """Edit Antivirus settings

        *Parameters:*
        - `provider`: name of antivirus provider to be edited.
        Either Sophos or McAfee
        - `scan_timeout`: virus scanning timeout (seconds)
        - `enable_auto_update`: Enable/Disable automatic updates (boolean value)

        *Exceptions:*
        - `GuiFeatureDisabledError`: if corresponding feature is disabled
        - `ValueError`: if provider name is not correct

        *Examples:*
        | Antivirus Edit Settings | McAfee | 120 |
        | Antivirus Edit Settings | McAfee | 120 | ${True} |
        """
        if self._is_element_present(EDIT_SETTINGS_BUTTON):
            self.click_button(EDIT_SETTINGS_BUTTON)
            if scan_timeout:
                self.input_text(TIMEOUT_EDIT, scan_timeout)
            if enable_auto_update is True:
                self._select_checkbox(AUTO_UPDATE_CHECKBOX)
            elif enable_auto_update is False:
                self._unselect_checkbox(AUTO_UPDATE_CHECKBOX)
            self._click_submit_button()

    @check_antivirus_feature(True)
    def antivirus_get_details(self, provider):
        """Return particular antivirus provider details

        *Parameters:*
        - `provider`: name of antivirus provider which details will be returned.
        Either Sophos or McAfee

        *Exceptions:*
        - `GuiFeatureDisabledError`: if corresponding feature is disabled
        - `ValueError`: if provider name is not correct

        *Return:*
        Dictionary which items are:
        | `Virus Scanning Timeout` | virus scanning timeout (in seconds) |
        | `AntiVirus Files` | <list of antivirus files> |
        each list item is dictionary and has the next format:
        | `File Type` | <name of item> |
        | `Last Update` | <timestamp of last update> |
        | `Current Version` | <current item's version> |

        *Examples:*
        | ${details}= | Antivirus Get Details | McAfee |
        | ${timeout}= | Get From Dictionary | ${details} | Virus Scanning Timeout |
        | Log | ${timeout} |
        | @{files}= | Get From Dictionary | ${details} | AntiVirus Files |
        | Log Many | @{files} |
        """
        INFO_TABLE = "//table[@class='cols']"
        STATUS_INFO_TIMEOUT = "//table[@class='pairs']/tbody/tr[2]/td"
        INFO_TABLE_ROWS = "%s//tr" % (INFO_TABLE,)
        INFO_TABLE_HEADERS_MAP = {'File Type': 1,
                                  'Last Update': 2,
                                  'Current Version': 3}
        INFO_TABLE_CELL = lambda header, row: "%s//tr[%d]/td[%d]" % \
                                              (INFO_TABLE, row, INFO_TABLE_HEADERS_MAP[header])
        STATUS_INFO_AUTO_UPDATE = "//table[@class='pairs']/tbody/tr[3]/td"

        details_dict = {}
        details_dict['Virus Scanning Timeout'] = self.get_text(STATUS_INFO_TIMEOUT)
        details_dict['Automatic Updates'] = self.get_text(STATUS_INFO_AUTO_UPDATE)

        details_dict['AntiVirus Files'] = []
        info_rows_count = int(self.get_matching_xpath_count(INFO_TABLE_ROWS)) - 1
        for row_num in xrange(2, 2 + info_rows_count):
            one_row_dict = {}
            for col_name in INFO_TABLE_HEADERS_MAP.iterkeys():
                one_row_dict[col_name] = self.get_text(INFO_TABLE_CELL(col_name,
                                                                       row_num)).strip()
            details_dict['AntiVirus Files'].append(one_row_dict)
        return details_dict
