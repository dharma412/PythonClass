#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/esa_int_users.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_email_reports
from report_interface import ReportInfoHolder


class EsaIntUsersMailReport(ReportInfoHolder):
    """
    | INT_USERS | 'Internal Users Summary' |

    Sorting column values for this email reports:

    Internal Users Summary:
    | N/A |

    """

    def get_name(self):
        return sma_email_reports.INT_USERS

    def get_selector(self):
        return 'value=mga_incoming_mail_scheduled'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        return None


# module functions
def get_reports():
    return [EsaIntUsersMailReport]
