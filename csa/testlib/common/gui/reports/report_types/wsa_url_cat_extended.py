#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_url_cat_extended.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaUrlCatExtendedReport(ReportInfoHolder):
    """
    | URL_CAT_EXTENDED | 'Top URL Categories - Extended' |

    Chart data values for this web report:

    Top Url Categories - Extended:
    | N/A |

    Sorting column values for this web reports:

    Top Url Categories - Extended:
    | 'bw used'             |
    | 'time spent'          |
    | 'total completed'     |
    | 'total blocked'       |
    | 'transactions total'  |

    """

    category_name_col_types = \
        {'bw used': 'Bandwidth Used',
         'time spent': 'Time Spent',
         'total completed': 'Transactions Completed',
         'total blocked': 'Transactions Blocked',
         'transactions total': 'Transactions Total'
         }

    # UI Devs put 'Transactions Total' insted of
    # 'Total Transactions' like in all other reports

    def get_name(self):
        return sma_web_reports.URL_CAT_EXTENDED

    def get_selector(self):
        return 'wsa_top_n_categories'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        select_name = 'sort_columns[wsa_top_n_categories_top_n_0]'
        values_map = {}
        for key, val in self.category_name_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table = (select_name, values_map)
        return [table]


# module functions
def get_reports():
    return [WsaUrlCatExtendedReport]
