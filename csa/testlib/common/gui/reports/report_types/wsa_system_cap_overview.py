#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_system_cap_overview.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaSystemCapOverviewReport(ReportInfoHolder):
    """
    | SYSTEM_CAP_OVERVIEW | 'System Capacity Overview' |

    Chart data values for this web report:

    System Capacity Overview:
    | N/A |

    Sorting column values for this web reports:

    System Capacity Overview:
    | 'cpu used'                |
    | 'response time'           |
    | 'proxy buffer memory'     |
    | 'transactions per sec'    |
    | 'connection out'          |
    | 'bw out'                  |

    """

    avg_usage_and_performance_col_types = \
        {'cpu used': 'CPU Usage %',
         'response time': 'Response Time (ms)',
         'proxy buffer memory': 'Proxy Buffer Memory (Bytes)',
         'transactions per sec': 'Transactions Per Second',
         'connection out': 'Connections Out',
         'bw out': 'Bandwidth Out (Bytes Per Second)'
         }

    def get_name(self):
        return sma_web_reports.SYSTEM_CAP_OVERVIEW

    def get_selector(self):
        return 'wsa_sma_system_capacity'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        select_name = 'sort_columns[wsa_sma_system_capacity_sma_system_capacity]'
        values_map = {}
        for key, val in self.avg_usage_and_performance_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table = (select_name, values_map)
        return [table]


# module functions
def get_reports():
    return [WsaSystemCapOverviewReport]
