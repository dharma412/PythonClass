#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_wbrs_filters.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaWbrsFiltersReport(ReportInfoHolder):
    """
    | WBRS_FILTERS | 'Web Reputation Filters' |

    Chart data values for this web report:

    Web Reputation Filters:
    | N/A |

    Sorting column values for this web reports:

    Web Reputation Filters:
    | 'block'               |
    | 'malware detected'    |
    | 'clean'               |
    | 'allow'               |

    """

    wbrs_col_types = \
        {'block': 'Block',
         'malware detected': 'Scan Further: Malware Detected',
         'clean': 'Scan Further: Clean',
         'allow': 'Allow'
         }

    def get_name(self):
        return sma_web_reports.WBRS_FILTERS

    def get_selector(self):
        return 'wsa_web_reputation_filters'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        select_name = 'sort_columns[wsa_web_reputation_filters_wbrs_filters]'
        values_map = {}
        for key, val in self.wbrs_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table = (select_name, values_map)
        return [table]


# module functions
def get_reports():
    return [WsaWbrsFiltersReport]
