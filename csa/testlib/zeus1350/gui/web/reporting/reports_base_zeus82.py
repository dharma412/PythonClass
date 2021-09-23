#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/web/reporting/reports_base_zeus82.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

from sma.constants import sma_web_reports
from common.gui.reports_base import ReportsBase


class ReportsBaseZeus82(ReportsBase):
    """Extends ReportsBase with SOCKS report functionality

    New web report types constants:
    | SOCKS_PROXY | 'SOCKS Proxy' |

    Chart data values for web report types:

    SOCKS Proxy:
    | Top Destinations for SOCKS    | Top Users for SOCKS       |
    | `Bandwidth Used`              | `Bandwidth Used`          |
    | `Transactions Allowed`        | `Transactions Allowed`    |
    | `Transactions Blocked`        | `Transactions Blocked`    |
    | `Total Transactions`          | `Total Transactions`      |


    Sorting column values for web reports:

    SOCKS - Destinations:
    | 'Domain/IP:Port' |
    | 'TCP / UDP' |
    | 'Bandwidth Used' |
    | 'Transactions Allowed' |
    | 'Transactions Blocked' |
    | 'Total Transactions' |

    SOCKS - Users:
    | 'User ID or Client IP' |
    | 'Bandwidth Used' |
    | 'Transactions Allowed' |
    | 'Transactions Blocked' |
    | 'Total Transactions' |

    """

    _available_socks_by_destination_chart = \
        {'Bandwidth Used': 'WEB_SOCKS_DESTINATIONS.BANDWIDTH_USED',
         'Transactions Allowed': 'WEB_SOCKS_DESTINATIONS.ALLOWED_TRANSACTION_TOTAL',
         'Transactions Blocked': 'WEB_SOCKS_DESTINATIONS.BLOCKED_TRANSACTION_TOTAL',
         'Total Transactions': 'WEB_SOCKS_DESTINATIONS.TRANSACTION_TOTAL'
         }

    _available_socks_by_user_chart = \
        {'Bandwidth Used': 'WEB_SOCKS_USERS.BANDWIDTH_USED',
         'Transactions Allowed': 'WEB_SOCKS_USERS.ALLOWED_TRANSACTION_TOTAL',
         'Transactions Blocked': 'WEB_SOCKS_USERS.BLOCKED_TRANSACTION_TOTAL',
         'Total Transactions': 'WEB_SOCKS_USERS.TRANSACTION_TOTAL'
         }

    _report_types = ReportsBase._report_types.copy()
    _report_types.update(
        {sma_web_reports.SOCKS_PROXY: 'wsa_socks'}
    )

    TABLE_COLUMNS_LINK_SELECTOR = "//span[contains(@onclick,'showTableOptionsDlg')]"
    SECTION_EXPORT_LINK_SELECTOR = "//span[contains(@onclick,'SectionExport')]"

    def _get_type_dicts(self, report_type):
        if report_type == sma_web_reports.SOCKS_PROXY:
            return (self._available_socks_by_destination_chart,
                    self._available_socks_by_user_chart)
        return super(ReportsBaseZeus82, self)._get_type_dicts(report_type)

    def _select_sort_column(self, report_type, columns):
        if report_type == sma_web_reports.SOCKS_PROXY:
            socks_col_types = \
                {'bw used': 'Bandwidth Used',
                 'total completed': 'Transactions Completed',
                 'total blocked': 'Transactions Allowed',
                 'transactions total': 'Total Transactions'
                 }
            columns_tuple = \
                self._convert_to_tuple_from_colon_separated_string(columns)
            elements = (
                'sort_columns[wsa_socks_socks_destinations_table]',
                'sort_columns[wsa_socks_socks_users_table]')
            self._select_sort_column_from_list(
                socks_col_types,
                elements[0], columns_tuple[0])
            self._select_sort_column_from_list(
                socks_col_types,
                elements[1], columns_tuple[1])

        super(ReportsBaseZeus82, self)._select_sort_column(report_type, columns)

    def _select_chart_data(self, type, row, type_dict):
        link = "xpath=//table[@class='layout']//tr[%d]//td[2]/a" % (row,)
        if type.lower() == 'none':
            return
        if type not in type_dict.keys():
            raise guiexceptions.ConfigError(
                "Invalid chart data type '%s'." % (type))

        radio_button_link = "xpath=//input[@id='chart_option_dlg_%s']" % \
                            (type_dict[type])
        self.click_element(link, "don't wait")
        self._click_radio_button(radio_button_link)
        self.click_element("xpath=//div[@id='chart_option_dlg']//button[text()='Save']",
                           "don't wait")

    def _find_section_area(self, section_path, timeout=60):
        old_section_loc = super(ReportsBaseZeus82, self)._find_section_area(section_path, timeout)
        if old_section_loc is None:
            return None
        container_locator = old_section_loc + "//ancestor::div[starts-with(@id,'container_')]"
        count = int(self.get_matching_xpath_count(container_locator))
        new_selector = None
        if count == 0:
            self._warn('Report section container was not found. Falling back to old locator')
            return old_section_loc
        if count > 1:
            self._warn('Found more then one report section container. Choosing the closest one')
        id = self.get_element_attribute("xpath=" + container_locator + "[1]@id")
        new_selector = "//*[@id='%s']" % id
        self._debug('Report section selector is %s' % (new_selector,))
        return new_selector
