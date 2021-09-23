#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_socks_proxy.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaSocksProxyReport(ReportInfoHolder):
    """
    | SOCKS_PROXY | 'SOCKS Proxy' |

    Chart data values for this web report:

    SOCKS Proxy:
    | Top Destinations for SOCKS    | Top Users for SOCKS   |
    | `bw used`                     | `bw used`             |
    | `total allowed`               | `total allowed`       |
    | `total blocked`               | `total blocked`       |
    | `transactions total`          | `transactions total`  |

    Sorting column values for this web reports:

    SOCKS - Destinations:
    | 'domain'              |
    | 'tcp udp'             |
    | 'bw used'             |
    | 'total allowed'       |
    | 'total blocked'       |
    | 'transactions total'  |

    SOCKS - Users:
    | 'bw used'             |
    | 'total allowed'       |
    | 'total blocked'       |
    | 'transactions total'  |

    """

    _available_socks_by_destination_chart = \
        {'bw used': 'WEB_SOCKS_DESTINATIONS.BANDWIDTH_USED',
         'total allowed': 'WEB_SOCKS_DESTINATIONS.ALLOWED_TRANSACTION_TOTAL',
         'total blocked': 'WEB_SOCKS_DESTINATIONS.BLOCKED_TRANSACTION_TOTAL',
         'transactions total': 'WEB_SOCKS_DESTINATIONS.TRANSACTION_TOTAL'
         }

    _available_socks_by_user_chart = \
        {'bw used': 'WEB_SOCKS_USERS.BANDWIDTH_USED',
         'total allowed': 'WEB_SOCKS_USERS.ALLOWED_TRANSACTION_TOTAL',
         'total blocked': 'WEB_SOCKS_USERS.BLOCKED_TRANSACTION_TOTAL',
         'transactions total': 'WEB_SOCKS_USERS.TRANSACTION_TOTAL'
         }

    socks_destination_col_types = \
        {'tcp udp': 'TCP / UDP',
         'bw used': 'Bandwidth Used',
         'total allowed': 'Transactions Allowed',
         'total blocked': 'Transactions Blocked',
         'transactions total': 'Total Transactions'
         }

    socks_users_col_types = \
        {'bw used': 'Bandwidth Used',
         'total allowed': 'Transactions Allowed',
         'total blocked': 'Transactions Blocked',
         'transactions total': 'Total Transactions'
         }

    def get_name(self):
        return sma_web_reports.SOCKS_PROXY

    def get_selector(self):
        return 'wsa_socks'

    def get_chart_data(self):
        return [self._available_socks_by_destination_chart,
                self._available_socks_by_user_chart]

    def get_table_columns_data(self):
        select_name = 'sort_columns[wsa_socks_socks_destinations_table]'
        values_map = {}
        for key, val in self.socks_destination_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table = (select_name, values_map)

        select_name = 'sort_columns[wsa_socks_socks_users_table]'
        values_map = {}
        for key, val in self.socks_users_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table2 = (select_name, values_map)

        return [table, table2]


# module functions
def get_reports():
    return [WsaSocksProxyReport]
