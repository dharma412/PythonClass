#!/usr/bin/env python
# $Id:
# $DateTime:
# $Author:

from esa.constants import email_reports
from report_interface import ReportInfoHolder

class EsaAPPReport(ReportInfoHolder):
    """
    | APP | 'Advanced Phishing Protection' |

    Sorting column values for this email reports:

    Advanced Phishing Protection
    | 'Message Forwarding Success' |
    | 'Message Forwarding Failure' |
    """

    message_attempt_to_be_forwarded_app_col_types = \
        {'MFS':'Message Forwarding Success',
         'MFF':'Message Forwarding Failure'
        }

    def get_name(self):
        return email_reports.APP

    def get_selector(self):
        return 'value=mga_advanced_phishing_protection'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        select_name = 'sort_columns[mga_advanced_phishing_protection_advanced_phishing_protection_summary_table]'
        values_map = {}
        for key, val in self.message_attempt_to_be_forwarded_app_col_types.iteritems():
            values_map[key] = '%s' % (val,)
        table = (select_name, values_map)
        return [table]

# module functions
def get_reports():
    return [EsaAPPReport]
