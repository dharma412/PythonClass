#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/new_reports_base.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import os
import re
import time
from datetime import date, timedelta, datetime
from time import localtime

from sma.constants import sma_email_reports
from sma.constants import sma_web_reports
from common.gui.guicommon import GuiCommon

from reports.report_check_error import ReportCheckError
from reports.archived_report_info import ArchivedReportInfo
from reports.scheduled_report_info import ScheduledReportInfo
from reports.report_setup import ReportSetup
from reports.report_check import ReportCheck

import common.gui.guiexceptions as guiexceptions


class ReportsBase(ReportSetup, ReportCheck):
    """New Reports Base - refactored class for support report manipulation.

    1. What was changed

        -   2 robot keywords were moved outside the class
            Now these keywords are defined in
            testlib/common/gui/firefox_autodownload.py and
            testlib/common/gui/wait_for_download.py
        -   3 classes that were defined in reports_base moved to reports folder:
            testlib/common/gui/reports/archived_report_info.py
            testlib/common/gui/reports/scheduled_report_info.py
            testlib/common/gui/reports/report_check_error.py
        -   main ReportsBase class was splitted into 2 separated classes
            ReportSetup - methods related to report setup and
            ReportCheck - methods used for getting data and verification
        -   all reports types were converted to modules and placed into
            testlib/common/gui/reports/report_types
        -   ReportSetup methods were updated to work with modular reports
        -   some new register methods were added to ReportSetup

    2. How to use

        New ReportBase provides exactly the same interface as old ReportBase
        by importing all the code and provides facade. Class name is also the same.
        Only thing that should be changed is to import class from another file

        Before:
                from common.gui.reports_base import ReportsBase
        After:
                from common.gui.new_reports_base import ReportsBase

        Before:
                from common.gui.reports_base import ArchivedReportInfo
        After:
                from common.gui.new_reports_base import ArchivedReportInfo
            (can also be:
             from common.gui.reports.archived_report_info import ArchivedReportInfo)

    3. How to extend

        New ReportBase uses modular aproach for reports.
        It allows to easily extend reporting class with new reports.

        Simple scenario:
        We have new report type in zeus80. This report type is already implemented and
        report type is placed in location for common reports
        testlib/common/gui/reports/report_types/wsa_socks_proxy.py

        So we need to import ReportBase

            from common.gui.new_reports_base import ReportsBase

        and change standard_reports_names with new report type by appending
        string with file name (without path and .py extension)

            class ReportsBaseZeus80(ReportsBase):
                "Extends ReportsBase with SOCKS report functionality"

                standard_reports_names = list(ReportsBase.standard_reports_names)
                standard_reports_names.append('wsa_socks_proxy')

        And that's all.


        More complex scenario:
        We have some report that is specific to some product branch.
        We create report module (see chapter "4. How to create new report type")
        and place it for example to
        testlib/zeus80/gui/reporting/my_custom_report.py

        Now we need to import base

            from common.gui.new_reports_base import ReportsBase

        and redefine _register_additional_reports()

            class ReportsBaseCustomZeus80(ReportsBase):
                "Extends ReportsBase with some custom report functionality"

                def _register_additional_reports(self):
                    from custom_report import MyCustomReport
                    report = MyCustomReport()
                    self._register_report(report)

    4. How to create new report type

        Basically report type file is a python module that contain one report
        (or more - but it is not recomended)

        Report class should implement very simple interface defined in
        report_types/report_interface.py

        For common report type it is required to define function
        that returns list of classess contained in module

            # module functions
            def get_reports():
                return [WsaSystemCapOverviewReport]


    5. Features / implementation details

        -   lazy loading is implemented so reports will be imported only at first use.
            Seems to be more efficient at initialization and also more memory frienly

        -   MyWebReport report have some specific requirement like unknown count
            of charts and sort columns. To work properly in this situation some
            additional methods were added to ReportSetup class. They are
            _select_chart_display_data_by_dict() and _select_sort_column_by_dict().
            ReportSetup will recognize if parameter for chart_data and sort_col is
            string or dict and choose the proper private method

    6. TODO



    """
    pass
