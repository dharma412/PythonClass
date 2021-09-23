#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_app_visibility.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaAppVisibilityReport(ReportInfoHolder):
    """
    | APP_VISIBILITY | 'Application Visibility' |

    Chart data values for this web report:

    Application Visibility:
    | Top Application Types | Top Applications      |
    | `bw used`             | `bw used`             |
    | `completed`           | `completed`           |
    | `limited`             | `limited`             |
    | `not limited`         | `not limited`         |
    | `blocked`             | `blocked`             |
    | `avc blocked`         | `avc blocked`         |
    | `transactions total`  | `transactions total`  |

    Sorting column values for this web reports:

    Application Visibility:
    | 'bw used'     |
    | 'completed'   |
    | 'blocked'     |
    | 'total'       |

    """

    _available_avc_chart_types = \
        {'bw used': 'WEB_APPLICATION_TYPE_DETAIL.BANDWIDTH_USED',
         'completed': 'WEB_APPLICATION_TYPE_DETAIL.COMPLETED_TRANSACTION_TOTAL',
         'limited': 'WEB_APPLICATION_TYPE_DETAIL.BW_LIMITED',
         'not limited': 'WEB_APPLICATION_TYPE_DETAIL.BW_NOT_LIMITED',
         'blocked': 'WEB_APPLICATION_TYPE_DETAIL.BLOCKED_TRANSACTION_TOTAL',
         'avc blocked': 'WEB_APPLICATION_TYPE_DETAIL.BLOCKED_BY_AVC',
         'transactions total': 'WEB_APPLICATION_TYPE_DETAIL.TRANSACTION_TOTAL'
         }

    _available_avc_name_chart_types = \
        {'bw used': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL.BANDWIDTH_USED',
         'completed': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL' + \
             '.COMPLETED_TRANSACTION_TOTAL',
         'limited': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL.BW_LIMITED',
         'not limited': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL.BW_NOT_LIMITED',
         'blocked': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL' + \
             '.BLOCKED_TRANSACTION_TOTAL',
         'avc blocked': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL.BLOCKED_BY_AVC',
         'transactions total': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL.TRANSACTION_TOTAL'
         }

    avc_col_types = \
        {'bw used': 'Bandwidth Used',
         'completed': 'Transactions Completed',
         'blocked': 'Transactions Blocked by Application',
         'total': 'Total Transactions'
         }

    def get_name(self):
        return sma_web_reports.APP_VISIBILITY

    def get_selector(self):
        return 'wsa_applications'

    def get_chart_data(self):
        return [self._available_avc_chart_types,
                self._available_avc_name_chart_types]

    def get_table_columns_data(self):
        select_name = 'sort_columns[wsa_applications_types_total]'
        values_map = {}
        for key, val in self.avc_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table = (select_name, values_map)

        select_name = 'sort_columns[wsa_applications_total]'
        values_map = {}
        for key, val in self.avc_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table2 = (select_name, values_map)

        return [table, table2]


# module functions
def get_reports():
    return [WsaAppVisibilityReport]
