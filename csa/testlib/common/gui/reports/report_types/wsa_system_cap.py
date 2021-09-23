#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_system_cap.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaSystemCapReport(ReportInfoHolder):
    """
    | SYSTEM_CAP | 'Web System Capacity' |

    Chart data values for this web report:

    System Capacity:
    | N/A |

    Sorting column values for this web reports:

    System Capacity:
    | N/A |

    """

    def get_name(self):
        return sma_web_reports.SYSTEM_CAP

    def get_selector(self):
        return 'wsa_sma_system_capacity_detail'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        return None


# module functions
def get_reports():
    return [WsaSystemCapReport]
