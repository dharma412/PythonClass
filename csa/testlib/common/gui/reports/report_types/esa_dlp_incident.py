#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/esa_dlp_incident.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_email_reports
from report_interface import ReportInfoHolder


class EsaDlpIncidentReport(ReportInfoHolder):
    """
    | DLP_INCIDENT | 'DLP Incident Summary' |

    Sorting column values for this email reports:

    Dlp Incident Summary:
    | 'low'             |
    | 'medium'          |
    | 'high'            |
    | 'critical'        |
    | 'total'           |
    | 'delivered enc'   |
    | 'delivered clear' |
    | 'dropped'         |

    """

    dlp_col_types = \
        {'low': 'Low',
         'medium': 'Medium',
         'high': 'High',
         'critical': 'Critical',
         'total': 'Total',
         'delivered enc': 'Delivered (encrypted)',
         'delivered clear': 'Delivered (clear)',
         'dropped': 'Dropped'
         }

    def get_name(self):
        return sma_email_reports.DLP_INCIDENT

    def get_selector(self):
        return 'value=mga_dlp_incident_summary'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        select_name = 'sort_columns[mga_dlp_incident_summary_dlp_incident_details]'
        values_map = {}
        for key, val in self.dlp_col_types.iteritems():
            values_map[key] = 'label=%s' % (val,)
        table = (select_name, values_map)
        return [table]


# module functions
def get_reports():
    return [EsaDlpIncidentReport]
