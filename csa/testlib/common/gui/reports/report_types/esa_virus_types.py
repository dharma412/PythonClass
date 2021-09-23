#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/esa_virus_types.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_email_reports
from report_interface import ReportInfoHolder


class EsaVirusTypesReport(ReportInfoHolder):
    """
    | VIRUS_TYPES | 'Virus Types' |

    Sorting column values for this email reports:

    Virus Types:
    | 'incoming'        |
    | 'outgoing'        |
    | 'total infected'  |

    """

    virus_types_detail_col_types = \
        {'incoming': 'Incoming Messages',
         'outgoing': 'Outgoing Messages',
         'total infected': 'Total Infected Messages'
         }

    def get_name(self):
        return sma_email_reports.VIRUS_TYPES

    def get_selector(self):
        return 'value=mga_virus_types'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        select_name = 'sort_columns[mga_virus_types_virus_types_detail]'
        values_map = {}
        for key, val in self.virus_types_detail_col_types.iteritems():
            values_map[key] = 'label=%s' % (val,)
        table = (select_name, values_map)
        return [table]


# module functions
def get_reports():
    return [EsaVirusTypesReport]
