#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_url_cat.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaUrlCatReport(ReportInfoHolder):
    """
    | URL_CAT | 'URL Categories' |

    Chart data values for this web report:

    Url Categories:
    | Top URL Categories    | Top URL Categories    |
    | `bw used`             | `bw used`             |
    | `bw saved`            | `bw saved`            |
    | `time spent`          | `time spent`          |
    | `webcat allowed`      | `webcat allowed`      |
    | `webcat warned`       | `webcat warned`       |
    | `webcat blocked`      | `webcat blocked`      |
    | `total completed`     | `total completed`     |
    | `total blocked`       | `total blocked`       |
    | `transactions total`  | `transactions total`  |
    | `blocked and warned`  | `blocked and warned`  |

    Sorting column values for this web reports:

    Url Categories:
    | 'bw used'             |
    | 'time spent'          |
    | 'total completed'     |
    | 'total blocked'       |
    | 'transactions total'  |

    """

    _available_webcat_chart_types = \
        {'bw used': 'WEB_WEBCAT_DETAIL.BANDWIDTH_USED',
         'bw saved': 'BANDWIDTH_SAVED',
         'time spent': 'WEB_WEBCAT_DETAIL.TIME_SPENT',
         'webcat allowed': 'WEB_WEBCAT_DETAIL.ALLOWED_BY_WEBCAT',
         'webcat warned': 'WEB_WEBCAT_DETAIL.WARNED_BY_WEBCAT',
         'webcat blocked': 'WEB_WEBCAT_DETAIL.BLOCKED_BY_WEBCAT',
         'total completed': 'WEB_WEBCAT_DETAIL.COMPLETED_TRANSACTION_TOTAL',
         'total blocked': 'WEB_WEBCAT_DETAIL.BLOCKED_TRANSACTION_TOTAL',
         'transactions total': 'WEB_WEBCAT_DETAIL.TRANSACTION_TOTAL',
         'blocked and warned': 'WEB_WEBCAT_DETAIL.WARNED_BY_WEBCAT' + \
                               ',WEB_WEBCAT_DETAIL.BLOCKED_BY_WEBCAT'
         }

    typical_col_types = \
        {'bw used': 'Bandwidth Used',
         'time spent': 'Time Spent',
         'total completed': 'Transactions Completed',
         'total blocked': 'Transactions Blocked',
         'transactions total': 'Total Transactions'
         }

    def get_name(self):
        return sma_web_reports.URL_CAT

    def get_selector(self):
        return 'wsa_url_categories'

    def get_chart_data(self):
        # 2 identical charts
        return [self._available_webcat_chart_types,
                self._available_webcat_chart_types]

    def get_table_columns_data(self):
        select_name = 'sort_columns[wsa_url_categories_top_categories]'
        values_map = {}
        for key, val in self.typical_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table = (select_name, values_map)
        return [table]


# module functions
def get_reports():
    return [WsaUrlCatReport]
