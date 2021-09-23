#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/gui/monitor/reports/scheduled_reports.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.decorators import set_speed
from reports_base_esa import ReportsBaseEsa, ScheduledReportInfo


class ScheduledReports(ReportsBaseEsa):
    """Scheduled Reports page interaction class.

    Interact with GUI elements of Monitor -> Scheduled Reports page.

    Available report types constants:

    | AMP |
    | AMP_VERDICT_UPDATES |
    | FILTERS | Content Filters |
    | DLP_INCIDENT | DLP Incident Summary |
    | DELIVERY | Delivery Status |
    | DOMAIN_BASED | Domain-Based Executive Summary |
    | EXECUTIVE | Executive Summary |
    | IN_MAIL | Incoming Mail Summary |
    | INT_USERS | Internal Users Summary |
    | OUT_DESTINATIONS | Outgoing Destinations |
    | OUT_MAIL | Outgoing Mail Summary |
    | OUT_DOMAIN_SENDERS | Outgoing Senders: Domains |
    | SENDER_GROUPS | Sender Groups |
    | SYSTEM_CAP | Email System Capacity |
    | TLS_CONN | TLS Connections |
    | VOF | Outbreak Filters |
    | VIRUS_TYPES | Virus Types |
    | RATE_LIMIT | Rate Limits |

    To be able to use constants user should add 'constants.py' file to the test
    case. This can be done via adding following into the \*** Settings \*** section:
            Variables      esa/constants.py

    This types are used on report creation stage.

    Example of constant's usage:
    | Scheduled Reports Add Report | ${email_reports.DELIVERY} |

    Every email report type has it's specifics sort column values.

    Sorting column values for email reports:

    Dlp Incident Summary:
    | 'low' |
    | 'medium' |
    | 'high' |
    | 'critical' |
    | 'total' |
    | 'delivered enc' |
    | 'delivered clear' |
    | 'dropped' |

    Delivery Status:
    | 'host status' |
    | 'active' |
    | 'connections out' |
    | 'delivered' |
    | 'soft' |
    | 'hard' |

    Outbreak Filters:
    | 'total' | 'outbreak' |
    | | 'first seen' |
    | | 'time' |
    | | 'messages' |

    Outgoing Destinations:
    | 'spam' |
    | 'virus' |
    | 'stopped' |
    | 'threat' |
    | 'clean' |
    | 'total processed' |
    | 'hard' |
    | 'delivered' |
    | 'total delivered' |

    Outgoing Senders: Domains:
    | 'spam' |
    | 'virus' |
    | 'stopped' |
    | 'threat' |
    | 'clean' |
    | 'total' |

    Tls Connections:
    | 'req. failed' | 'req. failed' |
    | 'req. success' | 'req. success' |
    | 'pref. failed' | 'pref. failed' |
    | 'pref success' | 'pref success' |
    | 'total' | 'total' |
    | 'unencrypted' | 'unencrypted' |
    | 'messages' | 'messages' |

    Virus Types:
    | 'incoming' |
    | 'outgoing' |
    | 'total infected' |
    """

    # method required by RF
    # return a list with all public methods
    def get_keyword_names(self):
        return ['scheduled_reports_add_report',
                'scheduled_reports_edit_report',
                'scheduled_reports_delete_report',
                'scheduled_reports_delete_all_reports',
                'scheduled_reports_get_reports', ]

    def _open_page(self):
        self._navigate_to('Monitor', 'Scheduled Reports')

    @set_speed(0)
    def scheduled_reports_add_report(self,
                                     report_type,
                                     title=None,
                                     report_format=None,
                                     time_range=None,
                                     schedule=None,
                                     email_to=None,
                                     num_of_rows=None,
                                     sort_col=None,
                                     filter=None, ):
        """Add Scheduled Report.

        Use this method to add Scheduled Report.

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

        Examples:
        | Scheduled Reports Add Report | ${email_reports.VOF} |
        | ... | title=OutbreakFiltersReport |
        | ... | report_format=pdf |
        | ... | schedule=monthly:03:30 |
        | ... | email_to=testuser@mail.qa |
        | ... | num_of_rows=50 |
        | ... | sort_col=total:time |
        | ... | filter=local |

        | Scheduled Reports Add Report | ${email_reports.TLS_CONN} |
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
                               sort_col, filter)
        self._click_submit_button()

    @set_speed(0)
    def scheduled_reports_edit_report(self,
                                      title,
                                      new_title=None,
                                      report_format=None,
                                      time_range=None,
                                      schedule=None,
                                      email_to=None,
                                      num_of_rows=None,
                                      sort_col=None,
                                      filter=None, ):
        """Edit Scheduled Report.

        Use this method to edit Scheduled Report.

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

        Examples:
        | Scheduled Reports Edit Report | SenderGroupsReport |
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
                               sort_col, filter)
        self._click_submit_button()

    @set_speed(0)
    def scheduled_reports_delete_report(self, name):
        """Delete Scheduled Report.

        Use this method to delete Scheduled Report.

        Parameters:
        - `name`: title of report to be deleted.

        Examples:
        | Scheduled Reports Delete Report | Report1 |
        """

        self._open_page()
        # 2 - number of column with reports names
        # 8 - number of column with checkboxes
        self._check_for_deletion(name, 2, 8)
        self._click_delete_button()

    @set_speed(0)
    def scheduled_reports_delete_all_reports(self):
        """Delete all Email Scheduled Reports.

        Use this method to delete all Scheduled Reports.

        Example:
        | Scheduled Reports Delete All Reports |
        """

        self._open_page()
        self._select_all_reports()
        self._click_delete_button()

    @set_speed(0)
    def scheduled_reports_get_reports(self):
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

        Example:
        | ${reports} = | Scheduled Reports Get Reports |
        """

        self._open_page()
        reports = self._get_reports_info(ScheduledReportInfo)

        return reports
