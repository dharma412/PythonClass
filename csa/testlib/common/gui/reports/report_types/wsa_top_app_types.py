#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_top_app_types.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaTopAppTypesReport(ReportInfoHolder):
    """
    | TOP_APP_TYPES | 'Top Application Types - Extended' |

    Chart data values for this web report:

    Top Application Types - Extended:
    | N/A |

    Sorting column values for this web reports:

    Top Application Types - Extended:
    | 'bw used'     |
    | 'completed'   |
    | 'blocked'     |
    | 'total'       |

    """

    app_name_col_types = \
        {'bw used': 'Bandwidth Used',
         'completed': 'Transactions Completed',
         'blocked': 'Transactions Blocked',
         'total': 'Transactions Total'
         }

    def get_name(self):
        return sma_web_reports.TOP_APP_TYPES

    def get_selector(self):
        return 'wsa_top_n_applications'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        select_name = 'sort_columns[wsa_top_n_applications_top_n_0]'
        values_map = {}
        for key, val in self.app_name_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table = (select_name, values_map)
        return [table]


# module functions
def get_reports():
    return [WsaTopAppTypesReport]
