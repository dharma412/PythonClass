#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/wsa_amp_verdict_updates.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from sma.constants import sma_web_reports
from report_interface import ReportInfoHolder


class WsaAMPVerdictUpdatesReport(ReportInfoHolder):
    """
    | AMP | 'Advanced Malware Protection Verdict Updates' |

    Chart data values for this web report:
    | N/A |

    Sorting column values for this web reports:
    | N/A |

    """

    def get_name(self):
        return sma_web_reports.AMP_VERDICT_UPDATES

    def get_selector(self):
        return 'wsa_advanced_malware_protection_verdict_updates'

    def get_chart_data(self):
        return None

    def get_table_columns_data(self):
        return None


# module functions
def get_reports():
    return [WsaAMPVerdictUpdatesReport]
