#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_web_sites.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaWebSitesReport(ReportInfoHolder):
    """
    | WEB_SITES | 'Web Sites' |

    Chart data values for this web report:

    Web Sites:
    | Top Domains           | Top Domains           |
    | `bw used`             | `bw used`             |
    | `bw saved`            | `bw saved`            |
    | `time spent`          | `time spent`          |
    | `webcat blocked`      | `webcat blocked`      |
    | `app blocked`         | `app blocked`         |
    | `wbrs blocked`        | `wbrs blocked`        |
    | `amv blocked`         | `amv blocked`         |
    | `other blocked`       | `other blocked`       |
    | `total completed`     | `total completed`     |
    | `total blocked`       | `total blocked`       |
    | `transactions total`  | `transactions total`  |

    Sorting column values for this web reports:

    Web Sites:
    | 'bw used'             |
    | 'time spent'          |
    | 'total completed'     |
    | 'total blocked'       |
    | 'transactions total'  |

    """

    _available_domain_chart_types = \
        {'bw used': 'DOMAINS.BANDWIDTH_USED',
         'bw saved': 'BANDWIDTH_SAVED_BY_BLOCKING',
         'time spent': 'DOMAINS.TIME_SPENT',
         'webcat blocked': 'DOMAINS.BLOCKED_BY_WEBCAT',
         'app blocked': 'DOMAINS.BLOCKED_BY_AVC',
         'wbrs blocked': 'DOMAINS.BLOCKED_BY_WBRS',
         'amv blocked': 'DOMAINS.BLOCKED_BY_AMW',
         'other blocked': 'DOMAINS.OTHER_BLOCKED',
         'total completed': 'DOMAINS.COMPLETED_TRANSACTION_TOTAL',
         'total blocked': 'DOMAINS.BLOCKED_TRANSACTION_TOTAL',
         'transactions total': 'DOMAINS.TRANSACTION_TOTAL'
         }

    typical_col_types = \
        {'bw used': 'Bandwidth Used',
         'time spent': 'Time Spent',
         'total completed': 'Transactions Completed',
         'total blocked': 'Transactions Blocked',
         'transactions total': 'Total Transactions'
         }

    def get_name(self):
        return sma_web_reports.WEB_SITES

    def get_selector(self):
        return 'wsa_web_sites'

    def get_chart_data(self):
        # 2 identical charts
        return [self._available_domain_chart_types, self._available_domain_chart_types]

    def get_table_columns_data(self):
        select_name = 'sort_columns[wsa_web_sites_domains_matched]'
        values_map = {}
        for key, val in self.typical_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table = (select_name, values_map)
        return [table]


# module functions
def get_reports():
    return [WsaWebSitesReport]
