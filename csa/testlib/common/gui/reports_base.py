#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports_base.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import os
import re
import time
from datetime import date, timedelta, datetime
from time import localtime

from sma.constants import sma_email_reports
from sma.constants import sma_web_reports
import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon


class ReportCheckError(guiexceptions.GuiError):
    """ Incorrect values were present on the page
    """

    # The special exception the product page validator
    def __init__(self, msg, page_errors=None):
        self.msg = msg
        if page_errors:
            self.page_errors = page_errors
        else:
            self.page_errors = list()

    def __str__(self):
        return str(self.msg) + ':\n\n' + '\n'.join(map(str, self.page_errors))

    # used by Robot Framework to print message to console and log
    def __unicode__(self):
        return unicode(self.__str__())


class ReportsBase(GuiCommon):
    """Base class for support report manipulation.

    This class provides basic actions for reports configuration libraries.
    To manipulate with reports you should be aware of supported report types.

    Available web report types constants:

    | OVERVIEW | 'Overview' |
    | USERS | 'Users' |
    | WEB_SITES | 'Web Sites' |
    | URL_CAT | 'URL Categories' |
    | URL_CAT_EXTENDED | 'Top URL Categories - Extended' |
    | APP_VISIBILITY | 'Application Visibility' |
    | TOP_APP_TYPES | 'Top Application Types - Extended' |
    | ANTIMALWARE | 'Anti-Malware' |
    | MALWARE_RISK | 'Client Malware Risk' |
    | WBRS_FILTERS | 'Web Reputation Filters' |
    | L4TM | 'L4 Traffic Monitor' |
    | USER_LOCATION | 'Reports by User Location' |
    | SYSTEM_CAP | 'Web System Capacity' |
    | SYSTEM_CAP_OVERVIEW | 'System Capacity Overview' |

    Available email report types constants:

    | FILTERS | 'Content Filters' |
    | DLP_INCIDENT | 'DLP Incident Summary' |
    | DELIVERY | 'Delivery Status' |
    | DOMAIN_BASED | 'Domain-Based Executive Summary' |
    | EXECUTIVE | 'Executive Summary' |
    | IN_MAIL | 'Incoming Mail Summary' |
    | INT_USERS | 'Internal Users Summary' |
    | OUT_DESTINATIONS | 'Outgoing Destinations' |
    | OUT_MAIL | 'Outgoing Mail Summary' |
    | OUT_DOMAIN_SENDERS | 'Outgoing Senders: Domains' |
    | SENDER_GROUPS | 'Sender Groups' |
    | SYSTEM_CAP | 'Email System Capacity' |
    | TLS_CONN | 'TLS Connections' |
    | VOF | 'Outbreak Filters' |
    | VIRUS_TYPES | 'Virus Types' |
    | APP | 'Advance Phishing Protection' |

    To be able to use constants user should add 'constants.py' file to the test
    case. This can be done via adding following line at the top of the test
    case under \*** Settings \*** section:
            Variables      sma/constants.py

    This types are used on report creation stage.

    Example of constant's usage:
    | Web Scheduled Reports Add Report | ${sma_web_reports.OVERVIEW} |
    | Web Archived Reports Add Report | ${sma_web_reports.URL_CAT} |
    | Email Scheduled Reports Add Report | ${sma_email_reports.DELIVERY} |
    | Email Archived Reports Add Report | ${sma_email_reports.VIRUS_TYPES} |

    Every web report type has it's specifics chart data values and sort column
    values.

    Every email report type has it's specifics sort column values.

    Chart data values for web report types:

    Overview:
    | N/A |

    Users:
    | Top Users (Left) | Top Users (Right) |
    | `bw used` | `bw used` |
    | `bw saved` | `bw saved` |
    | `time spent` | `time spent` |
    | `webcat blocked` | `webcat blocked` |
    | `app blocked` | `app blocked` |
    | `wbrs blocked` | `wbrs blocked` |
    | `amv blocked` | `amv blocked` |
    | `other blocked` | `other blocked` |
    | `total warned` | `total warned` |
    | `total completed` | `total completed` |
    | `total blocked` | `total blocked` |
    | `transactions total` | `transactions total` |

    Web Sites:
    | Top Domains | Top Domains |
    | `bw used` | `bw used` |
    | `bw saved` | `bw saved` |
    | `time spent` | `time spent` |
    | `webcat blocked` | `webcat blocked` |
    | `app blocked` | `app blocked` |
    | `wbrs blocked` | `wbrs blocked` |
    | `amv blocked` | `amv blocked` |
    | `other blocked` | `other blocked` |
    | `total completed` | `total completed` |
    | `total blocked` | `total blocked` |
    | `transactions total` | `transactions total` |

    Url Categories:
    | Top URL Categories | Top URL Categories |
    | `bw used` | `bw used` |
    | `bw saved` | `bw saved` |
    | `time spent` | `time spent` |
    | `webcat allowed` | `webcat allowed` |
    | `webcat warned` | `webcat warned` |
    | `webcat blocked` | `webcat blocked` |
    | `total completed` | `total completed` |
    | `total blocked` | `total blocked` |
    | `transactions total` | `transactions total` |
    | | `blocked and warned` |

    Top Url Categories - Extended:
    | N/A |

    Application Visibility:
    | Top Application Types | Top Applications |
    | `bw used` | `bw used` |
    | `completed` | `completed` |
    | `limited` | `limited` |
    | `not limited` | `not limited`  |
    | `blocked` | `blocked` |
    | `avc blocked` | `avc blocked` |
    | `transactions total` | `transactions total` |

    Top Application Types - Extended:
    | N/A |

    Anti-Malware:
    | Top Malware Categories | Top Malware Threats |
    | `bw saved` | `bw saved` |
    | `requests monitored` | `total monitored` |
    | `responses monitored` | `total blocked` |
    | `requests blocked` | `total detected` |
    | `responses blocked` | `monitored or blocked` |
    | `total monitored` | |
    | `total blocked` | |
    | `total detected` | |
    | `monitored or blocked` | |

    Client Malware Risk:
    | Web Proxy - Top Clients | L4 Traffic Monitor |
    | `bw saved` | `total monitored` |
    | `requests monitored` | `total blocked` |
    | `responses monitored` | `total detected` |
    | `requests blocked` | |
    | `responses blocked` | |
    | `total monitored` | |
    | `total blocked` | |
    | `total detected` | |
    | `monitored or blocked` | |

    Web Reputation Filters:
    | N/A |

    L4 Traffic Monitor:
    | Top Client IPs | Top Malware Sites |
    | `total monitored` | `total monitored` |
    | `total blocked` | `total blocked` |
    | `total detected` | `total detected` |

    Reports By User Location:
    | N/A |

    System Capacity Overview:
    | N/A |

    System Capacity:
    | N/A |

    To specify report chart data use values represented above.

    Example:
    | Web Scheduled Reports Add Report | ${sma_web_reports.URL_CAT} |
    | ... | title=Report2 |
    | ... | report_format=pdf |
    | ... | time_range=num days:50 |
    | ... | schedule=monthly:03:30 |
    | ... | email_to=test_mail@ironport.com |
    | ... | num_of_rows=20 |
    | ... | chart_data=webcat warned:webcat blocked |
    | ... | sort_col=time spent |

    In this example we specified chart data for `url categories` report type.
    First chart will contain `webcat warned` values, and second one
    `webcat blocked` values.
    To specify only one chart data and leave another default or with it's
    previous value just pass ${None} or None as it's value (See second example):

    Example:
    | Web Scheduled Reports Add Report | ${sma_web_reports.URL_CAT} |
    | ... | title=Report2 |
    | ... | report_format=pdf |
    | ... | time_range=num days:50 |
    | ... | schedule=monthly:03:30 |
    | ... | email_to=test_mail@ironport.com |
    | ... | num_of_rows=20 |
    | ... | chart_data=${None}:webcat blocked |
    | ... | sort_col=time spent |

    To select certain sort column values use next tables:

    Sorting column values for web reports:

    Overview, Reports By User Location, System Capacity:
    | N/A |

    Users, Url Categories, Web Sites, Top Url Categories - Extended:
    | 'bw used' |
    | 'time spent' |
    | 'total completed' |
    | 'total blocked' |
    | 'transactions total' |

    Application Visibility, Top Application Types - Extended:
    | 'bw used' |
    | 'completed' |
    | 'blocked' |
    | 'total' |

    Anti-Malware, Client Malware Risk, L4 Traffic Monitor:
    | 'total monitored' |
    | 'total blocked' |
    | 'total detected' |

    Web Reputation Filters:
    | 'block' |
    | 'malware detected' |
    | 'clean' |
    | 'allow' |

    System Capacity Overview:
    | 'cpu used' |
    | 'response time' |
    | 'proxy buffer memory' |
    | 'transactions per sec' |
    | 'connection out' |
    | 'bw out' |

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

    Advanced Phishing Protection:
    | 'Message Forwarding Success' |
    | 'Message Forwarding Failure' |

    Next example shows how to specify sorting column for report:

    Example:

    | ${type} | Set Variable | ${sma_web_reports.L4TM} |
    | Web Scheduled Reports Add Report | ${type} |
    | ... | title=Report7 |
    | ... | report_format=pdf |
    | ... | time_range=last week |
    | ... | schedule=monthly:03:30 |
    | ... | email_to=test_mail@ironport.com |
    | ... | num_of_rows=50 |
    | ... | chart_data=total monitored:total detected |
    | ... | sort_col=total monitored:total blocked:total detected |

    In this example we specify three sorting columns for l4 traffic monitor
    report. To leave previous value or default value see chart data examples.
    """

    _available_user_chart_types = \
        {'bw used': 'WEB_USER_DETAIL.BANDWIDTH_USED',
         'bw saved': 'BANDWIDTH_SAVED',
         'time spent': 'WEB_USER_DETAIL.TIME_SPENT',
         'webcat blocked': 'WEB_USER_DETAIL.BLOCKED_BY_WEBCAT',
         'app blocked': 'WEB_USER_DETAIL.BLOCKED_BY_APPLICATION',
         'wbrs blocked': 'WEB_USER_DETAIL.BLOCKED_BY_WBRS',
         'amv blocked': 'WEB_USER_DETAIL.BLOCKED_MALWARE',
         'other blocked': 'WEB_USER_DETAIL.BLOCKED_BY_ADMIN_POLICY',
         'total warned': 'WEB_USER_DETAIL.WARNED_TOTAL',
         'total completed': 'WEB_USER_DETAIL.COMPLETED_TRANSACTION_TOTAL',
         'total blocked': 'WEB_USER_DETAIL.BLOCKED_TRANSACTION_TOTAL',
         'transactions total': 'WEB_USER_DETAIL.TRANSACTION_TOTAL'
         }

    _available_domain_chart_types = \
        {'bw used': 'DOMAINS.BANDWIDTH_USED',
         'bw saved': 'BANDWIDTH_SAVED_BY_BLOCKING',
         'time spent': 'DOMAINS.TIME_SPENT',
         'webcat blocked': 'DOMAINS.BLOCKED_BY_WEBCAT',
         'app blocked': 'DOMAINS.BLOCKED_BY_AVC',
         'wbrs blocked': 'DOMAINS.BLOCKED_BY_WBRS',
         'amv blocked': 'DOMAINS.BLOCKED_BY_AMW',
         'other blocked': 'DOMAINS.OTHER_BLOCKED',
         'total completed': 'DOMAINS.COMPLETED_TRANSACTION_TOTAL',
         'total blocked': 'DOMAINS.BLOCKED_TRANSACTION_TOTAL',
         'transactions total': 'DOMAINS.TRANSACTION_TOTAL'
         }

    _available_webcat_chart_types = \
        {'bw used': 'WEB_WEBCAT_DETAIL.BANDWIDTH_USED',
         'bw saved': 'BANDWIDTH_SAVED',
         'time spent': 'WEB_WEBCAT_DETAIL.TIME_SPENT',
         'webcat allowed': 'WEB_WEBCAT_DETAIL.ALLOWED_BY_WEBCAT',
         'webcat warned': 'WEB_WEBCAT_DETAIL.WARNED_BY_WEBCAT',
         'webcat blocked': 'WEB_WEBCAT_DETAIL.BLOCKED_BY_WEBCAT',
         'total completed': 'WEB_WEBCAT_DETAIL.COMPLETED_TRANSACTION_TOTAL',
         'total blocked': 'WEB_WEBCAT_DETAIL.BLOCKED_TRANSACTION_TOTAL',
         'transactions total': 'WEB_WEBCAT_DETAIL.TRANSACTION_TOTAL',
         'blocked and warned': 'WEB_WEBCAT_DETAIL.WARNED_BY_WEBCAT' + \
                               ',WEB_WEBCAT_DETAIL.BLOCKED_BY_WEBCAT'
         }

    _available_avc_chart_types = \
        {'bw used': 'WEB_APPLICATION_TYPE_DETAIL.BANDWIDTH_USED',
         'completed': 'WEB_APPLICATION_TYPE_DETAIL.COMPLETED_TRANSACTION_TOTAL',
         'limited': 'WEB_APPLICATION_TYPE_DETAIL.BW_LIMITED',
         'not limited': 'WEB_APPLICATION_TYPE_DETAIL.BW_NOT_LIMITED',
         'blocked': 'WEB_APPLICATION_TYPE_DETAIL.BLOCKED_TRANSACTION_TOTAL',
         'avc blocked': 'WEB_APPLICATION_TYPE_DETAIL.BLOCKED_BY_AVC',
         'transactions total': 'WEB_APPLICATION_TYPE_DETAIL.TRANSACTION_TOTAL'
         }

    _available_avc_name_chart_types = \
        {'bw used': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL.BANDWIDTH_USED',
         'completed': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL' + \
             '.COMPLETED_TRANSACTION_TOTAL',
         'limited': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL.BW_LIMITED',
         'not limited': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL.BW_NOT_LIMITED',
         'blocked': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL' + \
             '.BLOCKED_TRANSACTION_TOTAL',
         'avc blocked': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL.BLOCKED_BY_AVC',
         'transactions total': \
             'WEB_APPLICATION_NAME_APPLICATION_TYPE_DETAIL.TRANSACTION_TOTAL'
         }

    _available_amv_chart_categories = \
        {'category': 'key',
         'bw saved': 'BANDWIDTH_SAVED',
         'requests monitored': 'WEB_MALWARE_CATEGORY.MONITORED_MALWARE_REQUEST',
         'responses monitored': \
             'WEB_MALWARE_CATEGORY.MONITORED_MALWARE_RESPONSE',
         'requests blocked': 'WEB_MALWARE_CATEGORY.BLOCKED_MALWARE_REQUEST',
         'responses blocked': 'WEB_MALWARE_CATEGORY.BLOCKED_MALWARE_RESPONSE',
         'total monitored': 'WEB_MALWARE_CATEGORY.MONITORED_MALWARE',
         'total blocked': 'WEB_MALWARE_CATEGORY.BLOCKED_MALWARE',
         'total detected': 'WEB_MALWARE_CATEGORY.DETECTED_MALWARE',
         'monitored or blocked': \
             'WEB_MALWARE_CATEGORY.MONITORED_MALWARE' + \
             ',WEB_MALWARE_CATEGORY.BLOCKED_MALWARE',
         }

    _available_amv_chart_threats = \
        {'category': 'key1',
         'bw saved': 'BANDWIDTH_SAVED',
         'total monitored': \
             'WEB_MALWARE_NAME_MALWARE_CATEGORY_DETAIL.MONITORED_MALWARE',
         'total blocked': \
             'WEB_MALWARE_NAME_MALWARE_CATEGORY_DETAIL.BLOCKED_MALWARE',
         'total detected': \
             'WEB_MALWARE_NAME_MALWARE_CATEGORY_DETAIL.DETECTED_MALWARE',
         'monitored or blocked': \
             'WEB_MALWARE_NAME_MALWARE_CATEGORY_DETAIL.MONITORED_MALWARE' + \
             ',WEB_MALWARE_NAME_MALWARE_CATEGORY_DETAIL.BLOCKED_MALWARE'
         }

    _available_client_activity_chart = \
        {'bw saved': 'BANDWIDTH_SAVED',
         'requests monitored': 'WEB_USER_DETAIL.MONITORED_MALWARE_REQUEST',
         'responses monitored': 'WEB_USER_DETAIL.MONITORED_MALWARE_RESPONSE',
         'requests blocked': 'WEB_USER_DETAIL.BLOCKED_MALWARE_REQUEST',
         'responses blocked': 'WEB_USER_DETAIL.BLOCKED_MALWARE_RESPONSE',
         'total monitored': 'WEB_USER_DETAIL.MONITORED_MALWARE',
         'total blocked': 'WEB_USER_DETAIL.BLOCKED_MALWARE',
         'total detected': 'WEB_USER_DETAIL.DETECTED_MALWARE_TOTAL',
         'monitored or blocked': \
             'WEB_USER_DETAIL.MONITORED_MALWARE,WEB_USER_DETAIL.BLOCKED_MALWARE'
         }

    _available_client_activity_traffic = \
        {'total monitored': 'WEB_USER_BY_TRAFFIC_MONITOR.MONITORED_MALWARE',
         'total blocked': 'WEB_USER_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE',
         'total detected': \
             'WEB_USER_BY_TRAFFIC_MONITOR.MONITORED_MALWARE' + \
             ',WEB_USER_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE'
         }

    _available_traffic_monitor_by_user_chart = \
        {'total monitored': 'WEB_USER_BY_TRAFFIC_MONITOR.MONITORED_MALWARE',
         'total blocked': 'WEB_USER_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE',
         'total detected': 'WEB_USER_BY_TRAFFIC_MONITOR.MONITORED_MALWARE' + \
                           ',WEB_USER_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE'
         }

    _available_traffic_monitor_by_host_chart = \
        {'total monitored': 'WEB_HOST_BY_TRAFFIC_MONITOR.MONITORED_MALWARE',
         'total blocked': 'WEB_HOST_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE',
         'total detected': 'WEB_HOST_BY_TRAFFIC_MONITOR.MONITORED_MALWARE' + \
                           ',WEB_HOST_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE'
         }

    _report_type_to_chart_data = \
        {sma_web_reports.OVERVIEW: None,
         sma_web_reports.USERS: _available_user_chart_types,
         sma_web_reports.WEB_SITES: _available_domain_chart_types,
         sma_web_reports.URL_CAT: _available_webcat_chart_types,
         sma_web_reports.URL_CAT_EXTENDED: None,
         sma_web_reports.APP_VISIBILITY: None,
         sma_web_reports.TOP_APP_TYPES: None,
         sma_web_reports.ANTIMALWARE: None,
         sma_web_reports.MALWARE_RISK: None,
         sma_web_reports.WBRS_FILTERS: None,
         sma_web_reports.L4TM: None,
         sma_web_reports.USER_LOCATION: None,
         sma_web_reports.SYSTEM_CAP_OVERVIEW: None,
         sma_web_reports.SYSTEM_CAP: None
         }

    _report_types = \
        {sma_web_reports.OVERVIEW: 'wsa_monitor_overview_scheduled',
         sma_web_reports.USERS: 'wsa_users',
         sma_web_reports.WEB_SITES: 'wsa_web_sites',
         sma_web_reports.URL_CAT: 'wsa_url_categories',
         sma_web_reports.URL_CAT_EXTENDED: 'wsa_top_n_categories',
         sma_web_reports.TOP_APP_TYPES: 'wsa_top_n_applications',
         sma_web_reports.APP_VISIBILITY: 'wsa_applications',
         sma_web_reports.ANTIMALWARE: 'wsa_malware',
         sma_web_reports.MALWARE_RISK: 'wsa_client_activity',
         sma_web_reports.WBRS_FILTERS: 'wsa_web_reputation_filters',
         sma_web_reports.L4TM: 'wsa_l4_traffic_monitor',
         sma_web_reports.USER_LOCATION: 'wsa_mus_scheduled',
         sma_web_reports.SYSTEM_CAP_OVERVIEW: 'wsa_sma_system_capacity',
         sma_web_reports.SYSTEM_CAP: 'wsa_sma_system_capacity_detail',
         sma_email_reports.FILTERS: 'mga_content_filters',
         sma_email_reports.DLP_INCIDENT: 'mga_dlp_incident_summary',
         sma_email_reports.DELIVERY: 'mga_outgoing_delivery_status',
         sma_email_reports.DOMAIN_BASED: 'mga_domain_overview',
         sma_email_reports.EXECUTIVE: 'mga_overview_scheduled',
         sma_email_reports.IN_MAIL: 'mga_incoming_mail_scheduled',
         sma_email_reports.INT_USERS: 'mga_internal_user_scheduled',
         sma_email_reports.VOF: 'mga_virus_outbreaks_scheduled',
         sma_email_reports.OUT_DESTINATIONS: 'mga_destination_domains',
         sma_email_reports.OUT_MAIL: 'mga_outgoing_mail_scheduled',
         sma_email_reports.OUT_DOMAIN_SENDERS: 'mga_internal_senders',
         sma_email_reports.SENDER_GROUPS: 'mga_sender_groups',
         sma_email_reports.SYSTEM_CAP: 'sma_system_capacity_scheduled',
         sma_email_reports.TLS_CONN: 'mga_tls_connections',
         sma_email_reports.VIRUS_TYPES: 'mga_virus_types',
         sma_email_reports.ADVANCED_MALWARE_PROTECTION: 'mga_advanced_malware_protection',
         sma_email_reports.ADVANCED_MALWARE_PROTECTION_FILE_ANALYSIS: 'mga_amp_file_analysis'
         }

    error_message = ''

    TABLE_COLUMNS_LINK_SELECTOR = "//a[contains(@href, 'showTableOptions')]"
    SECTION_EXPORT_LINK_SELECTOR = "//a[contains(@href, 'showTableOptions')]"

    # def get_keyword_names(self):
    # return [
    # 'configure_autodownload_for_browser',
    # 'wait_for_download',
    # ]

    def _convert_to_tuple_from_colon_separated_string(self, user_input):
        if isinstance(user_input, (str, unicode)):
            user_input = tuple([item.strip() for item in user_input.split(':')])
        else:
            raise ValueError('Argument \'%s\' should be string type.' % \
                             (user_input,))
        return user_input

    def _click_add_scheduled_report_button(self):
        self.click_button("//input[@title='Add Scheduled Report...']")

    def _click_add_archived_report_button(self):
        self.click_button("//input[@title='Generate Report Now...']")

    def _select_report_type(self, report_type):
        print '>>> report_type: %s' % report_type
        print '>>> report type: %s' % self._report_types[report_type]
        if report_type not in self._report_types.keys():
            raise guiexceptions.ConfigError("Invalid report type '%s'." % \
                                            (report_type))
        self.select_from_list('report_type', '%s' % \
                              (self._report_types[report_type],))
        # wait for a page load to happen or timeout expires.
        self.wait_until_page_loaded(60000)

    def _fill_report_title(self, title):
        self.input_text("//input[@id='report_title']", title)

    def _select_time_range(self, timerange):
        if timerange is None:
            return False

        time_range_types = {'last day': 'calendar_day',
                            'last week': 'calendar_week',
                            'last month': 'calendar_month',
                            'last year': 'calendar_year',
                            'num days': 'custom_day',
                            'num months': 'custom_month',
                            'timestamp': 'timestamp_day',
                            'day': 'current_day',
                            'week': 'current_week',
                            'month': 'current_month',
                            '30 days': 'current_month',
                            'quarter': 'current_quarter',
                            '90 days': 'current_quarter',
                            'yesterday': 'calendar_day',
                            'previous month': 'calendar_month',
                            'previous calendar month': 'calendar_month',
                            'custom': 'timestamp_day',
                            'custom range': 'timestamp_day'
                            }
        timerange = self._convert_to_tuple_from_colon_separated_string(timerange)
        if len(timerange) == 2:
            time_range = timerange[0]
            if (timerange[0] == 'num days'):
                num_days = timerange[1]
            else:
                num_days = None
            if (timerange[0] == 'num months'):
                num_months = timerange[1]
            else:
                num_months = None
        elif len(timerange) == 3:
            time_range = timerange[0]
            date1 = timerange[1]
            date2 = timerange[2]
        else:
            time_range = timerange[0]
            num_days = None
            num_months = None

        if time_range.lower() not in time_range_types.keys():
            raise guiexceptions.ConfigError("Invalid time range '%s'." % \
                                            (time_range))
        _time_locator1 = 'days_include'
        _time_locator2 = 'date_range'
        if int(self.get_matching_xpath_count("id('" + _time_locator1 + "')")) > 0:
            self.select_from_list(_time_locator1, '%s' % \
                                  (time_range_types[time_range.lower()],))
        elif int(self.get_matching_xpath_count("id('" + _time_locator2 + "')")) > 0:
            self.select_from_list(_time_locator2, '%s' % \
                                  (time_range_types[time_range.lower()],))
        else:
            raise guiexceptions.GuiValueError('Time Range control was not founds')
        if time_range.lower() == 'timestamp' or time_range.lower() == 'custom' or (time_range.lower())[:6] == 'custom':
            self._select_timestamp(date1, date2)
        else:
            if num_days is not None:
                if not num_days.isdigit():
                    raise guiexceptions.ConfigError(
                        "Invalid value '%s'. Should be positive int." % \
                        (num_days))
                self.input_text("//input[@id='custom_day']", num_days)

            if num_months is not None:
                if not num_months.isdigit():
                    raise guiexceptions.ConfigError(
                        "Invalid value '%s'. Should be positive int." % \
                        (num_months))
                self.input_text("//input[@id='custom_month']", num_months)

    def _select_report_format(self, reportformat):
        format_types = {'pdf': 'id=format_pdf',
                        'csv': 'id=format_csv'
                        }
        if reportformat not in format_types.keys():
            raise guiexceptions.ConfigError("Invalid format '%s'." % (reportformat))
        self._click_radio_button(format_types[reportformat])

    def _select_filtering(self, filtertype):
        filter_types = {'global': 'id=global',
                        'local': 'id=local'
                        }
        if filtertype not in filter_types.keys():
            raise guiexceptions.ConfigError("Invalid filter '%s'." % (filtertype))
        self._click_radio_button(filter_types[filtertype])

    def _select_outgoing_domain(self, domain):
        domain_types = {'server': 'id=data_source_cg_server',
                        'email_address': 'id=data_source_cg_address'
                        }
        if domain not in domain_types.keys():
            raise guiexceptions.ConfigError(
                "Invalid outgoing domain '%s'." % (domain))
        self._click_radio_button(domain_types[domain])

    def _select_report_schedule(self, schedule):
        schedule_types = {'daily': 'id=schedule_type_daily',
                          'weekly': 'id=schedule_type_weekly',
                          'monthly': 'id=schedule_type_monthly'}
        schedule = \
            self._convert_to_tuple_from_colon_separated_string(schedule)
        if len(schedule) == 4:
            schedule_type, time_h, time_m, day = schedule
        else:
            schedule_type, time_h, time_m = schedule
            day = None

        time_h_types = [('%02d' % (x)) for x in range(24)]
        time_h_types.append(None)
        time_m_types = ['00', '15', '30', '45', None]
        day_types = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                     'Thursday', 'Friday', 'Saturday', None]

        if schedule_type not in schedule_types.keys():
            raise guiexceptions.ConfigError(
                'Invalid report schedule type value \'%s\'.' % (schedule_type,))
        if time_h not in time_h_types:
            raise guiexceptions.ConfigError(
                'Invalid report schedule hour value \'%s\'.' % (time_h,))
        if time_m not in time_m_types:
            raise guiexceptions.ConfigError(
                'Invalid report schedule minutes value \'%s\'.' % (time_m,))
        if day not in day_types:
            raise guiexceptions.ConfigError(
                'Invalid report schedule day value \'%s\'. ' % (day,))
        if schedule_type is not None:
            self._click_radio_button(schedule_types[schedule_type])
        if time_h is not None:
            self.select_from_list('id=hour', '%s' % (time_h))
        if time_m is not None:
            self.select_from_list('id=minute', '%s' % (time_m))
        if day is not None:
            self.select_from_list('id=wday', '%s' % (day))

    def _fill_email_to(self, emails):
        if emails.lower() == 'off':
            self.input_text("//input[@id='recipients']", '')
        else:
            self.input_text("//input[@id='recipients']", emails)

    def _select_language(self, language):
        language = language.lower()
        language_types = {'deutsch': 'de-de',
                          'english': 'en-us',
                          'espanol': 'es',
                          'france': 'fr-fr',
                          'italian': 'it',
                          'japanese': 'ja',
                          'korean': 'ko',
                          'portuguese': 'pt-br',
                          'russian': 'ru',
                          'chinese': 'zh-cn',
                          'taiwan': 'zh-tw'
                          }
        if language not in language_types.keys():
            raise guiexceptions.ConfigError(
                'Invalid language %s requested' % language)
        self.select_from_list('id=lang', language_types[language])

    def _select_number_of_rows(self, number_of_rows):
        if not self._is_element_present("//select[@id='rows']"):
            return
        number_of_row_types = ['10', '20', '50', '100']
        if number_of_rows not in number_of_row_types:
            raise guiexceptions.ConfigError(
                "Invalid number of rows '%s'." % (number_of_rows))
        self.select_from_list('id=rows', '%s' % (number_of_rows))

    def _select_number_of_items(self, number_of_items):
        if not self._is_element_present("//select[@id='max_items']"):
            return
        number_of_items_types = range(2, 21, 1)
        if int(number_of_items) not in number_of_items_types:
            raise guiexceptions.ConfigError(
                "Invalid number of items '%s'." % (number_of_items))
        self.select_from_list('id=max_items', '%s' % (number_of_items))

    def _select_chart_data(self, charttype, row, type_dict):
        link = "//table[@class='layout']//tr[%d]//td[2]/a" % (row,)
        if charttype.lower() == 'none':
            return
        if charttype not in type_dict.keys():
            raise guiexceptions.ConfigError(
                "Invalid chart data type '%s'." % (charttype))

        radio_button_link = "//input[@id='chart_option_dlg_%s']" % \
                            (type_dict[charttype])
        self.click_element(link, "don't wait")
        self._click_radio_button(radio_button_link)
        self.click_element("//span[@class='button-group']/button[2]",
                           "don't wait")

    def _get_type_dicts(self, report_type):

        if report_type in [sma_web_reports.USERS, sma_web_reports.WEB_SITES,
                           sma_web_reports.URL_CAT, sma_web_reports.WBRS_FILTERS]:
            return (self._report_type_to_chart_data[report_type],
                    self._report_type_to_chart_data[report_type],)
        if report_type == sma_web_reports.APP_VISIBILITY:
            return (self._available_avc_chart_types,
                    self._available_avc_name_chart_types)
        if report_type == sma_web_reports.ANTIMALWARE:
            return (self._available_amv_chart_categories,
                    self._available_amv_chart_threats)
        if report_type == sma_web_reports.MALWARE_RISK:
            return (self._available_client_activity_chart,
                    self._available_client_activity_traffic)
        if report_type == sma_web_reports.L4TM:
            return (self._available_traffic_monitor_by_user_chart,
                    self._available_traffic_monitor_by_host_chart)

    def _select_chart_display_data(self, report_type, data):

        l_type_dict, r_type_dict = self._get_type_dicts(report_type)
        data = self._convert_to_tuple_from_colon_separated_string(data)
        if len(data) == 2:
            chart_left, chart_right = data
        else:
            raise guiexceptions.ConfigError('')
        if chart_left is not None:
            self._select_chart_data(chart_left, 2, l_type_dict)
        if chart_right is not None:
            self._select_chart_data(chart_right, 3, r_type_dict)

    def _select_sort_column(self, report_type, columns):
        typical_col_types = \
            {'bw used': 'Bandwidth Used',
             'time spent': 'Time Spent',
             'total completed': 'Transactions Completed',
             'total blocked': 'Transactions Blocked',
             'transactions total': 'Total Transactions'
             }
        avc_col_types = \
            {'bw used': 'Bandwidth Used',
             'completed': 'Transactions Completed',
             'blocked': 'Transactions Blocked by Application',
             'total': 'Total Transactions'
             }
        amw_col_types = \
            {'total monitored': 'Transactions Monitored',
             'total blocked': 'Transactions Blocked',
             'total detected': 'Transactions Detected'
             }
        client_activity_trans_col_types = \
            {'total monitored': 'Malware Transactions Monitored',
             'total blocked': 'Malware Transactions Blocked',
             'total detected': 'Total Malware Transactions Detected'
             }
        client_activity_connections_col_types = \
            {'total monitored': 'Malware Connections Monitored',
             'total blocked': 'Malware Connections Blocked',
             'total detected': 'Total Malware Connections Detected'
             }
        wbrs_col_types = \
            {'block': 'Block',
             'malware detected': 'Scan Further: Malware Detected',
             'clean': 'Scan Further: Clean',
             'allow': 'Allow'
             }
        l4_mon_col_types = \
            {'total monitored': 'Malware Connections Monitored',
             'total blocked': 'Malware Connections Blocked',
             'total detected': 'Total Malware Connections Detected'
             }
        avg_usage_and_performance_col_types = \
            {'cpu used': 'CPU Usage %',
             'response time': 'Response Time (ms)',
             'proxy buffer memory': 'Proxy Buffer Memory (Bytes)',
             'transactions per sec': 'Transactions Per Second',
             'connection out': 'Connections Out',
             'bw out': 'Bandwidth Out (Bytes Per Second)'
             }
        app_name_col_types = \
            {'bw used': 'Bandwidth Used',
             'completed': 'Transactions Completed',
             'blocked': 'Transactions Blocked',
             'total': 'Transactions Total'
             }
        category_name_col_types = \
            {'bw used': 'Bandwidth Used',
             'time spent': 'Time Spent',
             'total completed': 'Transactions Completed',
             'total blocked': 'Transactions Blocked',
             'transactions total': 'Transactions Total'
             }
        dlp_col_types = \
            {'low': 'Low',
             'medium': 'Medium',
             'high': 'High',
             'critical': 'Critical',
             'total': 'Total',
             'delivered enc': 'Delivered (encrypted)',
             'delivered clear': 'Delivered (clear)',
             'dropped': 'Dropped'
             }
        outgoing_dest_status_col_types = \
            {'host status': 'Latest Host Status',
             'active': 'Active Recipients',
             'connections out': 'Connections Out',
             'delivered': 'Delivered Recipients',
             'soft': 'Soft Bounced',
             'hard': 'Hard Bounced'
             }
        threat_det_col_types = \
            {'total': 'Total Messages'
             }
        pyvirus_outbreaks_col_types = \
            {'outbreak': 'Outbreak ID',
             'first seen': 'First Seen Globally',
             'time': 'Protection Time',
             'messages': 'Quarantined Messages'
             }
        outgoing_dest_detail_col_types = \
            {'spam': 'Spam Detected',
             'virus': 'Virus Detected',
             'stopped': 'Stopped by Content Filter',
             'threat': 'Total Threat',
             'clean': 'Clean',
             'total processed': 'Total Processed',
             'hard': 'Hard Bounced',
             'delivered': 'Delivered',
             'total delivered': 'Total Messages Delivered'
             }
        senders_detail_col_types = \
            {'spam': 'Spam Detected',
             'virus': 'Virus Detected',
             'stopped': 'Stopped by Content Filter',
             'threat': 'Total Threat',
             'clean': 'Clean',
             'total': 'Total Messages'
             }
        tls_connections_details_col_types = \
            {'req. failed': 'TLS Req. Failed',
             'req. success': 'TLS Req. Success',
             'pref. failed': 'TLS Pref. Failed',
             'pref success': 'TLS Pref. Success',
             'total': 'Total TLS Connections',
             'unencrypted': 'Unencrypted Connections',
             'messages': 'Messages by TLS'
             }
        virus_types_detail_col_types = \
            {'incoming': 'Incoming Messages',
             'outgoing': 'Outgoing Messages',
             'total infected': 'Total Infected Messages'
             }
        message_attempt_to_be_forwarded_app_col_types = \
            {'MFS':'Message Forwarding Success',
             'MFF':'Message Forwarding Failure'
             }
        columns = \
            self._convert_to_tuple_from_colon_separated_string(columns)

        if report_type == sma_web_reports.USERS:
            elements = ('sort_columns[wsa_users_users_table]',)
            self._select_sort_column_from_list(typical_col_types,
                                               elements[0], columns[0])
        elif report_type == sma_web_reports.WEB_SITES:
            elements = ('sort_columns[wsa_web_sites_domains_matched]',)
            self._select_sort_column_from_list(typical_col_types,
                                               elements[0], columns[0])
        elif report_type == sma_web_reports.URL_CAT_EXTENDED:
            elements = ('sort_columns[wsa_top_n_categories_top_n_0]',)
            self._select_sort_column_from_list(category_name_col_types,
                                               elements[0], columns[0])
        elif report_type == sma_web_reports.WBRS_FILTERS:
            elements = (
                'sort_columns[wsa_web_reputation_filters_wbrs_filters]',)
            self._select_sort_column_from_list(wbrs_col_types,
                                               elements[0], columns[0])
        elif report_type == sma_web_reports.URL_CAT:
            elements = ('sort_columns[wsa_url_categories_top_categories]',)
            self._select_sort_column_from_list(typical_col_types,
                                               elements[0], columns[0])
        elif report_type == sma_web_reports.APP_VISIBILITY:
            elements = ('sort_columns[wsa_applications_types_total]',
                        'sort_columns[wsa_applications_total]')
            self._select_sort_column_from_list(avc_col_types,
                                               elements[0], columns[0])
            self._select_sort_column_from_list(avc_col_types,
                                               elements[1], columns[1])
        elif report_type == sma_web_reports.TOP_APP_TYPES:
            elements = ('sort_columns[wsa_top_n_applications_top_n_0]',)
            self._select_sort_column_from_list(app_name_col_types,
                                               elements[0], columns[0])
        elif report_type == sma_web_reports.ANTIMALWARE:
            elements = ('sort_columns[wsa_malware_malware_categories]',
                        'sort_columns[wsa_malware_malware_threats]')
            self._select_sort_column_from_list(amw_col_types,
                                               elements[0], columns[0])
            self._select_sort_column_from_list(amw_col_types,
                                               elements[1], columns[1])
        elif report_type == sma_web_reports.MALWARE_RISK:
            elements = (
                'sort_columns[wsa_client_activity_top_at_risk_clients]',
                'sort_columns[wsa_client_activity_l4_tm_client_ips]')
            self._select_sort_column_from_list(
                client_activity_trans_col_types,
                elements[0], columns[0])
            self._select_sort_column_from_list(
                client_activity_connections_col_types,
                elements[1], columns[1])
        elif report_type == sma_web_reports.L4TM:
            elements = (
                'sort_columns[wsa_l4_traffic_monitor_l4_tm_client_ips]',
                'sort_columns[wsa_l4_traffic_monitor_malware_ports_detected]',
                'sort_columns[wsa_l4_traffic_monitor_top_l4_tm_sites]')
            self._select_sort_column_from_list(l4_mon_col_types,
                                               elements[0], columns[0])
            self._select_sort_column_from_list(l4_mon_col_types,
                                               elements[1], columns[1])
            self._select_sort_column_from_list(l4_mon_col_types,
                                               elements[2], columns[2])
        elif report_type == sma_web_reports.SYSTEM_CAP_OVERVIEW:
            elements = (
                'sort_columns[wsa_sma_system_capacity_sma_system_capacity]',)
            self._select_sort_column_from_list(
                avg_usage_and_performance_col_types,
                elements[0], columns[0])
        elif report_type == sma_email_reports.DLP_INCIDENT:
            elements = (
                'sort_columns[mga_dlp_incident_summary_dlp_incident_details]',)
            self._select_sort_column_from_list(dlp_col_types,
                                               elements[0], columns[0])
        elif report_type == sma_email_reports.DELIVERY:
            elements = (
                'sort_columns[mga_outgoing_delivery_status_status_table]',)
            self._select_sort_column_from_list(outgoing_dest_status_col_types,
                                               elements[0], columns[0])
        elif report_type == sma_email_reports.VOF:
            elements = (
                'sort_columns[mga_virus_outbreaks_scheduled_threat_details]',
                'sort_columns[mga_virus_outbreaks_scheduled_outbreak_details]')
            self._select_sort_column_from_list(threat_det_col_types,
                                               elements[0], columns[0])
            self._select_sort_column_from_list(pyvirus_outbreaks_col_types,
                                               elements[1], columns[1])
        elif report_type == sma_email_reports.OUT_DESTINATIONS:
            elements = (
                'sort_columns[mga_destination_domains_virus_types_detail]',)
            self._select_sort_column_from_list(outgoing_dest_detail_col_types,
                                               elements[0], columns[0])
        elif report_type == sma_email_reports.OUT_DOMAIN_SENDERS:
            elements = ('sort_columns[mga_internal_senders_sender_detail]',)
            self._select_sort_column_from_list(senders_detail_col_types,
                                               elements[0], columns[0])
        elif report_type == sma_email_reports.TLS_CONN:
            elements = (
                'sort_columns[mga_tls_connections_received_tls_detail]',
                'sort_columns[mga_tls_connections_sent_tls_detail]')
            self._select_sort_column_from_list(
                tls_connections_details_col_types,
                elements[0], columns[0])
            self._select_sort_column_from_list(
                tls_connections_details_col_types,
                elements[1], columns[1])
        elif report_type == sma_email_reports.VIRUS_TYPES:
            elements = ('sort_columns[mga_virus_types_virus_types_detail]',)
            self._select_sort_column_from_list(virus_types_detail_col_types,
                                               elements[0], columns[0])
        elif report_type == email_reports.APP:
	       elements = ('sort_columns[mga_advanced_phishing_protection_advanced_phishing_protection_summary_table]',)
	       self._select_sort_column_from_list(message_attempt_to_be_forwarded_app_col_types,
				               elements[0], columns[0])

    def _select_sort_column_from_list(self, type_dict, locator, label):
        if label.lower() == 'none':
            return
        if label is not None:
            self.select_from_list(
                "//select[@name='%s']" % (locator,),
                '%s' % (type_dict[label],))

    def _get_report_row_index(self, name, col):
        report_table = '//table[@class="cols"]'
        table_rows = self.get_matching_xpath_count(
            '%s/tbody/tr' % (report_table,))
        for i in xrange(2, int(table_rows) + 1):
            report_name = self.get_text('%s/tbody/tr[%s]/td[%s]' %
                                        (report_table, i, col)).split(' \n')[0]
            if name == report_name:
                return i
        return None

    def _click_deliver_button(self):
        self.click_button("//input[@value='Deliver This Report']")

    def _click_edit_report_link(self, name):
        cell_id = '//table[@class="cols"]//tr[%s]//td[2]/a'

        row = self._get_report_row_index(name, 2)
        if row is None:
            raise guiexceptions.GuiValueError('Report "%s"' % (name,))
        self.click_link(cell_id % (row))

    def _click_delete_button(self):
        self.click_button("//input[@value='Delete']", "don't wait")
        self.click_button("//button[text()='Delete']")

    def _check_for_deletion(self, name, name_col, check_col):
        cell_id = '//table[@class="cols"]//tr[%s]//td[%s]/input'

        row = self._get_report_row_index(name, name_col)
        if row is None:
            raise guiexceptions.GuiValueError('Report "%s"' % (name,))
        self.click_element(cell_id % (row, check_col), "don't wait")

    def _set_archive_setting(self, setting):
        archive_checkbox = "//input[@name='archive']"
        if setting not in ['yes', 'no']:
            raise guiexceptions.ConfigError(
                'Invalid archive setting \'%s\'.Should be \'yes\' or \'no\'.' \
                % (setting,))
        if setting.lower() == 'yes':
            self.select_checkbox(archive_checkbox)
        else:
            self.unselect_checkbox(archive_checkbox)

    def _select_timestamp(self, start_date, end_date):
        start_date_input = "//input[@id='from_date']"
        end_date_input = "//input[@id='end_date']"
        start_time = "//select[@id='from_time']"
        end_time = "//select[@id='end_time']"
        date = "//a[text()='15']"
        try:
            start_date = time.strptime(start_date, '%d %b %Y %H')
            end_date = time.strptime(end_date, '%d %b %Y %H')
        except ValueError:
            raise ('Incorrect time range value: %s, %s.' % \
                   (start_date, end_date))
        if start_date > end_date:
            raise \
                guiexceptions.GuiValueError('Incorrect time range %s, %s.' + \
                                            'first date should be less than second date.' % \
                                            (start_date, end_date))
        # used trick: start and end date passed into hidden values instead
        # using calendar stuff.

        self.click(start_date_input)
        self.click(date)

        # if you see errors related to invisible elements -
        # this should be changed to
        #
        # start_date_input_id = 'from_date'
        # self._set_input_value_with_javascript(start_date_input_id,
        #               time.strftime('%d %b %Y', start_date))

        self.input_text(start_date_input,
                        time.strftime('%d %b %Y', start_date))

        self.click(end_date_input)
        self.click(date)

        # if you see errors related to invisible elements -
        # same as above
        self.input_text(end_date_input, time.strftime('%d %b %Y', end_date))

        self.select_from_list(start_time, time.strftime('%H', start_date))
        self.select_from_list(end_time, time.strftime('%H', end_date))
        self.click_button("//button[text()='Save']")

    def _get_report_type(self):
        reporttype = self.get_value("//input[@name='report_type']")
        return [k for k, v in self._report_types.iteritems() if v == reporttype][0]

    def _show_all(self):
        if self._is_element_present('//select[@id="type_report"]'):
            try:
                self.select_from_list('//select[@id="type_report"]', 'All')
            except Exception:
                self.select_from_list('//select[@id="type_report"]', 'all')

    def _select_all_reports(self):
        self.click_element("//input[@name='del_0']", "don't wait")

    def _fill_report_data(self, report_type, title, report_format, time_range,
                          schedule, email_to, num_of_rows, chart_data,
                          sort_col, reportfilter, language=None):

        if report_type is not None:
            self._select_report_type(report_type)
        else:
            report_type = self._get_report_type()

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

        if num_of_rows is not None and \
                (report_type == 'top url categories - extended' or
                 report_type == 'top application types - extended'):
            self._select_number_of_items(num_of_rows)
        elif num_of_rows is not None:
            self._select_number_of_rows(num_of_rows)

        if schedule is not None:
            self._select_report_schedule(schedule)

        if email_to is not None:
            self._fill_email_to(email_to)

        if reportfilter is not None:
            self._select_filtering(reportfilter)

        if language is not None:
            self._select_language(language)

    def _fill_archived_report_data(self, report_type, title, report_format,
                                   time_range, email_to, archive, num_of_rows,
                                   chart_data, sort_col, reportfilter, language=None):

        self._fill_report_data(report_type, title, report_format, time_range,
                               None, None, num_of_rows, chart_data, sort_col,
                               reportfilter, language)
        if archive is not None:
            self._set_archive_setting(archive)

        if archive is not None and archive.lower() == 'no' and \
                email_to is None:
            guiexceptions.ConfigError(
                'You have to specify at least one option: ' + \
                'either \'archive\' or \'email to\'.')

        if email_to is not None:
            self.select_checkbox("//input[@id='deliver']")
            self._fill_email_to(email_to)

    def _select_report_generation(self, report_generation, file_to_upload,
                                  domains, emails):
        if report_generation is None:
            return

        if report_generation == 'configfile':
            self._click_radio_button(
                "//input[@id='gen_opt_upload_file']")
            available_files = self.get_list_items(
                "//select[@id='file_server']")
            if file_to_upload is not None:
                if file_to_upload in available_files:
                    self._click_radio_button(
                        "//input[@id='load_type_server']")
                    self.select_from_list('file_server', '%s' % \
                                          (file_to_upload))
                else:
                    self._click_radio_button(
                        "//input[@id='load_type_local']")
                    self.input_text(
                        "//input[@id='local_file']", file_to_upload)
        elif report_generation == 'individual':
            self._click_radio_button("//input[@id='gen_opt_enter_data']")
            if domains is not None:
                if domains.lower() == 'off':
                    self.input_text("//input[@id='domains']", '')
                else:
                    self.input_text("//input[@id='domains']", domains)
            if emails is not None:
                if emails.lower() == 'off':
                    self.input_text(
                        "//input[@id='gen_opt_recipients']", '')
                else:
                    self.input_text(
                        "//input[@id='gen_opt_recipients']", emails)
        else:
            raise guiexceptions.GuiValueError(
                'Unknown "%s" report generation option.' % \
                (report_generation,))

    def _select_logo(self, logo):
        if logo is None:
            return
        elif logo.lower() == 'cisco':
            self._click_radio_button("//input[@id='default_logo_id']")
        else:
            self._click_radio_button("//input[@id='custom_logo_id']")
            self.input_text("//input[@id='custom_logo']", logo)

    def _check_reports_availability(self):
        no_scheduled_msg = 'There are no Scheduled Reports defined.'
        no_archived_msg = 'There are no reports to display.'
        report_exist = False
        if self._is_text_present(no_scheduled_msg):
            self._info(no_scheduled_msg)
        elif self._is_text_present(no_archived_msg):
            self._info(no_archived_msg)
        else:
            report_exist = True
        return report_exist

    def _get_reports_info(self, report_class, report_type='email'):
        REPORT_INFO_CELL = lambda row, title_column: REPORTS_TABLE % \
                                                     (row, title_column)
        REPORTS_TABLE = "//table[@class='cols']/tbody/tr[%s]/td[%s]"

        reports = []
        start_row = 2
        if self._check_reports_availability():
            num_of_rows = int(self.get_matching_xpath_count(
                REPORT_INFO_CELL('*', 1)))

            if report_type == 'email':
                columns_order = report_class._email_columns_order
            else:
                columns_order = report_class._web_columns_order

            for row in xrange(start_row, num_of_rows + start_row):
                report_info = {}
                for column, column_name in enumerate(columns_order, 1):
                    report_info[column_name] = self.get_text(
                        REPORT_INFO_CELL(row, column))
                reports.append(str(report_class(**report_info)))

        return reports

    def _make_section_loc(self, section_path, exact=True):
        self._debug("Prepearing section locatoor for section: %s" % (section_path,))
        if exact:
            text_selection = "(normalize-space(text())="
        else:
            text_selection = "contains(text(),"
        section_path_list = section_path.split(" > ")
        section_loc = ""
        section_loc += "//dl[contains(@class,'header') or contains(@class,'box')]"
        section_loc += "/dt/descendant-or-self::*[%s'%s')]" % (text_selection, section_path_list[0])
        section_loc += "/ancestor-or-self::dt"
        if len(section_path_list) == 1:
            section_loc += "//following-sibling::dd"
            return [section_loc]

        # search subsection in 'dashboard' tables
        section_loc1 = section_loc
        section_loc1 += "/following-sibling::dd"
        section_loc1 += "//table[@class='dashboard']//*[%s'%s')]" % (text_selection, section_path_list[1])
        section_loc1 += "/ancestor::table[@class='dashboard']/following-sibling::table"

        # search subsection in the same parent row
        section_loc2 = section_loc
        section_loc2 += "/ancestor::tr[1]"
        section_loc2 += "//dl[contains(@class,'header') or contains(@class,'box')]"
        section_loc2 += "/dt/descendant-or-self::*[%s'%s')]" % (text_selection, section_path_list[1])
        section_loc2 += "/ancestor-or-self::dt/following-sibling::dd"

        # search subsection in next rows
        section_loc3 = section_loc
        section_loc3 += "/ancestor::tr[1]/following-sibling::tr"
        section_loc3 += "//dl[contains(@class,'header') or contains(@class,'box')]"
        section_loc3 += "/dt/descendant-or-self::*[%s'%s')]" % (text_selection, section_path_list[1])
        section_loc3 += "/ancestor-or-self::dt[1]/following-sibling::dd"
        section_loc3 = "(%s)[1]" % section_loc3
        return [section_loc1, section_loc2, section_loc3]

    def _set_element_id(self, locator):
        """ Assign id to the element and return xpath to search by id."""
        if int(self.get_matching_xpath_count(locator + "/self::*[@id]")) > 0:
            _id = self.get_element_attribute(locator + "@id")
        else:
            _id = time.time()
            self.assign_id_to_element(locator, _id)
        return "//*[@id='%s']" % _id

    def _find_section_area(self, section_path, timeout=60):
        """ Find table by indicating section name and parent headers as path. """
        self._debug("Searching section: %s" % (section_path,))
        sections = section_path.split(" > ")
        section_locs = self._make_section_loc(section_path, True) + \
                       self._make_section_loc(section_path, False)

        section_loc = None
        _timer_start = time.time()
        while ((time.time() - _timer_start) < timeout) \
                and (section_loc is None):
            for section_loc_i in section_locs:
                section_count = int(self.get_matching_xpath_count(section_loc_i))
                self._debug("Search by locator: %s gave %s items" % (section_loc_i, section_count))
                if section_count > 0:
                    section_loc = "(%s)[1]" % (section_loc_i,)
                    return self._set_element_id(section_loc)
            time.sleep(3)

        return section_loc

    def _find_table(self, section_path, section_loc=None, timeout=60):
        """ Find table by indicating section name and parent headers as path. """
        if section_loc is None:
            table_loc = self._find_section_area(section_path)
        else:
            table_loc = section_loc
        if table_loc is None:
            return None
        tables_count = 0
        _timer_start = time.time()
        while (time.time() - _timer_start) < timeout:
            _table_loc = table_loc + "//thead/parent::table"
            tables_count = int(self.get_matching_xpath_count(_table_loc))
            if tables_count == 0:
                _table_loc = table_loc + "//tr[contains(@class, 'header')]/parent::table"
                tables_count = int(self.get_matching_xpath_count(_table_loc))
            if tables_count == 0:
                _table_loc = table_loc + "//tr[contains(@class, 'header')]/parent::tbody/parent::table"
                tables_count = int(self.get_matching_xpath_count(_table_loc))
            if tables_count == 0:
                _table_loc = table_loc + "/table"
                tables_count = int(self.get_matching_xpath_count(_table_loc))
            if tables_count == 0:
                time.sleep(1)
            else:
                break
        if tables_count > 0:
            return _table_loc
        else:
            return None

    def _get_table_head_loc(self, table_loc):
        """ Return list of headesr in a table, specified by table locator. """
        # trying to find table with thead
        table_head = table_loc + "/thead"
        table_head_count = int(self.get_matching_xpath_count(table_head))
        table_head_rows_count = 0
        if table_head_count > 0:
            table_head_rows_count = int(self.get_matching_xpath_count(table_head + "/tr"))
        else:
            # trying to find table with headers in rows
            table_head_rows_count = int(self.get_matching_xpath_count(table_loc + "//tr[contains(@class, 'header')]"))
            table_head = table_loc + "//tr[contains(@class, 'header')]/parent::*"

        return [table_head, table_head_rows_count]

    def _get_table_headers(self, table_loc):
        """ Return list of headesr in a table, specified by table locator. """
        head_data = []
        rowspan_numbers = []

        table_head, table_head_rows_count = self._get_table_head_loc(table_loc)

        # get table headers (first row)
        _header_th_count = int(self.get_matching_xpath_count(table_head + "/tr[1]/th"))
        self._debug("_header_th_count: %s" % _header_th_count)
        for _th in range(1, 1 + _header_th_count):
            # prepare getting value
            _th_loc = table_head + "/tr[1]/th[" + str(_th) + "]"
            self._debug("_th_loc: %s" % _th_loc)
            # check visibility
            _visible = self._is_visible(_th_loc)
            # get column span
            _th_colspan = 1
            if int(self.get_matching_xpath_count(_th_loc + "/self::*[@colspan]")) > 0:
                _th_colspan = int(self.get_element_attribute(_th_loc + "@colspan"))
            # get row span
            _th_rowspan = 1
            if int(self.get_matching_xpath_count(_th_loc + "/self::*[@rowspan]")) > 0:
                _th_rowspan = int(self.get_element_attribute(_th_loc + "@rowspan"))
            # get value
            if _visible:
                _th_value = self.get_text(_th_loc)
            else:
                _th_value = None
            for _data_index in range(_th_colspan):
                rowspan_numbers.append(_th_rowspan)
                head_data.append(_th_value)

        # loop through other rows to have unique headers in the list
        for th_tr in range(2, 1 + table_head_rows_count):
            _header_th_count = int(self.get_matching_xpath_count(table_head + "/tr[" + str(th_tr) + "]/th"))
            self._debug("_header_th_count: %s" % _header_th_count)
            _cell_index = 0
            # loop through header TH elements
            for _th in range(1, 1 + _header_th_count):
                # skip first cells missed by row spanning
                while rowspan_numbers[_cell_index] > 1:
                    rowspan_numbers[_cell_index] -= 1
                    _cell_index += 1
                    self._debug("_cell_index: %s" % _cell_index)
                # prepare getting value
                _th_loc = table_head + "/tr[" + str(th_tr) + "]/th[" + str(_th) + "]"
                self._debug("_th_loc: %s" % _th_loc)
                # check visibility
                _visible = self._is_visible(_th_loc)
                # get column span
                _th_colspan = 1
                if int(self.get_matching_xpath_count(_th_loc + "/self::*[@colspan]")) > 0:
                    _th_colspan = int(self.get_element_attribute(_th_loc + "@colspan"))
                # get row span
                _th_rowspan = 1
                if int(self.get_matching_xpath_count(_th_loc + "/self::*[@rowspan]")) > 0:
                    _th_rowspan = int(self.get_element_attribute(_th_loc + "@rowspan"))
                # get value
                _th_value = self.get_text(+_th_loc)
                for _data_index in range(_cell_index, _cell_index + _th_colspan):
                    rowspan_numbers[_data_index] = _th_rowspan
                    if _visible:
                        head_data[_data_index] += " " + _th_value
                    else:
                        head_data[_data_index] = None
                _cell_index += _th_colspan

        return head_data

    def _get_table_header_index(self, table_loc, header):
        """ Return index of cells for specified header. """
        table_head, table_head_rows_count = self._get_table_head_loc(table_loc)
        if table_head_rows_count == 1:
            _header_loc = table_head + "/tr[1]/th/descendant-or-self::*[normalize-space(text())='" + header + "']"
            _header_count = int(self.get_matching_xpath_count(_header_loc))
            if _header_count < 1:
                return None
            return int(
                self.get_matching_xpath_count(_header_loc + "/ancestor-or-self::th[1]/preceding-sibling::th")) + 1
        else:
            head_list = self._get_table_headers(table_loc)
            try:
                return head_list.index(header) + 1
            except:
                return None

    def _get_table_rows_loc(self, table_loc):
        """ Return locator for table rows. """
        table_body = table_loc + "/tbody[not(contains(@style,'display: none'))]"
        if int(self.get_matching_xpath_count(table_body)) > 0:
            table_rows = table_body + "/tr[not(contains(@class, 'header'))]"
        else:
            table_rows = table_loc + "//tr[contains(@class, 'header')]/parent::*/tr[not(contains(@class, 'header'))]"

        return table_rows

    def _get_table_values(self, tables_loc):
        """ Return list of values in a table or tables, specified by table locator. """
        _prev_speed = self.set_selenium_speed(0)

        tables_list = []
        tables_count = int(self.get_matching_xpath_count(tables_loc))
        for table_num in range(1, 1 + tables_count):
            table_list = []
            table_loc = "(" + tables_loc + ")[" + str(table_num) + "]"

            _new_id = time.time()
            self.assign_id_to_element(table_loc, _new_id)
            table_loc = "//*[@id='%s']" % _new_id

            head_list = self._get_table_headers(table_loc)
            cleared_head_list = list(head_list)
            for i in range(cleared_head_list.count(None)):
                cleared_head_list.remove(None)

            table_list.append(cleared_head_list)

            # getting table body for getting data
            table_rows = self._get_table_rows_loc(table_loc)

            # going through rows
            tr_count = int(self.get_matching_xpath_count(table_rows))
            for tr_num in range(1, 1 + tr_count):
                row_loc = "(" + table_rows + ")[" + str(tr_num) + "]"
                if not self._is_visible(row_loc + "/*[1]"):
                    continue
                row_list = []
                td_count = int(self.get_matching_xpath_count(row_loc + "/*"))
                for td_num in range(1, 1 + td_count):
                    td_loc = row_loc + "/*[" + str(td_num) + "]"
                    # skip invisible
                    if head_list[td_num - 1] is None:
                        continue
                    td_value = self.get_text(td_loc)
                    row_list.append(td_value)
                table_list.append(row_list)
            tables_list.append(table_list)

        self.set_selenium_speed(_prev_speed)

        # parsing case of one table found
        if len(tables_list) == 1:
            return tables_list[0]
        else:
            return tables_list

    def _get_table_row_index(self, table_loc, row_name):
        """ Return index of cells for specified header. """
        # getting table body for getting data
        table_rows = self._get_table_rows_loc(table_loc)

        _row_loc = table_rows + "/*[1]/descendant-or-self::*[normalize-space(text())='" + row_name + "']"
        tr_count = int(self.get_matching_xpath_count(_row_loc))
        if tr_count < 1:
            return None
        return int(self.get_matching_xpath_count(
            _row_loc + "/ancestor-or-self::tr[1]/preceding-sibling::tr[not(contains(@class, 'header'))]")) + 1

    def _get_table_cell_loc(self, table_loc, row_name, header=None):
        table_rows = self._get_table_rows_loc(table_loc)
        _row = self._get_table_row_index(table_loc, row_name)
        if header is None:
            _col = 1
        else:
            _col = self._get_table_header_index(table_loc, header)
        self._debug("_row: %s" % _row)
        self._debug("_col: %s" % _col)
        return "(" + table_rows + ")[" + str(_row) + "]/*[" + str(_col) + "]"

    def _get_table_cell_value(self, table_loc, row_name, header=None):
        _cell_loc = self._get_table_cell_loc(table_loc, row_name, header)
        return self.get_text(_cell_loc)

    def _convert_tuple_to_table(self, user_input):
        """ Convert tuple with strings of comma-separated pairs ('key:value') to
        multidimentional list. """
        _first_column_name = None
        _headers = []
        _table = []
        _row = []
        for _user_string in user_input:
            _user_string = _user_string.replace("\,", "&#044;")
            _user_string = _user_string.replace("\:", "&#058;")
            _array = _user_string.split(',')
            for _pair in _array:
                _pos = _pair.find(':')
                if _pos < 0:
                    _name = ''
                    _value = _pair.strip()
                    if _value == '':
                        continue
                elif _pos == 0:
                    _name = ''
                    _value = _pair[1:].strip()
                else:
                    _name = _pair[0:_pos].strip()
                    _value = _pair[_pos + 1:].strip()

                _name = _name.replace("&#044;", ",")
                _name = _name.replace("&#058;", ":")
                _value = _value.replace("&#044;", ",")
                _value = _value.replace("&#058;", ":")

                if _first_column_name is None:
                    _first_column_name = _name
                elif _name == _first_column_name:
                    _table.append(list(_row))
                    _row = map(lambda x: '', range(len(_headers)))
                if _name not in _headers:
                    _headers.append(_name)
                    _row.append(_value)
                else:
                    _row[_headers.index(_name)] = _value
        _table.append(list(_row))
        _table.insert(0, _headers)
        self._debug(_table)
        return _table

    def _convert_str_to_time(self, str_time):
        time_value_time = None
        try:
            time_value_time = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        except:
            pass
        if time_value_time is None:
            try:
                time_value_time = time.strptime(str_time, "%Y %m %d %H")
            except:
                pass
        if time_value_time is None:
            try:
                time_value_time = time.strptime(str_time, "%Y %m %d %H %M")
            except:
                pass
        if time_value_time is None:
            try:
                time_value_time = time.strptime(str_time, "%d %b %Y %H:%M")
            except:
                pass
        if time_value_time is None:
            try:
                time_value_time = time.strptime(str_time, "%d %b %Y %H:%M  (GMT)")
            except:
                pass
        if time_value_time is not None:
            time_value_time = time.mktime(time_value_time)
        self._debug("time_value_time")
        self._debug(str_time)
        self._debug(time_value_time)

        return time_value_time

    def _compare_times(self, time1, time2, time_precision=None):
        """Compares two strings with datetime and return True if equal.
        """
        time1_value_time = self._convert_str_to_time(time1)
        time2_value_time = self._convert_str_to_time(time2)
        if time1_value_time is not None and time2_value_time is not None:
            self._debug("time difference")
            self._debug(time1_value_time - time2_value_time)
            if time_precision is not None:
                return abs(time1_value_time - time2_value_time) < time_precision
            else:
                return time1_value_time == time2_value_time
        else:
            return False

    def _compare_numbers(self, num1, num2, number_precision=None):
        self._debug("num1=%s" % num1)
        self._debug("num2=%s" % num2)
        num1_value_num = None
        try:
            num1_value_num = float(num1)
        except:
            pass
        if num1_value_num is None:
            m = re.search("[^\-\d\.]{0,2}(\-?\d+\.?\d*)[^\-\d\.]{0,2}", str(num1))
            if m is not None:
                num1_value_num = (m.groups())[0]
                self._debug("num1_value_num=%s" % num1_value_num)
                try:
                    num1_value_num = float(num1_value_num)
                except:
                    pass
        self._debug("num1_value_num=%s" % num1_value_num)
        num2_value_num = None
        try:
            num2_value_num = float(num2)
        except:
            pass
        if num2_value_num is None:
            m = re.search("[^\-\d\.]{0,2}(\-?\d+\.?\d*)[^\-\d\.]{0,2}", str(num2))
            if m is not None:
                num2_value_num = (m.groups())[0]
                self._debug("num2_value_num=%s" % num2_value_num)
                try:
                    num2_value_num = float(num2_value_num)
                except:
                    pass
        self._debug("num2_value_num=%s" % num2_value_num)
        if (num1_value_num is None) and (num2_value_num is not None) and len(num1) > 0:
            _first_char = str(num1)[0]
            if _first_char == '=' or _first_char == '>' or _first_char == '<':
                try:
                    return eval(str(num2_value_num) + str(num1))
                except:
                    return False
        if (num1_value_num is not None) and (num2_value_num is not None):
            self._debug("number difference")
            self._debug(num1_value_num - num2_value_num)
            if number_precision is not None:
                return abs(num1_value_num - num2_value_num) < number_precision
            else:
                return num1_value_num == num2_value_num

        return False

    def _simple_match(self, input_string, find_string):
        _find_string = re.sub(r'([\.\^\$\+\{\}\[\]\\\|\(\)])', r'\\\1', find_string)
        _find_string = re.sub(r'(\*)', r'.*', _find_string)
        _find_string = re.sub(r'(\\\\\.\*?)', r'\*', _find_string)
        _find_string = re.sub(r'(\?)', r'.{1}', _find_string)
        _find_string = re.sub(r'(\\\\\.\{1\})', r'\?', _find_string)
        _find_string = '^' + _find_string + '$'
        return not (re.match(_find_string, input_string) is None)

    def _compare_tables(self, exp_table, fnd_table, section_name=None,
                        number_precision=None, time_precision=None, data_in_first_column=True):
        """Compares two-dimentional arrays (expected table and found table) and
        returns message for reporting errors.
        """
        self._debug("Compare tables: section_name")
        self._debug(section_name)
        self._debug("Compare tables: exp_table")
        self._debug(exp_table)
        self._debug("Compare tables: fnd_table")
        self._debug(fnd_table)

        _error_message = ''
        if section_name != None:
            section_name = " in '%s' section" % section_name
        else:
            section_name = ''

        # Checking column headers from first rows.
        # 'new_exp_head' and 'new_fnd_head' contain matched headers.
        new_exp_head = []
        new_fnd_head = {}
        for exp_head in exp_table[0]:
            if (fnd_table[0].count(exp_head)) == 0:
                _error_message += "\r\n'%s' column was not found%s." % (exp_head, section_name)
                self._debug(_error_message)
            else:
                new_exp_head.append([exp_head, exp_table[0].index(exp_head)])
                new_fnd_head[exp_head] = fnd_table[0].index(exp_head)

        for fnd_head in fnd_table[0]:
            if (exp_table[0].count(fnd_head)) == 0:
                _error_message += "\r\n'%s' column was not expected%s." % (fnd_head, section_name)
                self._debug(_error_message)

        if data_in_first_column is False:
            new_exp_row = []
            new_fnd_row = {}
            for i in range(1, len(exp_table)):
                new_exp_row.append([i, i])
                new_fnd_row[i] = i
        else:
            # Creating list of row identifiers by taking values from first column.
            exp_items = []
            for i in range(1, len(exp_table)):
                exp_items.append(exp_table[i][0])

            fnd_items = []
            for i in range(1, len(fnd_table)):
                fnd_items.append(fnd_table[i][0])

            # Checking rows by values in first column.
            # 'new_exp_row' and 'new_fnd_row' contain matched rows.
            new_exp_row = []
            new_fnd_row = {}
            for exp_item in exp_items:
                if (fnd_items.count(exp_item)) == 0:
                    _error_message += "\r\n'%s' row was not found%s." % (exp_item, section_name)
                    self._debug(_error_message)
                else:
                    new_exp_row.append([exp_item, exp_items.index(exp_item) + 1])
                    new_fnd_row[exp_item] = fnd_items.index(exp_item) + 1

            for fnd_item in fnd_items:
                if (exp_items.count(fnd_item)) == 0:
                    _error_message += "\r\n'%s' row was not expected%s." % (fnd_item, section_name)
                    self._debug(_error_message)

        # Checking values in mached rows and columns
        for row_name, row_num in new_exp_row:
            for col_name, col_num in new_exp_head:
                exp_value = exp_table[row_num][col_num]
                fnd_value = fnd_table[new_fnd_row[row_name]][new_fnd_head[col_name]]
                if self._simple_match(fnd_value, exp_value):
                    self._info("'%s' column of '%s' row contains value '%s'%s." % (
                    col_name, row_name, fnd_value, section_name))
                elif (exp_value != fnd_value):
                    exp_value = str(exp_value).strip()
                    fnd_value = str(fnd_value).strip()
                    if self._compare_numbers(exp_value, fnd_value, number_precision):
                        pass
                    elif self._compare_times(exp_value, fnd_value, time_precision):
                        pass
                    else:
                        _error_message += "\r\n'%s' was present instead of expected '%s' for '%s' column '%s' row%s." % (
                        fnd_value, exp_value, col_name, row_name, section_name)
                        self._debug(_error_message)

        self._debug(_error_message)
        return _error_message

    def _process_table(self, section_name, expected_values=None,
                       data_in_first_column=None, number_precision=None, time_precision=None):
        """ Process getting or checking a table, specified by section full name (with names of parent headers). """
        _sct_loc = self._find_section_area(section_name)
        self._debug("Section locator:")
        self._debug(_sct_loc)
        if _sct_loc is None:
            self.error_message += "Section '%s' was not found." % (section_name)
            return None
        if not self._is_visible(_sct_loc):
            self.error_message += "Section '%s' was not found." % (section_name)
            return None
        _tbl_loc = self._find_table(section_name, _sct_loc)
        self._debug("Table locator:")
        self._debug(_tbl_loc)
        if _tbl_loc is None or not self._is_visible(_tbl_loc):
            section_value = self.get_text(_sct_loc)
            style_loc = _sct_loc + "//style"
            for style_counter in range(1, 1 + int(self.get_matching_xpath_count(style_loc))):
                style_value = self.get_text(style_loc + "[" + str(style_counter) + "]")
                section_value = section_value.replace(style_value, "")
            section_value = section_value.strip(' \r\n')
            self._debug(section_value)
            if expected_values is None:
                return section_value
            else:
                if isinstance(expected_values, (list, tuple)):
                    expected_values = expected_values[0]
                if section_value.strip() != str(expected_values).strip():
                    self.error_message += "'%s' was present instead of '%s' in section '%s'." % (
                    section_value, str(expected_values), section_name)
                    return None
                else:
                    return section_value

        _actual_table = self._get_table_values(_tbl_loc)

        self._debug("Expected table:")
        self._debug(expected_values)
        self._debug("Actual_table:")
        self._debug(_actual_table)

        if expected_values is None:
            return _actual_table

        if isinstance(expected_values, (str, unicode)):
            expected_values = tuple([expected_values])

        if len(expected_values) > 0:
            _expected_table = self._convert_tuple_to_table(expected_values)
            self._debug("Expected table:")
            self._debug(_expected_table)
            self._debug("Actual_table:")
            self._debug(_actual_table)
            self.error_message += self._compare_tables(_expected_table,
                                                       _actual_table, section_name, number_precision=number_precision,
                                                       time_precision=time_precision,
                                                       data_in_first_column=data_in_first_column)

        return _actual_table

    def _select_chart_option(self, option, chart_number, timeout=60):
        chart_number = int(chart_number)

        self._debug("----- Select chart option (%s) for chart %s -----\r\n" % (option, chart_number))

        _options_link_loc = "//a[contains(@onclick, 'ChartOptions')]"

        # waiting for 'Columns...' link
        _timer_start = time.time()
        while (time.time() - _timer_start) < timeout:
            if int(self.get_matching_xpath_count(_options_link_loc)) > 0:
                break
            else:
                time.sleep(1)

        option_list = option.split(":")
        if len(option_list) > 1:
            _section_loc = self._find_section_area(option_list[0])
            if _section_loc is None:
                raise guiexceptions.GuiValueError("'%s' section was not found." % \
                                                  (option_list[0],))
            _options_link_loc = _section_loc + _options_link_loc
            option = option_list[1].strip()

        if int(self.get_matching_xpath_count(_options_link_loc)) < 1:
            raise guiexceptions.GuiValueError("'Chart Options' link was not found.")

        self.click_element("(%s)[%s]" % (_options_link_loc, chart_number), "don't wait")

        # check if dialog is open
        _options_dlg_loc = "//div[@id='chart_option_dlg']"
        if not self._is_visible(_options_dlg_loc):
            raise guiexceptions.GuiValueError("Chart Options dialog was not found.")

        _option_loc = "%s//*[normalize-space(text())='%s']" % (_options_dlg_loc, option)
        if int(self.get_matching_xpath_count(_option_loc)) == 0:
            _option_loc = "%s//*[contains(text(), '%s')]" % (_options_dlg_loc, option)
        if int(self.get_matching_xpath_count(_option_loc)) == 0:
            raise guiexceptions.GuiValueError("Option '%s' was not found in chart %s" % (option, chart_number))

        self.click_element(_option_loc, "don't wait")

        self.click_button("//button[text()='Save']", "don't wait")
        self._debug("\r\n----- (Select chart options) -----")

    def _select_columns(self, section_name, columns, clear_others=False, timeout=60):
        if columns is None:
            return False

        _done_button = "//button[text()='Done']"

        self._debug("----- Select columns (%s) in section '%s' -----\r\n" % (str(columns), str(section_name)))

        _section_loc = self._find_section_area(section_name)
        self._debug("_section_loc: %s" % _section_loc)
        if _section_loc is None:
            raise guiexceptions.GuiValueError("'%s' section was not found." % \
                                              (section_name,))
        _columns_link_loc = _section_loc + self.TABLE_COLUMNS_LINK_SELECTOR
        self._debug("_columns_link_loc: %s" % _columns_link_loc)

        # waiting for 'Columns...' link
        _timer_start = time.time()
        while (time.time() - _timer_start) < timeout:
            if int(self.get_matching_xpath_count(_columns_link_loc)) > 0:
                break
            else:
                time.sleep(1)

        if int(self.get_matching_xpath_count(_columns_link_loc)) < 1:
            raise guiexceptions.GuiValueError("'Columns' link was not found for section '%s'." % \
                                              (section_name,))

        self._debug("Clicking _columns_link_loc")
        self.click_element(_columns_link_loc, "don't wait")

        # check if dialog is open
        _columns_dlg_loc = "//div[@id='yui_table_options_dlg']"
        try:
            self.element_should_be_visible(_columns_dlg_loc)
        except:
            raise guiexceptions.GuiValueError("Table columns dialog was not found.")

        self._debug("Dialog is open.")

        # get list of columns
        columns_list = map(lambda x: x.strip(), columns.split(','))
        columns_not_found = list(columns_list)
        self._debug("Columns: " + str(columns_list))

        _columns_tbody_loc = _columns_dlg_loc + "//table[1]/tbody"

        _prev_speed = self.set_selenium_speed(0)
        self._debug("Selenium speed was: %s" % _prev_speed)

        _select_all_columns = None
        if "all" in columns_list:
            _select_all_columns = True
            self._debug("Selecting all columns.")
        elif columns == '':
            _select_all_columns = False
            self._debug("Removing all columns.")

        if _select_all_columns is not None:
            _columns_loc = _columns_tbody_loc + "//input[@name='table_options_columns[]' and @type='checkbox']"
            _columns_count = int(self.get_matching_xpath_count(_columns_loc))
            self._debug("_columns_count: %s" % _columns_count)
            for _col in range(1, 1 + _columns_count):
                _input_loc = "(" + _columns_loc + ")[" + str(_col) + "]"
                _column_state = self._is_checked(_input_loc)
                if _column_state != _select_all_columns:
                    self.click_element(_input_loc, "don't wait")
        else:
            # going through rows on the dialog
            _columns_rows_loc = _columns_tbody_loc + "/tr"
            _columns_rows_count = int(self.get_matching_xpath_count(_columns_rows_loc))
            columns_not_found = list(columns_list)
            for _row in range(1, 1 + _columns_rows_count):
                self._debug("_row: %s" % _row)
                _input_loc = _columns_rows_loc + "[" + str(
                    _row) + "]//input[@name='table_options_columns[]' and @type='checkbox']"
                _column_state = self._is_checked(_input_loc)
                self._debug("_column_state: %s" % _column_state)

                # suppose checkbox label was specified
                _column_label = self.get_text(_columns_rows_loc + "[" + str(_row) + "]//label[@for]")
                self._debug("_column_label: %s" % _column_label)
                _column_found = False
                for _column in columns_list:
                    self._debug("_column: %s" % _column)
                    self._debug("_simple_match: %s" % self._simple_match(_column_label, _column))
                    if self._simple_match(_column_label, _column):
                        if not _column_state:
                            self.click_element(_input_loc, "don't wait")
                        try:
                            columns_not_found.remove(_column)
                        except:
                            pass
                        self._debug("columns_not_found: %s" % columns_not_found)
                        _column_found = True
                        break
                if _column_found:
                    continue

                # suppose checkbox id was specified
                _column_id = self.get_element_attribute(_input_loc + "@id")
                self._debug("_column_id: %s" % _column_id)
                if _column_id in columns_list:
                    if not _column_state:
                        self.click_element(_input_loc, "don't wait")
                    try:
                        columns_not_found.remove(_column_id)
                    except:
                        pass
                    self._debug("columns_not_found: %s" % columns_not_found)
                    continue

                # clear checkbox if the column is not needed
                if clear_others and _column_state:
                    self.click_element(_input_loc, "don't wait")

            self._debug("columns_not_found: %s" % columns_not_found)
            if len(columns_not_found) > 0:
                _absent_columns = ''
                for _column in columns_not_found:
                    _absent_columns += "'%s', " % (_column,)
                self.error_message += "Columns %s were not found on page '%s'.\r\n\t" \
                                      % (_absent_columns, self.get_location())

        self.set_selenium_speed(_prev_speed)

        self._debug("Clicking 'Done' button.")
        self.click_button(_done_button, "don't wait")
        self._debug("\r\n----- (Select columns) -----")

    def _search_row(self, section_name, row_name=None, timeout=60):
        if row_name is None:
            return False

        self._debug("Searching row '%s' in section '%s'" % (str(row_name), str(section_name)))

        _section_loc = self._find_section_area(section_name)
        self._debug("_section_loc: %s" % _section_loc)
        if _section_loc is None:
            self.error_message += "Section '%s' was not found on page '%s'.\r\n" \
                                  % (section_name, self.get_location())
            return False
        _search_field_loc = _section_loc + "//input[contains(@id, 'search_field')]"

        if int(self.get_matching_xpath_count(_search_field_loc)) < 1:
            raise guiexceptions.GuiValueError(
                "'Search' field was not found for section '%s'.\nLocator: '%s'" % \
                (section_name, _search_field_loc))

        self.input_text(_search_field_loc, row_name)

        _search_button_loc = _section_loc + "//input[contains(@id, 'search-button')]"
        self.click_element(_search_button_loc, "don't wait")

        _tbl_loc = self._find_table(section_name)
        _timer_start = time.time()
        while (time.time() - _timer_start) < timeout:
            if _tbl_loc is None:
                time.sleep(1)
                _tbl_loc = self._find_table(section_name)
            else:
                break
        if _tbl_loc is None:
            self.error_message += "Row '%s' was not found on page '%s'.\r\n" \
                                  % (row_name, self.get_location())
            return False

    def _select_items_display(self, section_name, items_display=None, timeout=60):
        if items_display is None:
            return False

        self._debug(
            "Selecting '%s' number of items to display in '%s' section." % (str(items_display), str(section_name)))

        _section_loc = self._find_section_area(section_name)
        _display_sel_loc = _section_loc + "//*[contains(@id, 'display-rows')]//select"

        # waiting for the field
        _timer_start = time.time()
        while (time.time() - _timer_start) < timeout:
            if int(self.get_matching_xpath_count(_display_sel_loc)) > 0:
                break
            else:
                time.sleep(1)

        self.select_from_list(_display_sel_loc, str(items_display))

        # waiting for enabling the field
        _timer_start = time.time()
        while (time.time() - _timer_start) < timeout:
            if int(self.get_matching_xpath_count(_display_sel_loc + "/self::*[not(@disabled='disabled')]")) > 0:
                break
            else:
                time.sleep(1)

        if not int(self.get_matching_xpath_count(_display_sel_loc + "/self::*[not(@disabled='disabled')]")) > 0:
            self.error_message += "Enabled 'Items Displayed' was not found.\r\n"

    def _open_details(self, section_name, row_name):
        self._search_row(section_name, row_name)
        _table_loc = self._find_table(section_name)
        _return_list = self._process_table(section_name)
        if _return_list is None:
            return None
        _row = False
        for i in range(len(_return_list)):
            if _return_list[i][0].strip() == row_name:
                _row = i
                break
        if not _row:
            raise guiexceptions.GuiValueError("'%s' row was not found in section '%s'." % \
                                              (row_name, section_name,))
        self.click_link(
            "((" + _table_loc + "/tbody[not(contains(@style,'display: none'))]/tr)[" + str(_row) + "]/td)[1]//a")

    def _follow_link_in_table(self, section_name, row_name, col_name=None):
        _table_loc = self._find_table(section_name)
        _cell_loc = self._get_table_cell_loc(_table_loc, row_name, col_name)
        _link_loc = _cell_loc + "//a"
        _link_count = int(self.get_matching_xpath_count(_link_loc))
        if _link_count < 1:
            raise guiexceptions.GuiValueError("Link was not found for '%s' row '%s' column in section '%s'." % \
                                              (row_name, col_name, section_name,))
        else:
            self.click_link(_link_loc)

    def _follow_link_in_chart(self, section_name, link_name):
        _sct_loc = self._find_section_area(section_name)
        self._debug("Section locator:")
        self._debug(_sct_loc)
        if _sct_loc is None:
            self.error_message += "Section '%s' was not found." % (section_name)
            return None

        _link_loc = "%s//a[normalize-space(text())='%s']" % (_sct_loc, link_name)
        if int(self.get_matching_xpath_count(_link_loc)) == 0:
            _link_loc = "%s//a[contains(text(), '%s')]" % (_sct_loc, link_name)
        if int(self.get_matching_xpath_count(_link_loc)) == 0:
            raise guiexceptions.GuiValueError("Link '%s' was not found in section %s" % (link_name, section_name))

        self.click_link(_link_loc)

    def _chart_presence(self, section_name):
        _sct_loc = self._find_section_area(section_name)
        self._debug("Section locator:")
        self._debug(_sct_loc)
        if _sct_loc is None:
            self.error_message += "Section '%s' was not found." % (section_name)
            return False

        _chart_loc = "%s//img" % (_sct_loc)
        if int(self.get_matching_xpath_count(_chart_loc)) == 0:
            return False

        return self._is_visible(_chart_loc)

    def _export(self, section_name, timeout=60):
        self._debug("Exporting section '%s'" % str(section_name))

        _section_loc = self._find_section_area(section_name)
        if _section_loc is None:
            raise ValueError("Section '%s' was not found." % section_name)
        _export_link_loc = _section_loc + self.SECTION_EXPORT_LINK_SELECTOR

        # waiting for 'Export' link
        for i in range(timeout):
            if int(self.get_matching_xpath_count(_export_link_loc)) > 0:
                break
            else:
                time.sleep(1)

        if int(self.get_matching_xpath_count(_export_link_loc)) < 1:
            raise guiexceptions.GuiValueError("'Export' link was not found for section '%s'." % \
                                              (section_name,))

        _title = self.get_text("//*[@id='report_title']/h1").strip()

        self.click_element(_export_link_loc, "don't wait")

        sections = section_name.split(" > ")
        _start_time = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = self.wait_for_download(_title + " " + (sections[-1]).strip(), start_time=_start_time)
        self._info("CSV file was saved as %s" % filename)
        return filename

    def _pdf(self):
        self._debug("Saving section '%s' in PDF format.")

        _pdf_link_loc = "//a[contains(text(), 'PDF')]"

        if int(self.get_matching_xpath_count(_pdf_link_loc)) < 1:
            raise guiexceptions.GuiValueError("'PDF' link was not found.")

        _title = self.get_text("//*[@id='report_title']/h1").strip()

        self.click_element(_pdf_link_loc, "don't wait")

        _start_time = time.strftime("%Y-%m-%d %H:%M:%S")
        filename = self.wait_for_download(_title, start_time=_start_time)
        self._info("PDF file was saved as %s" % filename)
        return filename

    def _get_value(self, section_name, _return_list, row, column):
        _row = 0
        for _row_num in range(1, len(_return_list)):
            if str(_return_list[_row_num][0]).strip() == row.strip():
                _row = _row_num
                break
        if _row < 1:
            try:
                _row = int(row)
            except:
                pass
        if _row < 1 or _row >= len(_return_list):
            self.error_message += "Row '%s' was not found in '%s' table." % (row, section_name)
            return None

        _col = 0
        for _col_num in range(1, len(_return_list[0])):
            if str(_return_list[0][_col_num]).strip().find(column.strip()) > -1:
                _col = _col_num
                break
        if _col < 1:
            self.error_message += "Column '%s' was not found in '%s' table." % (column, section_name)
            return None

        _found_value = str(_return_list[_row][_col])
        return _found_value

    def _check_value(self, section_name, _return_list, row, column, criterion):
        self._debug("section_name: %s" % section_name)
        self._debug("_return_list: %s" % _return_list)
        self._debug("row: %s" % row)
        self._debug("column: %s" % column)
        self._debug("criterion: %s" % criterion)

        _found_value = self._get_value(section_name, _return_list, row, column)
        self._debug("_found_value: %s" % _found_value)

        if str(criterion)[0] != '<' and str(criterion)[0] != '>' and str(criterion)[0:2] != '==':
            if str(criterion)[0] != '=':
                criterion = "='%s'" % criterion
            else:
                criterion = "=='%s'" % criterion
            _found_value = "'%s'" % _found_value
            self._debug("criterion: %s" % criterion)
            self._debug("_found_value: %s" % _found_value)

        if _found_value is not None:
            try:
                if eval(_found_value + criterion):
                    return True
            except:
                pass
            # compare as numbers
            _found_value = re.search("([\-\d\.]+)", _found_value).groups()[0]
            try:
                if eval(_found_value + criterion):
                    return True
            except:
                pass

        self.error_message += "'%s' column for '%s' row in '%s' table had value %s, which does not satisfy %s criterion." % (
        column, row, section_name, _found_value, criterion)
        return False

    def _check_cell_value(self, section_name, row, column, criterion):
        self._debug("section_name: %s" % section_name)
        self._debug("row: %s" % row)
        self._debug("column: %s" % column)
        self._debug("criterion: %s" % criterion)

        _tbl_loc = self._find_table(section_name)
        if _tbl_loc is None:
            self.error_message += "Table was not found in section '%s'." % (section_name,)
            return False
        _found_value = self._get_table_cell_value(_tbl_loc, row, column)
        self._debug("_found_value: %s" % _found_value)

        if str(criterion)[0] != '<' and str(criterion)[0] != '>' and str(criterion)[0:2] != '==':
            if str(criterion)[0] == '=':
                criterion = "='%s'" % criterion
            else:
                criterion = "=='%s'" % criterion
            _found_value = "'%s'" % _found_value
            self._debug("criterion: %s" % criterion)
            self._debug("_found_value: %s" % _found_value)

        if _found_value is not None:
            try:
                if eval(_found_value + criterion):
                    return True
            except:
                pass
            # compare as numbers
            if _found_value is not None:
                _found_value = re.search("([\-\d\.]+)", _found_value).groups()[0]
                try:
                    if eval(_found_value + criterion):
                        return True
                except:
                    pass

        self.error_message += "'%s' column for '%s' row in '%s' table had value %s, which does not satisfy %s criterion." % (
        column, row, section_name, _found_value, criterion)
        return False

    def _create_autodownload_prefs_js(self, download_folder, mime_types):
        self._ff_profile.download_dir = download_folder
        self.prefs_js_path = os.path.join(self._ff_profile.directory, 'prefs.js')
        prefs_js = open(self.prefs_js_path, 'a+')

        # Generate Firefox's prefs.js.
        prefs_js.write('# Mozilla User Preferences\n')
        prefs_js.write('user_pref("browser.download.dir", "' + download_folder + '");\n')
        prefs_js.write('user_pref("browser.download.folderList", 2);\n')
        prefs_js.write('user_pref("browser.helperApps.neverAsk.saveToDisk","' + mime_types + '");\n')
        prefs_js.write('user_pref("browser.download.manager.showWhenStarting",false);\n')
        prefs_js.write('user_pref("firefox_prefs_browser.download.dir","' + download_folder + '");\n')
        prefs_js.write('user_pref("pdfjs.disabled",true);\n')
        prefs_js.write('user_pref("browser.altClickSave",true);\n')
        prefs_js.write('user_pref("plugin.scan.plid.all",false);\n')
        prefs_js.write('user_pref("general.warnOnAboutConfig",false);\n')
        prefs_js.write('user_pref("plugin.disable_full_page_plugin_for_types","application/pdf");\n')


        prefs_js.close()

    def configure_autodownload_for_browser(self, download_folder, mime_types):
        """Configures browser to proxy request through DUT by doing the
           followings:
              - stop all current running web browser.
              - stop the current running Selenium RC.
              - create a prefs.js file in existing Firefox profile directory.
              - restart Selenium RC again using the updated Firefox profile
                directory.

        Parameters:
            - `download_folder`: folder for saving downloadable files.
            - `mime_types`: A comma-separated list of MIME types to save to disk without asking what to use to open the file.

           Example:
           | Configure Autodownload For Browser | %{HOME} | text/csv |
        """
        try:
            self.close_browser()
            self._info('Delaying 5 seconds to allow Selenium RC to shutdown')
            time.sleep(5)
        except:
            pass
        self._create_autodownload_prefs_js(download_folder, mime_types)
        self._info('Delaying 5 seconds to allow Selenium RC to come up')
        time.sleep(5)

    def _get_filemtime(self, filename):
        filetimesecs = 0
        try:
            filetimesecs = os.path.getmtime(filename)
        except:
            pass
        return filetimesecs

    def wait_for_download(self, filename, start_time=None, timeout=600, download_directory=None):
        """Waiting for file downloading by firefox.

        Parameters:
            - `filename`: a part of a filename, which is downloaded by firefox.
            - `start_time`: start time of downloading (with format: "%Y-%m-%d %H:%M:%S").
            If this parameter is missed, files, which downloading was started
            1 minute ago, are searched.
            - `timeout`: timeout for downloading. Default timeout is 10 minutes.
            - `download_directory`: download directory.

        Return:
        Location (path with filename) of downloaded file.

        Example:
           | Configure Autodownload For Browser | ${TEMPDIR} | application/pdf |
           | Launch DUT Browser |
           | Log Into DUT |
           | ${start_time}= | Get Time |
           | Navigate To | Management Appliance | Centralized Services | System Status |
           | Click Link | Printable (PDF) | don't wait |
           | ${saved_pdf}= | Wait For Download | system_status | start_time=${start_time} | timeout=60 |
        """

        filename = re.sub("\W", "_", filename)
        filename = re.sub("_+", "_", filename)
        filename = filename.strip("_")
        self._debug("filename: %s" % filename)

        if start_time is None:
            start_time = time.time() - 60
        else:
            start_time = time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))

        self._debug("start_time: %s" % start_time)
        if download_directory is None:
            _download_dir = self._ff_profile.download_dir
        else:
            _download_dir = download_directory
        self._debug("_download_dir: %s" % _download_dir)

        _downloaded = False

        _timer_start = time.time()
        while (time.time() - _timer_start) < int(timeout):
            files = [f for f in os.listdir(_download_dir) if (f.find(filename) > -1)]
            for name in files:
                full_name = os.path.join(_download_dir, name)
                self._debug("file: %s" % name)
                filetimesecs = self._get_filemtime(full_name)
                self._debug("filetimesecs: %s" % filetimesecs)
                if filetimesecs >= start_time:
                    _downloaded = (name.find(".part") < 0)
                    if _downloaded:
                        return full_name
                    else:
                        break
            time.sleep(3)

        raise ValueError("Download of %s file was not finished successfully." % filename)


class ScheduledReportInfo(object):
    """Container class holding information about scheduled report.

    Attributes:
        - `report_type`: type of the report.
        - `title`: title of the report.
        - `time_range`: time range for the report data.
        - `delivery`: delivery option of the report.
        - `format`: format of the report.
        - `schedule`: scheduling options of the report.
        - `next_run`: next run date of the report.
        - `tier`: appliances or appliance groups for which the report is
                  run. Always 'None' for scheduled reports for Web.
    """
    _email_columns_order = ('report_type', 'title', 'time_range', 'delivery',
                            'format', 'tier', 'schedule', 'next_run')
    _web_columns_order = ('report_type', 'title', 'time_range', 'delivery',
                          'format', 'schedule', 'next_run')

    def __init__(self, report_type, title, time_range, delivery,format,
                 schedule, next_run, tier=None):
        self.report_type = report_type
        self.title = title
        self.time_range = time_range
        self.delivery = delivery
        self.format = format
        self.schedule = schedule
        self.next_run = next_run
        self.tier = tier

    def __str__(self):
        info_str = 'Report Type: %s; Report Title: %s; Time Range: %s; ' \
                   'Delivery: %s; Format: %s; Schedule: %s; ' \
                   'Next Run Date: %s;' % (self.report_type, self.title,
                                           self.time_range, self.delivery, self.format, self.schedule,
                                           self.next_run)

        if self.tier is not None:
            info_str += ' Tier: %s;' % (self.tier,)

        return info_str


class ArchivedReportInfo(object):
    """Container class holding information about archived report.

    :Attributes:
        - `report_type`: type of the report.
        - `title`: title of the report.
        - `time_range`: time range for the report data.
        - `format`: format of the report.
        - `generate_date`: date which report was generated on.
        - `tier`: appliances or appliance groups for which the report was
                      generated. Always 'None' for archived reports for Web.
    """
    _email_columns_order = ('title', 'report_type', 'format', 'tier',
                            'time_range', 'generate_date')
    _web_columns_order = ('title', 'report_type', 'format',
                          'time_range', 'generate_date')

    def __init__(self, report_type, title, time_range, format,
                 generate_date, tier=None):
        self.report_type = report_type
        self.title = title
        self.time_range = time_range
        self.format = format
        self.generate_date = generate_date
        self.tier = tier

    def __str__(self):
        info_str = 'Report Type: %s; Report Title: %s; Time Range: %s; ' \
                   'Format: %s; Generated On: %s;' % (self.report_type,
                                                      self.title, self.time_range, self.format,
                                                      self.generate_date)

        if self.tier is not None:
            info_str += ' Tier: %s;' % (self.tier,)

        return info_str
