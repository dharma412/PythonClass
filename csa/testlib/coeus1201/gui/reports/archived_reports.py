#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/reports/archived_reports.py#1 $

from reports_base import ReportsBase

class ArchivedReports(ReportsBase):
    """Archived Reports page interaction class.

    This class designed to interact with GUI elements of Reporting ->
    Archived Reports page. Use keywords, listed below, to manipulate with
    Archived Reports.

    For report specific information please see 'Reports Base' keyword document.
    """

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['archived_reports_add_report',
                'archived_reports_delete_report',
                'archived_reports_delete_all_reports',
               ]

    def archived_reports_add_report(self,
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
        """Add Archived Report.

        Use this method to add Archived Report.

        Parameters:
        - `report_type`: type of report to be added. Mandatory.
        - `title`: report title. String. By default used pattern <Report Type>.
        - `report format`: Either _pdf_ or _csv_. Default _pdf_.
        - `time_range`: time range for the data included in the report. String
        with values separated by colon. First value represents time interval:
        _last day_, _last week_, _last month_ or _timestamp_. If _timestamp_
        was chosen, second values represents start date and end date in reported
        period. Date format: dd Mmm yyyy hh
        Example: timestamp:01 Apr 2011 01:24 Apr 2011 20
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
        | ${type} | Set Variable | overview |

        | Archived Reports Add Report    ${type} |
        | ... | title=Report1 |
        | ... | report_format=pdf |
        | ... | time_range=timestamp:01 Apr 2011 00:05 Apr 2011 23 |
        | ... | archive=yes |
        | ... | email_to=mkrysiuk@ironport.com |

        | ${type} | Set Variable | anti-malware |

        | Archived Reports Add Report | ${type} |
        | ... | title=Report4 |
        | ... | report_format=csv |
        | ... | time_range=last week |
        | ... | archive=yes |
        | ... | num_of_rows=50 |
        | ... | chart_data=requests monitored:total blocked |
        | ... | sort_col=total monitored:total blocked |
        """

        self._open_page()
        self.click_button("xpath=//input[@title='Generate Report Now...']")

        self._select_report_type(report_type)
        self.wait_until_page_loaded()

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

        if archive is not None:
            self._set_archive_setting(archive)

        if email_to is not None:
                self.select_checkbox("xpath=//input[@id='deliver']")
                self._fill_email_to(email_to)

        if archive is not None and archive.lower() == 'no' and email_to is None:
            guiexceptions.ConfigError(
                'You have to specify at least one option: ' + \
                'either \'archive\' or \'email to\'.')

        self._submit()

    def archived_reports_delete_report(self, name):
        """Delete Archived Report.

        Use this method to delete Archived Report.

        Parameters:
        - `name`: To delete report name.

        Examples:
        | Archived Reports Delete Report | Report1 |

        | Archived Reports Delete Report | Report5 |
        """

        self._open_page()
        self._show_all()
        self._check_for_deletion(name, 1, 6)
        self._click_delete_button()

    def archived_reports_delete_all_reports(self):
        """Delete all Archived Reports.

        Use this method to delete all Archived Reports.

        Example:
        | Archived Reports Delete All Reports |
        """

        self._open_page()
        self._show_all()
        self.click_element("xpath=//input[@id='del_0']", "don't wait")
        self._click_delete_button()

    def _open_page(self):
        self._navigate_to('Reporting', 'Archived Reports')

    def _submit(self):
        deliver_button = "xpath=//input[@value='Deliver This Report']"
        self.click_button(deliver_button)
        self._check_action_result()


