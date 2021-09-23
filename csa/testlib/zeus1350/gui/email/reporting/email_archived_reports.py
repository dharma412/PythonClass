#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/email/reporting/email_archived_reports.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from sma.constants import sma_email_reports
from common.gui.reports_base import ReportsBase
from common.gui.reports_base import ArchivedReportInfo
import common.gui.guiexceptions as guiexceptions


class EmailArchivedReports(ReportsBase):
    """Email Archived Reports page interaction class.

    This class designed to interact with GUI elements of Email -> Reporting ->
    Archived Reports page. Use keywords, listed below, to manipulate with
    Email Archived Reports.

    For report specific information please see
    http://eng.ironport.com/docs/qa/sarf/smakeyword/common/ReportsBase.html
    """

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['email_archived_reports_add_report',
                'email_archived_reports_delete_report',
                'email_archived_reports_delete_all_reports',
                'email_archived_reports_add_domain_based_report',
                'email_archived_reports_get_reports'
                ]

    def _open_page(self):
        self._navigate_to('Email', 'Reporting', 'Archived Reports')

        err_msg = 'The feature key for this feature has expired or is ' + \
                  'unavailable'
        if self._is_text_present(err_msg):
            raise guiexceptions.GuiFeaturekeyMissingError(err_msg)

    def email_archived_reports_add_report(self,
                                          report_type,
                                          title=None,
                                          report_format=None,
                                          time_range=None,
                                          email_to=None,
                                          archive=None,
                                          num_of_rows=None,
                                          sort_col=None,
                                          filter=None,
                                          language=None,
                                          ):
        """Add Email Archived Report.

        Use this method to add Email Archived Report.

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
        - `sort_col`: string with values separated by colon. Available
        values depends on report type. For detailed information see
        'Reports Base' keyword doc.
        - `filter`: Either _global_ or _local_. Default _global_. Used only
        for Outbreak Filters report.
        - `language`: Report Language, String.it takes one of these languages
          portuguese, chinese, deutsch, english, japanese, russian, taiwan,
          france, espanol, korean, italian

        Examples:
        | Email Archived Reports Add Report | ${sma_email_reports.DELIVERY} |
        | ... | title=DeliveryStatusReport |
        | ... | report_format=pdf |
        | ... | archive=no |
        | ... | email_to=testuser@ironport.com |
        | ... | num_of_rows=100 |
        | ... | sort_col=delivered |

        | Email Archived Reports Add Report | ${sma_email_reports.VIRUS_TYPES} |
        | ... | title=VirusTypesReport |
        | ... | report_format=csv |
        | ... | time_range=timestamp:01 Apr 2011 01:24 Apr 2011 20 |
        | ... | archive=yes |
        | ... | email_to=test@cisco.com |
        | ... | sort_col=outgoing |
        """

        self._open_page()
        self._click_add_archived_report_button()
        self._fill_archived_report_data(report_type, title, report_format,
                                        time_range, email_to, archive,
                                        num_of_rows, None, sort_col, filter, language)
        self._click_deliver_button()

    def email_archived_reports_add_domain_based_report(self,
                                                       title=None,
                                                       report_format=None,
                                                       time_range=None,
                                                       report_generation=None,
                                                       file_to_upload=None,
                                                       domains=None,
                                                       email_to=None,
                                                       outgoing_domain=None,
                                                       logo=None,
                                                       language=None
                                                       ):
        """Add Email Archived Domain-Based Executive Summary Report.

        Use this method to add Email Archived Domain-Based Report.

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
        | Email Archived Reports Add Domain Based Report |
        | ... | title=DomainBasedReport |
        | ... | report_format=pdf |
        | ... | time_range=last year |
        | ... | report_generation=individual |
        | ... | domains=qa12.qa, google.com |
        | ... | email_to=testuser@ironport.com |
        | ... | outgoing_domain=email_address |
        | ... | logo=cisco |
        """

        self._open_page()
        self._click_add_archived_report_button()
        self._fill_report_data(sma_email_reports.DOMAIN_BASED, title,
                               report_format, time_range, None, None, None,
                               None, None, None, language)
        self._select_report_generation(report_generation, file_to_upload,
                                       domains, email_to)
        if outgoing_domain is not None:
            self._select_outgoing_domain(outgoing_domain)

        self._select_logo(logo)
        self._click_deliver_button()

    def email_archived_reports_delete_report(self, name):
        """Delete Email Archived Report.

        Use this method to delete Email Archived Report.

        Parameters:
        - `name`: To delete report name.

        Examples:
        | Email Archived Reports Delete Report | Report |
        """

        self._open_page()
        self._show_all()
        # 1 - number of column with reports names
        # 7 - number of column with checkboxes
        self._check_for_deletion(name, 1, 7)
        self._click_delete_button()

    def email_archived_reports_delete_all_reports(self):
        """Delete all Email Archived Reports.

        Use this method to delete all Email Archived Reports.

        Example:
        | Email Archived Reports Delete All Reports |
        """

        self._open_page()
        self._show_all()
        self._select_all_reports()
        self._click_delete_button()

    def email_archived_reports_get_reports(self):
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
            generated.

        Example:
        | ${reports} = | Email Archived Reports Get Reports |
        """

        self._open_page()
        reports = self._get_reports_info(ArchivedReportInfo)

        return reports
