#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_amp.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaAMPReport(ReportInfoHolder):
    """
    | AMP | 'Advanced Malware Protection' |

    Chart data values for this web report:
    | Top Malware Threat Files  | Trend         |
    | `monitored`               | `monitored`   |
    | `blocked`                 | `blocked`     |
    | `detected`                | `detected`    |
    | `monitored or detected`   |               |

    Sorting column values for this web reports:

    Malware Threat Files:
    | 'treat name'  |
    | 'file type'   |
    | 'monitored'   |
    | 'blocked'     |
    | 'detected'    |

    """

    _available_amp_treat_files_chart = \
        {'monitored': 'WEB_AMP_DETAIL.TRANSACTIONS_MONITORED',
         'blocked': 'WEB_AMP_DETAIL.TRANSACTIONS_BLOCKED',
         'detected': 'WEB_AMP_DETAIL.TRANSACTIONS_DETECTED',
         'monitored or detected': 'WEB_AMP_DETAIL.TRANSACTIONS_MONITORED' + \
                                  ',WEB_AMP_DETAIL.TRANSACTIONS_BLOCKED'
         }

    _available_amp_trend_chart = \
        {'monitored': 'WEB_AMP_DETAIL_SUMMARY.TRANSACTIONS_MONITORED',
         'blocked': 'WEB_AMP_DETAIL_SUMMARY.TRANSACTIONS_BLOCKED',
         'detected': 'WEB_AMP_DETAIL_SUMMARY.TRANSACTIONS_DETECTED'
         }

    amp_treat_files_col_types = \
        {'treat name': 'WEB_AMP_DETAIL.AMP_MALWARE_NAME',
         'file type': 'WEB_AMP_DETAIL.AMP_CONTENT_TYPE',
         'monitored': 'WEB_AMP_DETAIL.TRANSACTIONS_MONITORED',
         'blocked': 'WEB_AMP_DETAIL.TRANSACTIONS_BLOCKED',
         'detected': '__DEFAULT__'
         }

    def get_name(self):
        return sma_web_reports.AMP

    def get_selector(self):
        return 'wsa_advanced_malware_protection'

    def get_chart_data(self):
        return [self._available_amp_treat_files_chart,
                self._available_amp_trend_chart]

    def get_table_columns_data(self):
        select_name = \
            'sort_columns[wsa_advanced_malware_protection_advanced_malware_protection_threats]'
        values_map = {}
        for key, val in self.amp_treat_files_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table = (select_name, values_map)

        return [table]


# module functions
def get_reports():
    return [WsaAMPReport]
