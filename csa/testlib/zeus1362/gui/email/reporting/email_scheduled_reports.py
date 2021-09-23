#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/gui/email/reporting/email_scheduled_reports.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from sma.constants import sma_email_reports
from common.gui.reports_base import ReportsBase
from common.gui.reports_base import ScheduledReportInfo
import common.gui.guiexceptions as guiexceptions

class EmailScheduledReports(ReportsBase):
    """Email Scheduled Reports page interaction class.

    This class designed to interact with GUI elements of Email -> Reporting ->
    Scheduled Reports page. Use keywords, listed below, to manipulate with
    Email Scheduled Reports.

    For report specific information please see
    http://eng.ironport.com/docs/qa/sarf/smakeyword/common/ReportsBase.html
    """

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['email_scheduled_reports_add_report',
                'email_scheduled_reports_edit_report',
                'email_scheduled_reports_add_domain_based_report',
                'email_scheduled_reports_edit_domain_based_report',
                'email_scheduled_reports_delete_report',
                'email_scheduled_reports_delete_all_reports',
                'email_scheduled_reports_get_reports'
               ]

    def _open_page(self):
        self._navigate_to('Email', 'Reporting', 'Scheduled Reports')

        err_msg = 'The Centralized Reporting service is currently ' + \
                'disabled'
        if self._is_text_present(err_msg):
            raise guiexceptions.GuiFeatureDisabledError(err_msg)

        err_msg = 'The feature key for this feature has expired or is ' + \
                'unavailable'
        if self._is_text_present(err_msg):
            raise guiexceptions.GuiFeaturekeyMissingError(err_msg)

    def email_scheduled_reports_add_report(self,
                                     report_type,
                                     title=None,
                                     report_format=None,
                                     time_range=None,
                                     schedule=None,
                                     email_to=None,
                                     num_of_rows=None,
                                     sort_col=None,
                                     filter=None,
                                     language=None,
                                     ):
        """Add Email Scheduled Report.

        Use this method to add Email Scheduled Report.

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
        - `sort_col`: string with values separated by colon. Available
        values depends on report type. For detailed information see
        'Reports Base' keyword doc.
        - `filter`: Either _global_ or _local_. Default _global_. Used only
        for Outbreak Filters report.
        - `language`: Report Language, String.it takes one of these languages
          portuguese, chinese, deutsch, english, japanese, russian, taiwan,
          france, espanol, korean, italian

        Examples:
        | Email Scheduled Reports Add Report | ${sma_email_reports.VOF} |
        | ... | title=OutbreakFiltersReport |
        | ... | report_format=pdf |
        | ... | schedule=monthly:03:30 |
        | ... | email_to=testuser@mail.qa |
        | ... | num_of_rows=50 |
        | ... | sort_col=total:time |
        | ... | filter=local |
        | ... | language=chinese |

        | Email Scheduled Reports Add Report | ${sma_email_reports.TLS_CONN} |
        | ... | title=TLSConnectionsReport |
        | ... | report_format=csv |
        | ... | time_range=last year |
        | ... | schedule=monthly:03:30 |
        | ... | email_to=testuser@ironport.com |
        | ... | sort_col=pref. failed:unencrypted |
        """

        self._open_page()
        self._click_add_scheduled_report_button()
        self._fill_report_data(report_type, title, report_format, time_range,
                               schedule, email_to, num_of_rows, None,
                               sort_col, filter, language)
        self._click_submit_button()

    def email_scheduled_reports_edit_report(self,
                                      title,
                                      new_title=None,
                                      report_format=None,
                                      time_range=None,
                                      schedule=None,
                                      email_to=None,
                                      num_of_rows=None,
                                      sort_col=None,
                                      filter=None,
                                      language=None,
                                      ):
        """Edit Email Scheduled Report.

        Use this method to edit Email Scheduled Report.

        Parameters:
        - `title`: To edit report title. String. Mandatory.
        - `new_title`: New report title.
        - `report format`: Either _pdf_ or _csv_. Default _pdf_.
         - `time_range`: time range for the data included in the report. String
        with values separated by semicolon. First value represents time
        interval: _last day_, _last week_, _last month_, _last year_, _num days_
        or _num months_. If _num days_ or _num months_ was chosen, second value
        represents number of days in interval, i.e: 'num days:30'.
        - `schedule`: scheduling options. String of values separated by
        semicolon. First one is schedule period: _daily_, _weekly_, _monthly_.
        Second - hour, i.e: 01,02,...24. Third - minutes: 00, 15, 30, 45. And
        last one, used only if schedule period is _weekly_, it represents day
        of week: _Sunday_, _Monday_...
        - `email_to`: string with e-mails. If you do not specify an email
        address, the report is archived only.
        - `num_of_rows`: for _pdf_ format. Number of rows to be included.
        - `sort_col`: string with values separated by semicolon. Available
        values depends on report type. For detailed information see
        'Reports Base' keyword doc.
        - `filter`: Either _global_ or _local_. Default _global_. Used only
        for Outbreak Filters report.
        - `language`: Report Language, String.it takes one of these languages
          portuguese, chinese, deutsch, english, japanese, russian, taiwan,
          france, espanol, korean, italian

        Examples:
        | Email Scheduled Reports Edit Report | SenderGroupsReport |
        | ... | new_title=myEditedSenderGroupsReport |
        | ... | report_format=pdf |
        | ... | time_range=num months:11 |
        | ... | schedule=monthly:01:00 |
        | ... | email_to=testuser@cisco.com |
        | ... | num_of_rows=50 |
        """

        self._open_page()
        self._click_edit_report_link(title)
        self._fill_report_data(None, new_title, report_format, time_range,
                               schedule, email_to, num_of_rows, None,
                               sort_col, filter, language)
        self._click_submit_button()

    def email_scheduled_reports_add_domain_based_report(self,
                                                       title=None,
                                                       report_format=None,
                                                       time_range=None,
                                                       schedule=None,
                                                       report_generation=None,
                                                       file_to_upload=None,
                                                       domains=None,
                                                       email_to=None,
                                                       outgoing_domain=None,
                                                       logo=None,
                                                       language=None
                                                       ):
        """Add Email Scheduled Domain-Based Executive Summary Report.

        Use this method to add Email Scheduled Domain-Based Report.

        Parameters:
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
        - `schedule`: scheduling options. String of values separated by
        semicolon. First one is schedule period: _daily_, _weekly_, _monthly_.
        Second - hour, i.e: 01,02,...24. Third - minutes: 00, 15, 30, 45. And
        last one, used only if schedule period is _weekly_, it represents day
        of week: _Sunday_, _Monday_...
        - `outgoing_domain`: domain type for the outgoing mail summary.
        Either _server_ or _email_address_. Default _server_.
        - `report_generation`: can be one of 'configfile' or 'individual'.
        - `domains`: a tuple of domains to generate report for. Applies only
         if `report_generation` is 'individual'.
        - `email_to`: a tuple of emails to send report to. Applies only if
        `report_generation` is 'individual'.
        - `file_to_upload`: either path to file on local machine or name of
        the file on the appliance. Applies only if `report_generation` is
        'configfile'.
        - `logo`: logo to use in the report. Either 'cisco' to use
        Cisco logo or path to logo file to use custom logo. None to
        use default value.
        - `language`: Report Language, String.it takes one of these languages
          portuguese, chinese, deutsch, english, japanese, russian, taiwan,
          france, espanol, korean, italian

        Examples:
        | Email Scheduled Reports Add Domain Based Report |
        | ... | title=DomainBasedReport |
        | ... | report_format=pdf |
        | ... | time_range=last year |
        | ... | schedule=monthly:03:30 |
        | ... | report_generation=individual |
        | ... | domains=qa12.qa, google.com |
        | ... | email_to=testuser@ironport.com |
        | ... | outgoing_domain=email_address |
        | ... | logo=cisco |
        | ... | language=russian |
        """

        self._open_page()
        self._click_add_scheduled_report_button()
        self._fill_report_data(sma_email_reports.DOMAIN_BASED, title,
                               report_format, time_range, schedule, None, None,
                               None,  None, None,language)
        self._select_report_generation(report_generation, file_to_upload,
                                       domains, email_to)
        if outgoing_domain is not None:
            self._select_outgoing_domain(outgoing_domain)

        self._select_logo(logo)
        self._click_submit_button()

    def email_scheduled_reports_edit_domain_based_report(self,
                                                       title,
                                                       new_title=None,
                                                       report_format=None,
                                                       time_range=None,
                                                       schedule=None,
                                                       report_generation=None,
                                                       file_to_upload=None,
                                                       domains=None,
                                                       email_to=None,
                                                       outgoing_domain=None,
                                                       logo=None,
                                                       language=None
                                                       ):
        """Edit Email Scheduled Domain-Based Executive Summary Report.

        Use this method to add Email Scheduled Domain-Based Report.

        Parameters:
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
        - `schedule`: scheduling options. String of values separated by
        semicolon. First one is schedule period: _daily_, _weekly_, _monthly_.
        Second - hour, i.e: 01,02,...24. Third - minutes: 00, 15, 30, 45. And
        last one, used only if schedule period is _weekly_, it represents day
        of week: _Sunday_, _Monday_...
        - `outgoing_domain`: domain type for the outgoing mail summary.
        Either _server_ or _email_address_. Default _server_.
        - `report_generation`: can be one of 'configfile' or 'individual'.
        - `domains`: a tuple of domains to generate report for. Applies only
         if `report_generation` is 'individual'.
        - `email_to`: a tuple of emails to send report to. Applies only if
        `report_generation` is 'individual'.
        - `file_to_upload`: either path to file on local machine or name of
        the file on the appliance. Applies only if `report_generation` is
        'configfile'.
        - `logo`: logo to use in the report. Either 'cisco' to use
        Cisco logo or path to logo file to use custom logo. None to
        use default value.
        - `language`: Report Language, String.it takes one of these languages
          portuguese, chinese, deutsch, english, japanese, russian, taiwan,
          france, espanol, korean, italian

        Examples:
        | Email Archived Reports Edit Domain Based Report |
        | ... | new_title=myEditedDomainBasedReport |
        | ... | report_format=csv |
        | ... | time_range=last week |
        | ... | schedule=daily:03:30 |
        | ... | report_generation=configfile |
        | ... | file_to_upload=config.dtd |
        | ... | outgoing_domain=server |
        | ... | logo=cisco |
        """

        self._open_page()
        self._click_edit_report_link(title)
        self._fill_report_data(sma_email_reports.DOMAIN_BASED, new_title,
                               report_format, time_range, schedule, None, None,
                               None,  None, None,language)
        self._select_report_generation(report_generation, file_to_upload,
                                       domains, email_to)
        if outgoing_domain is not None:
            self._select_outgoing_domain(outgoing_domain)

        self._select_logo(logo)
        self._click_submit_button()

    def email_scheduled_reports_delete_report(self, name):
        """Delete Email Scheduled Report.

        Use this method to delete Email Scheduled Report.

        Parameters:
        - `name`: title of report to be deleted.

        Examples:
        | Email Scheduled Reports Delete Report | Report1 |
        """

        self._open_page()
        # 2 - number of column with reports names
        # 9 - number of column with checkboxes
        self._check_for_deletion(name, 2, 9)
        self._click_delete_button()

    def email_scheduled_reports_delete_all_reports(self):
        """Delete all Email Scheduled Reports.

        Use this method to delete all Email Scheduled Reports.

        Example:
        | Email Scheduled Reports Delete All Reports |
        """

        self._open_page()
        self._select_all_reports()
        self._click_delete_button()

    def email_scheduled_reports_get_reports(self):
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
            run.

        Example:
        | ${reports} = | Email Scheduled Reports Get Reports |
        """

        self._open_page()
        reports = self._get_reports_info(ScheduledReportInfo)

        return reports
