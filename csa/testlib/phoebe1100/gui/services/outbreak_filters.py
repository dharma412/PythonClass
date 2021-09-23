#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/services/outbreak_filters.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import go_to_page, set_speed
from common.gui.guicommon import GuiCommon
import common.gui.guiexceptions as guiexceptions

ENABLE = "//input[@name='action:Enable']"
ENABLE_CHECKBOX = "//input[@id='vof_enabled']"
ACCEPT_LICENCE = "//input[@name='action:AcceptLicense']"
EDIT_SETTINGS = "//input[@name='action:Edit']"
UPDATENOW_BUTTON = "//input[@value='Update Rules Now']"
CLEAR_BUTTON = "//input[@value='Clear Current Rules']"
ACTION_RESULTS = "//*[@id='action-results-message']"
SETTINGS_TABLE = "//table[@class='pairs s50-50']"
INFO_TABLE = "//table[@class='cols']"

PAGE_PATH = ('Security Services', 'Outbreak Filters')


class OutbreakFilters(GuiCommon):
    """Keywords for interaction with
    ESA GUI Security Services -> Outbreak Filters page
    """

    def get_keyword_names(self):
        return ['outbreak_filters_is_enabled',
                'outbreak_filters_update_now',
                'outbreak_filters_enable',
                'outbreak_filters_disable',
                'outbreak_filters_clear_rules',
                'outbreak_filters_edit_settings',
                'outbreak_filters_get_details']

    @go_to_page(PAGE_PATH)
    @set_speed(0)
    def outbreak_filters_is_enabled(self):
        """Get current outbreak filters status

        *Return*
        True or False: whether OF are enabled or disabled

        *Examples:*
        | ${status}= | Outbreak Filters Is Enabled |
        """
        DISABLED_MARK = 'Outbreak Filters are currently disabled globally'
        return (not self._is_text_present(DISABLED_MARK))

    def outbreak_filters_enable(self):
        """Enable outbreak filters feature.
        Does nothing if feature is already enabled.

        *Examples:*
        | Outbreak Filters Enable |
        """
        LICENSE_AGREEMENT_MARK = 'License Agreement'
        if self.outbreak_filters_is_enabled():
            return
        self.click_button(ENABLE)
        if self._is_text_present(LICENSE_AGREEMENT_MARK):
            self.click_button(ACCEPT_LICENCE)

    def outbreak_filters_disable(self):
        """Disable outbreak filters feature.
        Does nothing if feature is already disabled.

        *Examples:*
        | Outbreak Filters Disable |
        """
        if self.outbreak_filters_is_enabled():
            self.click_button(EDIT_SETTINGS)
            self._unselect_checkbox(ENABLE_CHECKBOX)
            self._click_submit_button()

    def outbreak_filters_update_now(self):
        """Initiate manual OF update

        *Exceptions:*
        - `GuiFeatureDisabledError`: if OF feature is disabled

        *Return:*
        Update resulting message

        *Examples:*
        | ${msg}= | Outbreak Filters Update Now |
        """
        if not self.outbreak_filters_is_enabled():
            raise guiexceptions.GuiFeatureDisabledError('Outbreak Filters feature' \
                                                        'is disabled')
        self.click_button(UPDATENOW_BUTTON)
        return self.get_text(ACTION_RESULTS)

    def outbreak_filters_clear_rules(self):
        """Clear current OF rules

        *Exceptions:*
        - `GuiFeatureDisabledError`: if OF feature is not enabled
        - `ConfigError`: if there are no rules configured

        *Return:*
        Clear rules resulting message

        *Examples:*
        | ${msg}= | Outbreak Filters Clear Rules |
        """
        if not self.outbreak_filters_is_enabled():
            raise guiexceptions.GuiFeatureDisabledError('Outbreak Filters feature' \
                                                        'is disabled')
        if not self._is_element_present(CLEAR_BUTTON):
            raise guiexceptions.ConfigError('There are no rules' \
                                            ' available for clean')
        self.click_button(CLEAR_BUTTON, 'don\'t wait')
        self._click_continue_button()
        return self.get_text(ACTION_RESULTS)

    def outbreak_filters_edit_settings(self,
                                       enable_adaptive_rules=None,
                                       scan_size=None,
                                       mail_alerts=None,
                                       url_click_tracking=None):
        """Edit Outbreak Filters settings

        *Parameters:*
        - `enable_adaptive_rules`: whether to enable or disable Adaptive Rules.
        ${True} or ${False}
        - `max_mesg_size`: maximum Message Size to Scan (in bytes).
        You can add a trailing K or M to indicate unit
        - `recv_alerts` : whether you want to receive email alerts. ${True} to
        enable and ${False} to disable
        - `url_click_tracking` : whether you want to  Enable URL Click Tracking. ${True} to
        enable and ${False} to disable

        *Exceptions:*
        - `GuiFeatureDisabledError`: if OF feature is not enabled

        *Examples:*
        | Outbreak Filters Edit Settings | ${True} | 100K | ${False} | ${True} |
        """
        ADAPTIVE_RULES_CHECKBOX = "//input[@id='vof_use_heuristics']"
        MSG_SIZE_TEXT = "//input[@id='vof_max_msg_size']"
        MAIL_ALERT_CHECKBOX = "//input[@id='vof_change_alert']"
        URL_CLICK_TRACKING_CHECKBOX = "//input[@id='vof_urlclicktrack']"

        if not self.outbreak_filters_is_enabled():
            raise guiexceptions.GuiFeatureDisabledError('Outbreak Filters feature' \
                                                        'is disabled')
        self.click_button(EDIT_SETTINGS)
        if enable_adaptive_rules is not None:
            if enable_adaptive_rules:
                self._select_checkbox(ADAPTIVE_RULES_CHECKBOX)
            else:
                self._unselect_checkbox(ADAPTIVE_RULES_CHECKBOX)
        if scan_size:
            self.input_text(MSG_SIZE_TEXT, scan_size)
        if mail_alerts is not None:
            if mail_alerts:
                self._select_checkbox(MAIL_ALERT_CHECKBOX)
            else:
                self._unselect_checkbox(MAIL_ALERT_CHECKBOX)
        if url_click_tracking is not None:
            if url_click_tracking:
                self._select_checkbox(URL_CLICK_TRACKING_CHECKBOX)
            else:
                self._unselect_checkbox(URL_CLICK_TRACKING_CHECKBOX)
        self._click_submit_button()

    def outbreak_filters_get_details(self):
        """Collect information related to Outbreak Filters

        *Exceptions:*
        - `GuiFeatureDisabledError`: if OF feature is not enabled

        *Return:*
        Dictionary which keys are:

        | *Settings* | <value> |
        value is dictionary whose items are:
        | Global Status | <OF status text (Enabled/Disabled)> |
        | Adaptive Rules | <adaptive rules status (Enabled/Disabled)> |
        | Maximum Message Size to Scan | <maximum message size set in settings> |
        | Receive Emailed Alerts | <whether to receive email alerts (Yes/No)> |
        | URL Click Tracking | <Url Click Tracking status (Enabled/Disabled)> |

        | *Rules Updates* | <value> |
        value is list of dictionaries. Each dictionary has the next structure:
        | Rule Type | <rule type description> |
        | Last Update | <last update timestamp> |
        | Current Version | <version of current databases> |

        | *Threats Level Info* | <value> |
        value is list of dictionaries. Each dictionary has the next structure:
        | Threat Level | <level of the particular threat> |
        | Rule Id | <unique rule identifier> |
        | Rule Description | <rule description> |

        *Examples:*
        | ${details}= | Outbreak Filters Get Details |
        | ${settings}= | Get From Dictionary | ${details} | Settings |
        | Log | ${settings} |
        | ${rules}= | Get From Dictionary | ${details} | Rules Updates |
        | ${rule1}= | Get From List | ${rules} | 0 |
        | Log | ${rule1} |
        """
        if not self.outbreak_filters_is_enabled():
            raise guiexceptions.GuiFeatureDisabledError('Outbreak Filters feature' \
                                                        'is disabled')

        status_info = {}
        status_info['Settings'] = self._get_settings()
        status_info['Rules Updates'] = self._get_rules_updates()
        status_info['Threats Level Info'] = self._get_threat_level_info()
        return status_info

    def _get_settings(self):
        settings = {}
        for row in xrange(1, 6):
            key = self.get_text("%s/tbody/tr[%d]/th" % \
                                (SETTINGS_TABLE, row)).strip()[:-1]
            value = self.get_text("%s/tbody/tr[%d]/td" % \
                                  (SETTINGS_TABLE, row)).strip()
            settings[key] = value
        return settings

    def _get_rules_updates(self):
        rules_updates = []
        RULE_ITEMS = {'Rule Type': 1,
                      'Last Update': 2,
                      'Current Version': 3}
        rows_cnt = int(self.get_matching_xpath_count("%s[1]/tbody/tr" % \
                                                     (INFO_TABLE,)))
        for row in range(3, rows_cnt + 1):
            rule_update = {}
            for key, pos in RULE_ITEMS.iteritems():
                rule_update[key] = self.get_text("%s[1]/tbody/tr[%d]/td[%d]" % \
                                                 (INFO_TABLE, row, pos)).strip()
            rules_updates.append(rule_update)
        return rules_updates

    def _get_threat_level_info(self):
        threat_level_info_list = []
        THREAT_LEVEL_ITEMS = {'Threat Level': 1,
                              'Rule Id': 2,
                              'Rule Description': 3}
        rows_cnt = int(self.get_matching_xpath_count("%s[2]/tbody/tr" % \
                                                     (INFO_TABLE,)))
        for row in range(4, rows_cnt + 1):
            threat_level_info = {}
            for key, pos in THREAT_LEVEL_ITEMS.iteritems():
                threat_level_info[key] = self.get_text("%s[2]/tbody/tr[%d]/td[%d]" % \
                                                       (INFO_TABLE, row, pos)).strip()
            threat_level_info_list.append(threat_level_info)
        return threat_level_info_list
