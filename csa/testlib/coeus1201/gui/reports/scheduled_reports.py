#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/reports/scheduled_reports.py#1 $

from reports_base import ReportsBase
import time

class ScheduledReports(ReportsBase):
    """Scheduled Reports page interaction class.

    This class designed to interact with GUI elements of Reporting ->
    Scheduled Reports page. Use keywords, listed below, to manipulate with
    Scheduled Reports.

    Foe report specific information please see 'Reports Base' keyword document.
    """

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['scheduled_reports_add_report',
                'scheduled_reports_edit_report',
                'scheduled_reports_delete_report',
               ]

    def scheduled_reports_add_report(self,
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
        """Add Scheduled Report.

        Use this method to add Scheduled Report.

        Parameters:
        - `report_type`: type of report to be added. Mandatory.
        - `title`: report title. String. By default used pattern <Report Type>.
        - `report format`: Either _pdf_ or _csv_. Default _pdf_.
        - `time_range`: time range for the data included in the report. String
        with values separated by semicolon. First value represents time
        interval: _last day_, _last week_, _last month_ or _num days_. If
        _num days_ was chosen, second value represents number of days in
        interval, i.e: 'num days:30'.
        - `schedule`: scheduling options. String with values separated by
        semicolon. First one is schedule period: _daily_, _weekly_, _monthly_.
        Second - hour, i.e: 01,02,...24. Third - minutes: 00, 15, 30, 45. And
        last one, if schedule period is _weekly_, this one represents day of
        week: _Sunday_, _Monday_...
        - `email_to`: string with e-mails. If you do not specify an email
        address, the report is archived only.
        - `num_of_rows`: for _pdf_ format. Number of rows to be included.
        - `chart_data`: specify what data will be displayed on chart. String
        with values, separated by semicolon. Available values depends on report
        type. For detailed information see 'Reports Base' keyword doc.
        - `sort_col`: string with values separated by semicolon. Available
        values depends on report type. For detailed information see
        'Reports Base' keyword doc.

        Examples:
        | Scheduled Reports Add Report | overview |
        | ... | title=Report1 |
        | ... | report_format=csv |
        | ... | time_range=last week |
        | ... | schedule=monthly:03:30 |
        | ... | email_to=mkrysiuk@ironport.com |

        | Scheduled Reports Add Report | url categories |
        | ... | title=Report2 |
        | ... | report_format=pdf |
        | ... | time_range=last week |
        | ... | schedule=monthly:03:30 |
        | ... | email_to=mkrysiuk@ironport.com |
        | ... | num_of_rows=20 |
        | ... | chart_data=webcat monitored:webcat blocked |
        | ... | sort_col=time spent |
        """

        self._open_page()
        self.click_button("xpath=//input[@title='Add Scheduled Report...']")

        self._select_report_type(report_type)
        time.sleep(2)

        if title is not None:
            self._fill_report_title(title)

        if chart_data is not None:
            self._select_chart_display_data(report_type, chart_data)

        if sort_col is not None:
            self._select_sort_column(report_type, sort_col)

        if time_range is not None:
            self._select_time_range(time_range)

        if report_format is not None:
            self._select_report_format(report_format)

        if num_of_rows is not None:
            self._select_number_of_rows(num_of_rows)

        if schedule is not None:
            self._select_report_schedule(schedule)

        if email_to is not None:
            self._fill_email_to(email_to)

        self._click_submit_button()

    def scheduled_reports_edit_report(self,
                                      title,
                                      new_title=None,
                                      report_format=None,
                                      time_range=None,
                                      schedule=None,
                                      email_to=None,
                                      num_of_rows=None,
                                      chart_data=None,
                                      sort_col=None
                                      ):
        """Edit Scheduled Report.

        Use this method to edit Scheduled Report.

        Parameters:
        - `title`: To edit report title. String. Mandatory.
        - `new_title`: New report title.
        - `report format`: Either _pdf_ or _csv_. Default _pdf_.
        - `time_range`: time range for the data included in the report. String
        with values separated by semicolon. First value represents time
        interval: _last day_, _last week_, _last month_ or _num days_. If
        _num days_ was chosen, second value represents number of days in
        interval, i.e: 'num days: 30'.
        - `schedule`: scheduling options. String of values separated by
        semicolon. First one is schedule period: _daily_, _weekly_, _monthly_.
        Second - hour, i.e: 01,02,...24. Third - minutes: 00, 15, 30, 45. And
        last one, used only if schedule period is _weekly_, it represents day
        of week: _Sunday_, _Monday_...
        - `email_to`: string with e-mails. If you do not specify an email
        address, the report is archived only.
        - `num_of_rows`: for _pdf_ format. Number of rows to be included.
        - `chart_data`: specify what data will be displayed on chart. String
        with values, separated by semicolon. Available values depends on report
        type. For detailed information see 'Reports Base' keyword doc.
        - `sort_col`: string with values separated by semicolon. Available
        values depends on report type. For detailed information see
        'Reports Base' keyword doc.

        Examples:
        | Scheduled Reports Edit Report | Report10 |
        | ... | new_title=myEditedReport |
        | ... | report_format=pdf |
        | ... | time_range=last day |
        | ... | schedule=monthly:01:00 |
        | ... | email_to=mkrysiuk@cisco.com |
        | ... | num_of_rows=50 |
        | ... | chart_data=wbrs blocked:total warned |
        | ... | cort_col=total blocked |
        """

        self._open_page()
        self._show_all()
        self._click_edit_report_link(title)

        report_type = self._get_report_type()

        if new_title is not None:
            self._fill_report_title(new_title)

        if chart_data is not None:
            self._select_chart_display_data(report_type, chart_data)

        if sort_col is not None:
            self._select_sort_column(report_type, sort_col)

        if time_range is not None:
            self._select_time_range(time_range)

        if report_format is not None:
            self._select_report_format(report_format)

        if num_of_rows is not None:
            self._select_number_of_rows(num_of_rows)

        if schedule is not None:
            self._select_report_schedule(schedule)

        if email_to is not None:
            self._fill_email_to(email_to)

        self._click_submit_button()

    def scheduled_reports_delete_report(self, name):
        """Delete Scheduled Report.

        Use this method to delete Scheduled Report.

        Parameters:
        - `name`: title of report to be deleted.

        Examples:
        | Scheduled Reports Delete Report | Report1 |
        """

        self._open_page()
        self._show_all()
        self._check_for_deletion(name, 2, 8)
        self._click_delete_button()

    def _open_page(self):
        self._navigate_to('Reporting', 'Scheduled Reports')

