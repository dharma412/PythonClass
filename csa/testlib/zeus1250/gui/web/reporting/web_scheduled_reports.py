#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/reporting/web_scheduled_reports.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from reports_base_zeus835 import ReportsBaseZeus835
from common.gui.new_reports_base import ScheduledReportInfo
import common.gui.guiexceptions as guiexceptions

class WebScheduledReports(ReportsBaseZeus835):
    """Web Scheduled Reports page interaction class.

    This class designed to interact with GUI elements of Web -> Reporting ->
    Scheduled Reports page. Use keywords, listed below, to manipulate with
    Web Scheduled Reports.

    For report specific information please see
    http://eng.ironport.com/docs/qa/sarf/smakeyword/common/ReportsBase.html
    """

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['web_scheduled_reports_add_report',
                'web_scheduled_reports_edit_report',
                'web_scheduled_reports_delete_report',
                'web_scheduled_reports_delete_all_reports',
                'web_scheduled_reports_get_reports'
               ]

    def _open_page(self):
        self._navigate_to('Web', 'Reporting', 'Scheduled Reports')

        err_msg = 'The Centralized Web Reporting service is currently disabled'
        if self._is_text_present(err_msg):
            raise guiexceptions.GuiFeatureDisabledError(err_msg)

        err_msg = 'The feature key for this feature has expired or is ' + \
            'unavailable'
        if self._is_text_present(err_msg):
            raise guiexceptions.GuiFeaturekeyMissingError(err_msg)

    def web_scheduled_reports_add_report(self,
                                     report_type,
                                     title=None,
                                     report_format=None,
                                     time_range=None,
                                     schedule=None,
                                     email_to=None,
                                     num_of_rows=None,
                                     chart_data=None,
                                     sort_col=None
                                     ):
        """Add Web Scheduled Report.

        Use this method to add Web Scheduled Report.

        Parameters:
        - `report_type`: type of report to be added. Mandatory.
        - `title`: report title. String. By default used pattern <Report Type>.
        - `report format`: Either _pdf_ or _csv_. Default _pdf_.
        - `time_range`: time range for the data included in the report. String
        with values separated by colon. First value represents time
        interval: _last day_, _last week_, _last month_, _last year_, _num days_
        or _num months_. If _num days_ or _num months_ was chosen, second value
        represents number of days or months in interval, i.e: 'num days:30'.
        - `schedule`: scheduling options. String with values separated by
        colon. First one is schedule period: _daily_, _weekly_, _monthly_.
        Second - hour, i.e: 01,02,...24. Third - minutes: 00, 15, 30, 45. And
        last one, if schedule period is _weekly_, this one represents day of
        week: _Sunday_, _Monday_...
        - `email_to`: string with e-mails. If you do not specify an email
        address, the report is archived only.
        - `num_of_rows`: for _pdf_ format. Number of rows to be included.
        - `chart_data`: specify what data will be displayed on chart. String
        with values, separated by colon. Available values depends on report
        type. For detailed information see 'Reports Base' keyword doc.
        - `sort_col`: string with values separated by colon. Available
        values depends on report type. For detailed information see
        'Reports Base' keyword doc.

        Examples:
        | Web Scheduled Reports Add Report | ${sma_web_reports.USER_LOCATION} |
        | ... | report_format=pdf |
        | ... | time_range=num months:11 |
        | ... | schedule=weekly:03:30:Sunday |
        | ... | email_to=testuser@mail.qa, testuser@test.com |

        | Web Scheduled Reports Add Report | ${sma_web_reports.WEB_SITES} |
        | ... | title=WebSitesReport |
        | ... | report_format=pdf |
        | ... | time_range=last month |
        | ... | schedule=daily:03:30 |
        | ... | email_to=testuser@ironport.com |
        | ... | num_of_rows=20 |
        | ... | chart_data=other blocked:wbrs blocked |
        | ... | sort_col=total completed |
        """

        self._open_page()
        self._click_add_scheduled_report_button()
        self._fill_report_data(report_type, title, report_format, time_range,
                               schedule, email_to, num_of_rows, chart_data,
                               sort_col, None)
        self._click_submit_button()

    def web_scheduled_reports_edit_report(self,
                                      title,
                                      new_title=None,
                                      report_format=None,
                                      time_range=None,
                                      schedule=None,
                                      email_to=None,
                                      num_of_rows=None,
                                      chart_data=None,
                                      sort_col=None,
                                      ):
        """Edit Web Scheduled Report.

        Use this method to edit Web Scheduled Report.

        Parameters:
        - `title`: To edit report title. String. Mandatory.
        - `new_title`: New report title.
        - `report format`: Either _pdf_ or _csv_. Default _pdf_.
         - `time_range`: time range for the data included in the report. String
        with values separated by colon. First value represents time
        interval: _last day_, _last week_, _last month_, _last year_, _num days_
        or _num months_. If _num days_ or _num months_ was chosen, second value
        represents number of days or months in interval, i.e: 'num days:30'.
        - `schedule`: scheduling options. String of values separated by
        colon. First one is schedule period: _daily_, _weekly_, _monthly_.
        Second - hour, i.e: 01,02,...24. Third - minutes: 00, 15, 30, 45. And
        last one, used only if schedule period is _weekly_, it represents day
        of week: _Sunday_, _Monday_...
        - `email_to`: string with e-mails. If you do not specify an email
        address, the report is archived only.
        - `num_of_rows`: for _pdf_ format. Number of rows to be included.
        - `chart_data`: specify what data will be displayed on chart. String
        with values, separated by colon. Available values depends on report
        type. For detailed information see 'Reports Base' keyword doc.
        - `sort_col`: string with values separated by colon. Available
        values depends on report type. For detailed information see
        'Reports Base' keyword doc.

        Examples:
        | Web Scheduled Reports Edit Report | L4TrafficMonitorReport |
        | ... | new_title=myEditedL4TrafficMonitorReport |
        | ... | report_format=pdf |
        | ... | time_range=last day |
        | ... | schedule=monthly:01:00 |
        | ... | email_to=testuser@cisco.com |
        | ... | num_of_rows=50 |
        | ... | chart_data=total monitored:total detected |
        | ... | cort_col=total monitored:total blocked:total detected |
        """

        self._open_page()
        self._click_edit_report_link(title)
        self._fill_report_data(None, new_title, report_format, time_range,
                               schedule, email_to, num_of_rows, chart_data,
                               sort_col, None)
        self._click_submit_button()

    def web_scheduled_reports_delete_report(self, name):
        """Delete Web Scheduled Report.

        Use this method to delete Web Scheduled Report.

        Parameters:
        - `name`: title of report to be deleted.

        Examples:
        | Web Scheduled Reports Delete Report | Report1 |
        """

        self._open_page()
        # 2 - number of column with reports names
        # 8 - number of column with checkboxes
        self._check_for_deletion(name, 2, 8)
        self._click_delete_button()

    def web_scheduled_reports_delete_all_reports(self):
        """Delete all Web Scheduled Reports.

        Use this method to delete all Web Scheduled Reports.

        Example:
        | Web Scheduled Reports Delete All Reports |
        """

        self._open_page()
        self._select_all_reports()
        self._click_delete_button()

    def web_scheduled_reports_get_reports(self):
        """Get all configured scheduled reports.

        Return:
            A list of ScheduledReportInfo objects holding information about
            scheduled reports.
            Each object has the following attributes:
            - `report_type`: type of the report.
            - `title`: title of the report.
            - `time_range`: time range for the report data.
            - `delivery`: delivery option of the report.
            - `format`: format of the report.
            - `schedule`: scheduling options of the report.
            - `next_run`: next run date of the report.
            - `tier`: appliances or appliance groups for which the report is
            run. Always 'None' for scheduled reports for Web.

        Example:
        | ${reports} = | Web Scheduled Reports Get Reports |
        """

        self._open_page()
        reports = self._get_reports_info(ScheduledReportInfo, 'web')

        return reports
