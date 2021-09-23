#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/gui/monitor/reports/archived_reports.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.gui.guicommon import GuiCommon
from reports_base_esa import ReportsBaseEsa, ArchivedReportInfo


class ArchivedReports(ReportsBaseEsa):
    """Archived Reports page interaction class.

    Interact with GUI elements of Monitor -> Archived Reports page.

    Available report types constants:

    | AMP | Advanced Malware Protection |
    | AMP_VERDICT_UPDATES | Advanced Malware Protection Verdict Updates |
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
    case. This can be done via adding following line into the \*** Settings \*** section:
            Variables      esa/constants.py

    This types are used on report creation stage.

    Example of constant's usage:
    | Archived Reports Add Report | ${email_reports.VIRUS_TYPES} |

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

    def get_keyword_names(self):
        return ['archived_reports_add_report',
                'archived_reports_delete_report',
                'archived_reports_delete_all_reports',
                'archived_reports_get_reports']

    def _open_page(self):
        self._navigate_to('Monitor', 'Archived Reports')

    def archived_reports_add_report(self,
                                    report_type,
                                    title=None,
                                    report_format=None,
                                    time_range=None,
                                    email_to=None,
                                    archive=None,
                                    num_of_rows=None,
                                    sort_col=None,
                                    filter=None, ):
        """Add Email Archived Report.

        Use this method to add Archived Report.

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

        Examples:
        | Archived Reports Add Report | ${sma_email_reports.DELIVERY} |
        | ... | title=DeliveryStatusReport |
        | ... | report_format=pdf |
        | ... | archive=no |
        | ... | email_to=testuser@ironport.com |
        | ... | num_of_rows=100 |
        | ... | sort_col=delivered |

        | Archived Reports Add Report | ${sma_email_reports.VIRUS_TYPES} |
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
                                        num_of_rows, None, sort_col, filter)
        self._click_deliver_button()

    def archived_reports_delete_report(self, name):
        """Delete Email Archived Report.

        Use this method to Email Archived Report.

        Parameters:
        - `name`: To delete report name.

        Examples:
        | Archived Reports Delete Report | Report |
        """
        self._open_page()
        self._show_all()
        # 1 - number of column with reports names
        # 6 - number of column with checkboxes
        self._check_for_deletion(name, 1, 6)
        self._click_delete_button()

    def archived_reports_delete_all_reports(self):
        """Delete all Email Archived Reports.

        Use this method to delete all Archived Reports.

        Example:
        | Archived Reports Delete All Reports |
        """
        self._open_page()
        self._show_all()
        self._select_all_reports()
        self._click_delete_button()

    def archived_reports_get_reports(self):
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

        Example:
        | ${reports} = | Archived Reports Get Reports |
        """
        self._open_page()
        reports = self._get_reports_info(ArchivedReportInfo)
        return reports
