#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_l4tm.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaL4tmReport(ReportInfoHolder):
    """
    | L4TM | 'L4 Traffic Monitor' |

    Chart data values for this web report:

    L4 Traffic Monitor:
    | Top Client IPs    | Top Malware Sites |
    | `total monitored` | `total monitored` |
    | `total blocked`   | `total blocked`   |
    | `total detected`  | `total detected`  |

    Sorting column values for this web reports:

    L4 Traffic Monitor:
    | 'total monitored' |
    | 'total blocked'   |
    | 'total detected'  |

    """

    _available_traffic_monitor_by_user_chart = \
        {'total monitored': 'WEB_USER_BY_TRAFFIC_MONITOR.MONITORED_MALWARE',
         'total blocked': 'WEB_USER_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE',
         'total detected': 'WEB_USER_BY_TRAFFIC_MONITOR.MONITORED_MALWARE' + \
                           ',WEB_USER_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE'
         }

    _available_traffic_monitor_by_host_chart = \
        {'total monitored': 'WEB_HOST_BY_TRAFFIC_MONITOR.MONITORED_MALWARE',
         'total blocked': 'WEB_HOST_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE',
         'total detected': 'WEB_HOST_BY_TRAFFIC_MONITOR.MONITORED_MALWARE' + \
                           ',WEB_HOST_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE'
         }

    l4_mon_col_types = \
        {'total monitored': 'Malware Connections Monitored',
         'total blocked': 'Malware Connections Blocked',
         'total detected': 'Total Malware Connections Detected'
         }

    def get_name(self):
        return sma_web_reports.L4TM

    def get_selector(self):
        return 'wsa_l4_traffic_monitor'

    def get_chart_data(self):
        return [self._available_traffic_monitor_by_user_chart, \
                self._available_traffic_monitor_by_host_chart]

    def get_table_columns_data(self):
        select_name = 'sort_columns[wsa_l4_traffic_monitor_l4_tm_client_ips]'
        values_map = {}
        for key, val in self.l4_mon_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table = (select_name, values_map)

        select_name = 'sort_columns[wsa_l4_traffic_monitor_malware_ports_detected]'
        table2 = (select_name, values_map)

        select_name = 'sort_columns[wsa_l4_traffic_monitor_top_l4_tm_sites]'
        table3 = (select_name, values_map)

        return [table, table2, table3]


# module functions
def get_reports():
    return [WsaL4tmReport]
