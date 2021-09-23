#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/esa_vof.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_email_reports
from report_interface import ReportInfoHolder


class EsaVofReport(ReportInfoHolder):
    """
    | VOF | 'Outbreak Filters' |

    Sorting column values for this email reports:

    Outbreak Filters:
    | 'total'   | 'outbreak'    |
    |           | 'first seen'  |
    |           | 'time'        |
    |           | 'messages'    |

    """

    threat_det_col_types = \
        {'total': 'Total Messages'
         }

    pyvirus_outbreaks_col_types = \
        {'outbreak': 'Outbreak ID',
         'first seen': 'First Seen Globally',
         'time': 'Protection Time',
         'messages': 'Quarantined Messages'
         }

    def get_name(self):
        return sma_email_reports.VOF

    def get_selector(self):
        return 'value=mga_virus_outbreaks_scheduled'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        select_name = 'sort_columns[mga_virus_outbreaks_scheduled_threat_details]'
        values_map = {}
        for key, val in self.threat_det_col_types.iteritems():
            values_map[key] = 'label=%s' % (val,)
        table = (select_name, values_map)

        select_name = 'sort_columns[mga_virus_outbreaks_scheduled_outbreak_details]'
        values_map = {}
        for key, val in self.pyvirus_outbreaks_col_types.iteritems():
            values_map[key] = 'label=%s' % (val,)
        table2 = (select_name, values_map)
        return [table, table2]


# module functions
def get_reports():
    return [EsaVofReport]
