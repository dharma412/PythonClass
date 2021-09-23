#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/gui/web/reporting/web_archived_reports.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from reports_base_zeus835 import ReportsBaseZeus835
from common.gui.new_reports_base import ArchivedReportInfo

class WebArchivedReports(ReportsBaseZeus835):
    """Web Archived Reports page interaction class.

    This class designed to interact with GUI elements of Web -> Reporting ->
    Archived Reports page. Use keywords, listed below, to manipulate with
    Web Archived Reports.

    For report specific information please see
    http://eng.ironport.com/docs/qa/sarf/smakeyword/common/ReportsBase.html
    """

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['web_archived_reports_add_report',
                'web_archived_reports_delete_report',
                'web_archived_reports_delete_all_reports',
                'web_archived_reports_get_reports'
               ]

    def _open_page(self):
        self._navigate_to('Web', 'Reporting', 'Archived Reports')

        err_msg = 'The feature key for this feature has expired or is ' + \
                'unavailable'
        if self._is_text_present(err_msg):
            raise guiexceptions.GuiFeaturekeyMissingError(err_msg)

    def web_archived_reports_add_report(self,
                                     report_type,
                                     title=None,
                                     report_format=None,
                                     time_range=None,
                                     email_to=None,
                                     archive=None,
                                     num_of_rows=None,
                                     chart_data=None,
                                     sort_col=None
                                     ):
        """Add Web Archived Report.

        Use this method to add Web Archived Report.

        Parameters:
        - `report_type`: type of report to be added. Mandatory.
        - `title`: report title. String. By default used pattern <Report Type>.
        - `report format`: Either _pdf_ or _csv_. Default _pdf_.
        - `time_range`: time range for the data included in the report. String
        with values separated by colon. First value represents time interval:
        _last day_, _last week_, _last month_, _last year_, _num days_,
        _num months_ or _timestamp_. If _timestamp_ was chosen, second values
        represents start date and end date in reported period.
        Date format: dd Mmm yyyy hh
        Example: timestamp:01 Apr 2011 01:24 Apr 2011 20
        If _num days_ or _num months_ was chosen, second value
        represents number of days or months in interval, i.e: 'num days:30'.
        - `archive`: Either 'yes' or 'no' to set archive report or not. 'yes'
        is used as default value.
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

        | Web Archived Reports Add Report | ${sma_web_reports.USERS} |
        | ... | title=UsersReport |
        | ... | report_format=csv |
        | ... | time_range=last day |
        | ... | archive=yes |
        | ... | email_to=testuser@ironport.com |
        | ... | chart_data=bw used:total blocked |
        | ... | sort_col=total completed |

        | Web Archived Reports Add Report | ${sma_web_reports.MALWARE_RISK} |
        | ... | title=ClientMalwareRiskReport |
        | ... | report_format=pdf |
        | ... | time_range=num months:3 |
        | ... | archive=yes |
        | ... | num_of_rows=50 |
        | ... | chart_data=bw saved:total detected |
        | ... | sort_col=total monitored:total detected |
        """

        self._open_page()
        self._click_add_archived_report_button()
        self._fill_archived_report_data(report_type, title, report_format,
                                        time_range, email_to, archive,
                                        num_of_rows, chart_data, sort_col,
                                        None)
        self._click_deliver_button()

    def web_archived_reports_delete_report(self, name):
        """Delete Web Archived Report.

        Use this method to delete Web Archived Report.

        Parameters:
        - `name`: To delete report name.

        Examples:
        | Web Archived Reports Delete Report | Report |
        """

        self._open_page()
        self._show_all()
        # 1 - number of column with reports names
        # 6 - number of column with checkboxes
        self._check_for_deletion(name, 1, 6)
        self._click_delete_button()

    def web_archived_reports_delete_all_reports(self):
        """Delete all Web Archived Reports.

        Use this method to delete all Web Archived Reports.

        Example:
        | Web Archived Reports Delete All Reports |
        """

        self._open_page()
        self._show_all()
        self._select_all_reports()
        self._click_delete_button()

    def web_archived_reports_get_reports(self):
        """Get all archived reports.

        Return:
            A list of ArchivedReportInfo objects holding information about
            archived reports.
            Each object has the following attributes:
            - `report_type`: type of the report.
            - `title`: title of the report.
            - `time_range`: time range for the report data.
            - `format`: format of the report.
            - `generate_date`: date which report was generated on.
            - `tier`: appliances or appliance groups for which the report was
            generated. Always 'None' for archived reports for Web.

        Example:
        | ${reports} = | Web Archived Reports Get Reports |
        """

        self._open_page()
        reports = self._get_reports_info(ArchivedReportInfo, 'web')

        return reports
