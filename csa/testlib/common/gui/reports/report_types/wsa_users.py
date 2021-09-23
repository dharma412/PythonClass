#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_users.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaUsersReport(ReportInfoHolder):
    """
    | USERS | 'Users' |

    Chart data values for this web report:

    Users:
    | Top Users (Left)      | Top Users (Right)     |
    | `bw used`             | `bw used`             |
    | `bw saved`            | `bw saved`            |
    | `time spent`          | `time spent`          |
    | `webcat blocked`      | `webcat blocked`      |
    | `app blocked`         | `app blocked`         |
    | `wbrs blocked`        | `wbrs blocked`        |
    | `amv blocked`         | `amv blocked`         |
    | `other blocked`       | `other blocked`       |
    | `total warned`        | `total warned`        |
    | `total completed`     | `total completed`     |
    | `total blocked`       | `total blocked`       |
    | `transactions total`  | `transactions total`  |

    Sorting column values for this web reports:

    Users:
    | 'bw used'             |
    | 'time spent'          |
    | 'total completed'     |
    | 'total blocked'       |
    | 'transactions total'  |

    """

    _available_user_chart_types = \
        {'bw used': 'WEB_USER_DETAIL.BANDWIDTH_USED',
         'bw saved': 'BANDWIDTH_SAVED',
         'time spent': 'WEB_USER_DETAIL.TIME_SPENT',
         'webcat blocked': 'WEB_USER_DETAIL.BLOCKED_BY_WEBCAT',
         'app blocked': 'WEB_USER_DETAIL.BLOCKED_BY_APPLICATION',
         'wbrs blocked': 'WEB_USER_DETAIL.BLOCKED_BY_WBRS',
         'amv blocked': 'WEB_USER_DETAIL.BLOCKED_MALWARE',
         'other blocked': 'WEB_USER_DETAIL.BLOCKED_BY_ADMIN_POLICY',
         'total warned': 'WEB_USER_DETAIL.WARNED_TOTAL',
         'total completed': 'WEB_USER_DETAIL.COMPLETED_TRANSACTION_TOTAL',
         'total blocked': 'WEB_USER_DETAIL.BLOCKED_TRANSACTION_TOTAL',
         'transactions total': 'WEB_USER_DETAIL.TRANSACTION_TOTAL'
         }

    typical_col_types = \
        {'bw used': 'Bandwidth Used',
         'time spent': 'Time Spent',
         'total completed': 'Transactions Completed',
         'total blocked': 'Transactions Blocked',
         'transactions total': 'Total Transactions'
         }

    def get_name(self):
        return sma_web_reports.USERS

    def get_selector(self):
        return 'wsa_users'

    def get_chart_data(self):
        # 2 identical charts
        return [self._available_user_chart_types,
                self._available_user_chart_types]

    def get_table_columns_data(self):
        select_name = 'sort_columns[wsa_users_users_table]'
        values_map = {}
        for key, val in self.typical_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table = (select_name, values_map)
        return [table]


# module functions
def get_reports():
    return [WsaUsersReport]
