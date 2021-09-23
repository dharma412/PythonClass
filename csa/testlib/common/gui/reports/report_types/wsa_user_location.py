#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_user_location.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaUserLocationReport(ReportInfoHolder):
    """
    | USER_LOCATION | 'Reports by User Location' |

    Chart data values for this web report:

    Reports By User Location:
    | N/A |

    Sorting column values for this web reports:

    Reports By User Location:
    | N/A |

    """

    def get_name(self):
        return sma_web_reports.USER_LOCATION

    def get_selector(self):
        return 'wsa_mus_scheduled'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        return None


# module functions
def get_reports():
    return [WsaUserLocationReport]
