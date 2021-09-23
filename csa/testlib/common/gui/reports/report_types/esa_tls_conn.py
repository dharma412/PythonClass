#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/esa_tls_conn.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_email_reports
from report_interface import ReportInfoHolder


class EsaTlsConnReport(ReportInfoHolder):
    """
    | TLS_CONN | 'TLS Connections' |

    Sorting column values for this email reports:

    Tls Connections:
    | 'req. failed'     | 'req. failed'     |
    | 'req. success'    | 'req. success'    |
    | 'pref. failed'    | 'pref. failed'    |
    | 'pref success'    | 'pref success'    |
    | 'total'           | 'total'           |
    | 'unencrypted'     | 'unencrypted'     |
    | 'messages'        | 'messages'        |

    """

    tls_connections_details_col_types = \
        {'req. failed': 'TLS Req. Failed',
         'req. success': 'TLS Req. Success',
         'pref. failed': 'TLS Pref. Failed',
         'pref success': 'TLS Pref. Success',
         'total': 'Total TLS Connections',
         'unencrypted': 'Unencrypted Connections',
         'messages': 'Messages by TLS'
         }

    def get_name(self):
        return sma_email_reports.TLS_CONN

    def get_selector(self):
        return 'value=mga_tls_connections'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        select_name = 'sort_columns[mga_tls_connections_received_tls_detail]'
        values_map = {}
        for key, val in self.tls_connections_details_col_types.iteritems():
            values_map[key] = 'label=%s' % (val,)
        table = (select_name, values_map)

        select_name = 'sort_columns[mga_tls_connections_sent_tls_detail]'
        table2 = (select_name, values_map)

        return [table, table2]


# module functions
def get_reports():
    return [EsaTlsConnReport]
