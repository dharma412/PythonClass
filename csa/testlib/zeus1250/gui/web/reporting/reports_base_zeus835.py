#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/reporting/reports_base_zeus835.py#4 $
# $DateTime: 2019/12/11 22:27:50 $
# $Author: sarukakk $

from sma.constants import sma_web_reports
from reports_base_zeus82 import ReportsBaseZeus82

class ReportsBaseZeus835(ReportsBaseZeus82):
    """
    Two report types added in addition to zeus82:
    Advanced Malware Protection and
    Advanced Malware Protection Verdict Updates

    """

    standard_reports_names = list(ReportsBaseZeus82.standard_reports_names)
    standard_reports_names.append('wsa_amp')
    standard_reports_names.append('wsa_amp_verdict_updates')
