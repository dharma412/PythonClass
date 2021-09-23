#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_my_reports.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaMyReportsReport(ReportInfoHolder):
    """
    | MY_REPORTS | 'My Reports' |

    Chart data values for this web report:

    - depends on configured blocks

    Sorting column values for this web reports:

    - depends on configured blocks

    """

    def get_name(self):
        return sma_web_reports.MY_DASHBOARD

    def get_selector(self):
        return 'My Web Reports'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        return None


# module functions
def get_reports():
    return [WsaMyReportsReport]
