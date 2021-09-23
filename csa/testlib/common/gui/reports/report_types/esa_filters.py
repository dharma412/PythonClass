#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/esa_filters.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_email_reports
from report_interface import ReportInfoHolder


class EsaFiltersReport(ReportInfoHolder):
    """
    | FILTERS | 'Content Filters' |


    Sorting column values for this email reports:

    Content Filters:
    | N/A |

    """

    def get_name(self):
        return sma_email_reports.FILTERS

    def get_selector(self):
        return 'value=mga_content_filters'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        return None


# module functions
def get_reports():
    return [EsaFiltersReport]
