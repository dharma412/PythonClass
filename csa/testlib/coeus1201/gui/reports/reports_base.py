#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/gui/reports/reports_base.py#1 $

import re
import time

import common.gui.guiexceptions as guiexceptions
from common.gui.guicommon import GuiCommon


class ReportsBase(GuiCommon):

    """Base class for support report manipulation.

    This class provides basic actions for reports configuration libraries.
    To manipulate with reports you should be aware of supported report types.

    Available report types:
    - `overview`,
    - `users`,
    - `web sites`,
    - `url categories`,
    - `application visibility`,
    - `anti-malware`,
    - `client malware risk`,
    - `web reputation filters`,
    - `l4 traffic monitor`,
    - `reports by user location`,
    - `system capacity`.

    This types are used on report creation stage.

    Example:
    | Scheduled Reports Add Report | overview |
    | Scheduled Reports Add Report | url categories |

    Every report type has it's specifics chart data values and sort column
    values.

    Chart data values for report types:
    `overview`:
    | N/A |

    `users`:
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

    `web sites`:
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

    `url categories`:
    | Top URL Categories | Top URL Categories |
    | `bw used` | `bw used` |
    | `bw saved` | `bw saved` |
    | `time spent` | `time spent` |
    | `webcat allowed` | `webcat allowed` |
    | `webcat monitored` | `webcat monitored` |
    | `webcat warned` | `webcat warned` |
    | `webcat blocked` | `webcat blocked` |
    | `total completed` | `total completed` |
    | `total blocked` | `total blocked` |
    | `transactions total` | `transactions total` |

    `application visibility`:
    | Top Application Types | Top Applications |
    | `bw used` | `bw used` |
    | `completed` | `completed` |
    | `limited` | `limited` |
    | `not limited` | `not limited`  |
    | `blocked` | `blocked` |
    | `avc blocked` | `avc blocked` |
    | `transactions total` | `transactions total` |

    `anti-malware`:
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

    `client malware risk`:
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

    `web reputation filters`:
    | N/A |

    `l4 traffic monitor`:
    | Top Client IPs | Top Malware Sites |
    | `total monitored` | `total monitored` |
    | `total blocked` | `total blocked` |
    | `total detected` | `total detected` |

    `reports by user location`:
    | N/A |

    `system capacity`:
    | N/A |

    To specify report chart data use values represented above.

    Example:
    | ${type} | Set Variable | url categories |
    | Scheduled Reports Add Report | ${type} |
    | ... | title=Report2 |
    | ... | report_format=csv |
    | ... | time_range=num days, 50 |
    | ... | schedule=monthly, 03, 30 |
    | ... | email_to=mkrysiuk@ironport.com |
    | ... | num_of_rows=20 |
    | ... | chart_data=webcat monitored, webcat blocked |
    | ... | sort_col=time spent |

    In this example we specified chart data for `url categories` report type.
    First chart will contain `webcat monitored` values, and second one
    `webcat blocked` values.
    To specify only one chart data and leave another default or with it's
    previous value just pass ${None} or None as it's value (See second example):

    Example:
    | ${type} | Set Variable | url categories |
    | Scheduled Reports Add Report | ${type} |
    | ... | title=Report2 |
    | ... | report_format=csv |
    | ... | time_range=num days, 50 |
    | ... | schedule=monthly, 03, 30 |
    | ... | email_to=mkrysiuk@ironport.com |
    | ... | num_of_rows=20 |
    | ... | chart_data=${None}, webcat blocked |
    | ... | sort_col=time spent |

    To select certain sort column values use next tables:

    Sorting column values:

    `overview`, `reports by user location`, `system capacity`:
    | N/A |

    `users`, `web sites`, `url categories`:
    | 'bw used' |
    | 'time spent' |
    | 'total completed' |
    | 'total blocked' |
    | 'transactions total' |

    `application visibility`:
    | 'bw used' |
    | 'completed' |
    | 'blocked' |
    | 'total' |

    `anti-malware`, `client malware risk`. `l4 traffic monitor`:
    | 'total monitored' |
    | 'total blocked' |
    | 'total detected' |

    `web reputation filters`:
    | 'block' |
    | 'malware detected' |
    | 'clean' |
    | 'allow' |

    Next example shows how to specify sorting column for report:

    Example:
    | ${type} | Set Variable | l4 traffic monitor |
    | Scheduled Reports Add Report | ${type} |
    | ... | title=Report7 |
    | ... | report_format=pdf |
    | ... | time_range=last week |
    | ... | schedule=monthly, 03, 30 |
    | ... | email_to=mkrysiuk@ironport.com |
    | ... | num_of_rows=50 |
    | ... | chart_data=total monitored, total detected |
    | ... | sort_col=total monitored, total blocked, total detected |

    In this example we specify three sorting columns for l4 traffic monitor
    report. To leave previous value or default value see chart data examples.
    """

    _available_user_chart_types = \
        {'bw used':'WEB_USER_DETAIL.BANDWIDTH_USED',
         'bw saved':'BANDWIDTH_SAVED',
         'time spent':'WEB_USER_DETAIL.TIME_SPENT',
         'webcat blocked':'WEB_USER_DETAIL.BLOCKED_BY_WEBCAT',
         'app blocked':'WEB_USER_DETAIL.BLOCKED_BY_APPLICATION',
         'wbrs blocked':'WEB_USER_DETAIL.BLOCKED_BY_WBRS',
         'amv blocked':'WEB_USER_DETAIL.BLOCKED_MALWARE',
         'other blocked':'WEB_USER_DETAIL.BLOCKED_BY_ADMIN_POLICY',
         'total warned':'WEB_USER_DETAIL.WARNED_TOTAL',
         'total completed':'WEB_USER_DETAIL.COMPLETED_TRANSACTION_TOTAL',
         'total blocked':'WEB_USER_DETAIL.BLOCKED_TRANSACTION_TOTAL',
         'transactions total':'WEB_USER_DETAIL.TRANSACTION_TOTAL'
        }

    _available_domain_chart_types = \
        {'bw used':'DOMAINS.BANDWIDTH_USED',
         'bw saved':'BANDWIDTH_SAVED_BY_BLOCKING',
         'time spent':'DOMAINS.TIME_SPENT',
         'webcat blocked':'DOMAINS.BLOCKED_BY_WEBCAT',
         'app blocked':'DOMAINS.BLOCKED_BY_AVC',
         'wbrs blocked':'DOMAINS.BLOCKED_BY_WBRS',
         'amv blocked':'DOMAINS.BLOCKED_BY_AMW',
         'other blocked':'DOMAINS.OTHER_BLOCKED',
         'total completed':'DOMAINS.COMPLETED_TRANSACTION_TOTAL',
         'total blocked':'DOMAINS.BLOCKED_TRANSACTION_TOTAL',
         'transactions total':'DOMAINS.TRANSACTION_TOTAL'
        }

    _available_webcat_chart_types = \
        {'bw used':'WEB_WEBCAT_DETAIL.BANDWIDTH_USED',
         'bw saved':'BANDWIDTH_SAVED',
         'time spent':'WEB_WEBCAT_DETAIL.TIME_SPENT',
         'webcat allowed':'WEB_WEBCAT_DETAIL.ALLOWED_BY_WEBCAT',
         'webcat monitored':'WEB_WEBCAT_DETAIL.MONITORED_BY_WEBCAT',
         'webcat warned':'WEB_WEBCAT_DETAIL.WARNED_BY_WEBCAT',
         'webcat blocked':'WEB_WEBCAT_DETAIL.BLOCKED_BY_WEBCAT',
         'total completed':'WEB_WEBCAT_DETAIL.COMPLETED_TRANSACTION_TOTAL',
         'total blocked':'WEB_WEBCAT_DETAIL.BLOCKED_TRANSACTION_TOTAL',
         'transactions total':'WEB_WEBCAT_DETAIL.TRANSACTION_TOTAL'
        }

    _available_avc_chart_types = \
        {'bw used':'WEB_APPLICATION_TYPE_DETAIL.BANDWIDTH_USED',
         'completed':'WEB_APPLICATION_TYPE_DETAIL.COMPLETED_TRANSACTION_TOTAL',
         'limited':'WEB_APPLICATION_TYPE_DETAIL.BW_LIMITED',
         'not limited':'WEB_APPLICATION_TYPE_DETAIL.BW_NOT_LIMITED',
         'blocked':'WEB_APPLICATION_TYPE_DETAIL.BLOCKED_TRANSACTION_TOTAL',
         'avc blocked':'WEB_APPLICATION_TYPE_DETAIL.BLOCKED_BY_AVC',
         'transactions total':'WEB_APPLICATION_TYPE_DETAIL.TRANSACTION_TOTAL'
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
        {'category':'key',
         'bw saved':'BANDWIDTH_SAVED',
         'requests monitored':'WEB_MALWARE_CATEGORY.MONITORED_MALWARE_REQUEST',
         'responses monitored': \
         'WEB_MALWARE_CATEGORY.MONITORED_MALWARE_RESPONSE',
         'requests blocked':'WEB_MALWARE_CATEGORY.BLOCKED_MALWARE_REQUEST',
         'responses blocked':'WEB_MALWARE_CATEGORY.BLOCKED_MALWARE_RESPONSE',
         'total monitored':'WEB_MALWARE_CATEGORY.MONITORED_MALWARE',
         'total blocked':'WEB_MALWARE_CATEGORY.BLOCKED_MALWARE',
         'total detected':'WEB_MALWARE_CATEGORY.DETECTED_MALWARE',
         'monitored or blocked': \
         'WEB_MALWARE_CATEGORY.MONITORED_MALWARE' + \
         ',WEB_MALWARE_CATEGORY.BLOCKED_MALWARE',
        }

    _available_amv_chart_threats = \
        {'category':'key1',
         'bw saved':'BANDWIDTH_SAVED',
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
        {'bw saved':'BANDWIDTH_SAVED',
         'requests monitored':'WEB_USER_DETAIL.MONITORED_MALWARE_REQUEST',
         'responses monitored':'WEB_USER_DETAIL.MONITORED_MALWARE_RESPONSE',
         'requests blocked':'WEB_USER_DETAIL.BLOCKED_MALWARE_REQUEST',
         'responses blocked':'WEB_USER_DETAIL.BLOCKED_MALWARE_RESPONSE',
         'total monitored':'WEB_USER_DETAIL.MONITORED_MALWARE',
         'total blocked':'WEB_USER_DETAIL.BLOCKED_MALWARE',
         'total detected':'WEB_USER_DETAIL.DETECTED_MALWARE_TOTAL',
         'monitored or blocked': \
         'WEB_USER_DETAIL.MONITORED_MALWARE,WEB_USER_DETAIL.BLOCKED_MALWARE'
         }

    _available_client_activity_traffic = \
        {'total monitored':'WEB_USER_BY_TRAFFIC_MONITOR.MONITORED_MALWARE',
         'total blocked':'WEB_USER_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE',
         'total detected': \
         'WEB_USER_BY_TRAFFIC_MONITOR.MONITORED_MALWARE' + \
         ',WEB_USER_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE'
         }

    _available_traffic_monitor_by_user_chart = \
        {'total monitored':'WEB_USER_BY_TRAFFIC_MONITOR.MONITORED_MALWARE',
         'total blocked':'WEB_USER_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE',
         'total detected':'WEB_USER_BY_TRAFFIC_MONITOR.MONITORED_MALWARE' + \
         ',WEB_USER_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE'
        }

    _available_traffic_monitor_by_host_chart = \
        {'total monitored':'WEB_HOST_BY_TRAFFIC_MONITOR.MONITORED_MALWARE',
         'total blocked':'WEB_HOST_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE',
         'total detected':'WEB_HOST_BY_TRAFFIC_MONITOR.MONITORED_MALWARE' + \
         ',WEB_HOST_BY_TRAFFIC_MONITOR.BLOCKED_MALWARE'
        }

    _report_type_to_chart_data = \
        {'overview':None,
         'users': _available_user_chart_types,
         'web sites': _available_domain_chart_types,
         'url categories': _available_webcat_chart_types,
         'application visibility': None,
         'anti-malware': None,
         'client malware risk': None,
         'web reputation filters': None,
         'l4 traffic monitor': None,
         'reports by user location': None,
         'system capacity': None
        }


    _report_types = {'overview':'wsa_monitor_overview_scheduled',
                    'users':'wsa_users',
                    'web sites':'wsa_web_sites',
                    'url categories':'wsa_url_categories',
                    'application visibility':'wsa_applications',
                    'anti-malware':'wsa_malware',
                    'client malware risk':'wsa_client_activity',
                    'web reputation filters':'wsa_web_reputation_filters',
                    'l4 traffic monitor':'wsa_l4_traffic_monitor',
                    'reports by user location':'wsa_mus_scheduled',
                    'system capacity':'wsa_system_capacity'
                    }

    def _convert_to_tuple_from_colon_separated_string(self, user_input):
        if isinstance(user_input, (str, unicode)):
            user_input = tuple([item.strip() for item in user_input.split(':')])
        else:
            raise ValueError('Argument \'%s\' should be string type.' % \
                            (user_input,))
        return user_input


    def _select_report_type(self, report_type):

        if report_type not in self._report_types.keys():
            raise guiexceptions.ConfigError("Invalid report type '%s'." % \
                                            (report_type))
        self.select_from_list('report_type', '%s' % \
                              (self._report_types[report_type],))

    def _fill_report_title(self, title):
        self.input_text("xpath=//input[@id='report_title']", title)

    def _select_time_range(self, range):
        time_range_types = {'last day':'calendar_day',
                            'last week':'calendar_week',
                            'last month':'calendar_month',
                            'num days':'custom_day',
                            'timestamp':'timestamp_day'
                            }
        range = self._convert_to_tuple_from_colon_separated_string(range)
        if len(range) == 2:
            time_range, num_days = range
        elif len(range) == 3:
            time_range = range[0]
            date1 = range[1]
            date2 = range[2]
        else:
            time_range = range[0]
            num_days = None

        if time_range.lower() not in time_range_types.keys():
            raise guiexceptions.ConfigError("Invalid time range '%s'." % \
                                            (time_range))
        if time_range.lower() == 'timestamp':
            self._select_timestamp(date1, date2)
        else:
            self.select_from_list('days_include', '%s' % \
                              (time_range_types[time_range.lower()],))
            if num_days is not None:
                if not num_days.isdigit():
                    raise guiexceptions.ConfigError(
                        "Invalid value '%s'. Should be positive int." % \
                            (num_days))
                self.input_text("xpath=//input[@id='custom_day']", num_days)

    def _select_report_format(self, format):
        format_types = {'pdf':'id=format_pdf',
                        'csv':'id=format_csv'
                        }
        if format not in format_types.keys():
            raise guiexceptions.ConfigError("Invalid format '%s'." % (format))
        self._click_radio_button(format_types[format])

    def _select_report_schedule(self, schedule):
        schedule_types = {'daily':'id=schedule_type_daily',
                          'weekly':'id=schedule_type_weekly',
                          'monthly':'id=schedule_type_monthly'}
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
            self.input_text("xpath=//input[@id='recipients']", '')
        else:
            self.input_text("xpath=//input[@id='recipients']", emails)

    def _select_number_of_rows(self, number_of_rows):
        if not self._is_element_present("xpath=//select[@id='rows']"):
            return
        number_of_row_types = ['10', '20', '50', '100']
        if number_of_rows not in number_of_row_types:
                raise guiexceptions.ConfigError(
                    "Invalid number of rows '%s'." % (number_of_rows))
        self.select_from_list('id=rows', '%s' % (number_of_rows))

    def _select_chart_data(self, type, row, type_dict):
        link = "xpath=//table[@class='layout']//tr[%d]//td[2]/a" % (row,)
        if type.lower() == 'none':
            return
        if type not in type_dict.keys():
            raise guiexceptions.ConfigError(
                    "Invalid chart data type '%s'." % (type))

        radio_button_link = "xpath=//input[@id='chart_option_dlg_%s']" % \
                             (type_dict[type])

        self.click_element(link, "don't wait")
        self._click_radio_button(radio_button_link)
        self.click_button("xpath=//span[@class='button-group']//button[contains(text(),'Save')]",
                           "don't wait")

    def _get_type_dicts(self, report_type):

        if report_type in ['users', 'web sites', 'url categories',
                           'web reputation filters']:
            return (self._report_type_to_chart_data[report_type],
                    self._report_type_to_chart_data[report_type],)
        if report_type == 'application visibility':
            return (self._available_avc_chart_types,
                    self._available_avc_name_chart_types)
        if report_type == 'anti-malware':
            return (self._available_amv_chart_categories,
                    self._available_amv_chart_threats)
        if report_type == 'client malware risk':
            return (self._available_client_activity_chart,
                    self._available_client_activity_traffic)
        if report_type == 'l4 traffic monitor':
            return (self._available_traffic_monitor_by_user_chart,
                    self._available_traffic_monitor_by_host_chart)

    def _select_chart_display_data(self, report_type, data):

        l_type_dict, r_type_dict = self._get_type_dicts(report_type)
        data = self._convert_to_tuple_from_colon_separated_string(data)
        if len(data) == 2:
            chart_left, chart_right = data
        else:
            raise guiesceptions.ConfigError('')
        if chart_left is not None:
            self._select_chart_data(chart_left, 2, l_type_dict)
        if chart_right is not None:
            self._select_chart_data(chart_right, 3, r_type_dict)

    def _select_sort_column(self, report_type, columns):
        typical_col_types = \
                    {'bw used':'Bandwidth Used',
                     'time spent':'Time Spent',
                     'total completed':'Transactions Completed',
                     'total blocked':'Transactions Blocked',
                     'transactions total':'Total Transactions'
                    }
        avc_col_types = \
                    {'bw used' : 'Bandwidth Used',
                     'completed':'Transactions Completed',
                     'blocked':'Transactions Blocked by Application',
                     'total':'Total Transactions'
                     }
        amw_col_types = \
                    {'total monitored': 'Transactions Monitored',
                     'total blocked': 'Transactions Blocked',
                     'total detected': 'Transactions Detected'
                     }
        client_activity_transactions_col_types = \
                    {'total monitored': 'Malware Transactions Monitored',
                     'total blocked' : 'Malware Transactions Blocked',
                     'total detected' : 'Total Malware Transactions Detected'
                     }
        client_activity_connections_col_types = \
                    {'total monitored': 'Malware Connections Monitored',
                     'total blocked' : 'Malware Connections Blocked',
                     'total detected' : 'Total Malware Connections Detected'
                     }
        wbrs_col_types = \
                    {'block' : 'Block',
                     'malware detected' : 'Scan Further: Malware Detected',
                     'clean':'Scan Further: Clean',
                     'allow':'Allow'
                     }
        l4_mon_col_types = \
                    {'total monitored':'Malware Connections Monitored',
                     'total blocked':'Malware Connections Blocked',
                     'total detected':'Total Malware Connections Detected'
                     }

        columns = \
            self._convert_to_tuple_from_colon_separated_string(columns)

        if report_type == 'users':
            elements = ('sort_columns[wsa_users_users_table]',)
            self._select_sort_column_from_list(typical_col_types,
                                               elements[0], columns[0])
        elif report_type == 'web sites':
            elements = ('sort_columns[wsa_web_sites_domains_matched]',)
            self._select_sort_column_from_list(typical_col_types,
                                               elements[0], columns[0])
        elif report_type == 'web reputation filters':
            elements = (
                    'sort_columns[wsa_web_reputation_filters_wbrs_filters]',)
            self._select_sort_column_from_list(wbrs_col_types,
                                               elements[0], columns[0])
        elif report_type == 'url categories':
            elements = ('sort_columns[wsa_url_categories_top_categories]',)
            self._select_sort_column_from_list(typical_col_types,
                                               elements[0], columns[0])
        elif report_type == 'application visibility':
            elements = ('sort_columns[wsa_applications_types_total]',
                        'sort_columns[wsa_applications_total]')
            self._select_sort_column_from_list(avc_col_types,
                                               elements[0], columns[0])
            self._select_sort_column_from_list(avc_col_types,
                                               elements[1], columns[1])
        elif report_type == 'anti-malware':
            elements = ('sort_columns[wsa_malware_malware_categories]',
                        'sort_columns[wsa_malware_malware_threats]')
            self._select_sort_column_from_list(amw_col_types,
                                               elements[0], columns[0])
            self._select_sort_column_from_list(amw_col_types,
                                               elements[1], columns[1])
        elif report_type == 'client malware risk':
            elements = ('sort_columns[wsa_client_activity_top_at_risk_clients]',
                        'sort_columns[wsa_client_activity_l4_tm_client_ips]')
            self._select_sort_column_from_list(
                                        client_activity_transactions_col_types,
                                               elements[0], columns[0])
            self._select_sort_column_from_list(
                                        client_activity_connections_col_types,
                                               elements[1], columns[1])
        elif report_type == 'l4 traffic monitor':
            elements = ('sort_columns[wsa_l4_traffic_monitor_l4_tm_client_ips]',
                'sort_columns[wsa_l4_traffic_monitor_malware_ports_detected]',
                'sort_columns[wsa_l4_traffic_monitor_top_l4_tm_sites]')
            self._select_sort_column_from_list(l4_mon_col_types,
                                               elements[0], columns[0])
            self._select_sort_column_from_list(l4_mon_col_types,
                                               elements[1], columns[1])
            self._select_sort_column_from_list(l4_mon_col_types,
                                               elements[2], columns[2])

    def _select_sort_column_from_list(self, type_dict, locator, label):
        if label.lower() == 'none':
            return
        if label is not None:
            self.select_from_list(
                                  "xpath=//select[@name='%s']" % (locator,),
                                  '%s' % (type_dict[label],))

    def _get_report_row_index(self, name, col):
        report_table = '//table[@class="cols"]'
        table_rows = self.get_matching_xpath_count(
                                     '%s/tbody/tr' % (report_table,))
        for i in xrange(2, int(table_rows) + 1):
            report_name = self.get_text('xpath=%s/tbody/tr[%s]/td[%s]' %
                              (report_table, i, col)).split(' \n')[0]
            if name == report_name:
                return i
        return None

    def _click_edit_report_link(self, name):
        cell_id = 'xpath=//table[@class="cols"]//tr[%s]//td[2]/a'

        row = self._get_report_row_index(name, 2)
        if row is None:
            raise guiexceptions.GuiControlNotFoundError(
                    'Report "%s"' % (name,), self.get_location())
        self.click_link(cell_id % (row))

    def _click_delete_button(self):
        self.click_button("xpath=//input[@value='Delete']", "don't wait")
        self.click_button("xpath=//button[text()='Delete']")


    def _check_for_deletion(self, name, name_col, check_col):
        cell_id = 'xpath=//table[@class="cols"]//tr[%s]//td[%s]/input'

        row = self._get_report_row_index(name, name_col)
        if row is None:
            raise guiexceptions.GuiControlNotFoundError(
                    'Report "%s"' % (name,), self.get_location())
        self.click_element(cell_id % (row, check_col), "don't wait")

    def _set_archive_setting(self, setting):
        archive_checkbox = "xpath=//input[@name='archive']"
        if setting not in ['yes', 'no']:
            raise guiexceptions.ConfigError(
                'Invalid archive setting \'%s\'.Should be \'yes\' or \'no\'.' \
                % (setting,))
        if setting.lower() == 'yes':
            self.select_checkbox(archive_checkbox)
        else:
            self.unselect_checkbox(archive_checkbox)

    def _select_timestamp(self, start_date, end_date):
        setting_type_input = 'current_date_range'
        start_date_input = 'custom_date_from'
        end_date_input = 'custom_date_end'
        start_time_input = 'custom_time_from'
        end_time_input = 'custom_time_end'
        try:
            start_date = time.strptime(start_date, '%d %b %Y %H')
            end_date = time.strptime(end_date, '%d %b %Y %H')
        except ValueError:
            raise ('Incorrect time range value: %s, %s.' % \
                   (start_date, end_date))
        if start_date > end_date:
            raise guiexceptions.GuiValueError('Incorrect time range %s, %s.' + \
                'first date should be less than second date.' % \
                (start_date, end_date))
        # used trick: start and end date passed into hidden values instead using
        # calendar stuff.

        self._set_input_value_with_javascript(setting_type_input, 'timestamp_day')
        self._set_input_value_with_javascript(start_date_input,
                        time.strftime('%d/%m/%Y', start_date))
        self._set_input_value_with_javascript(end_date_input,
                        time.strftime('%d/%m/%Y', end_date))
        self._set_input_value_with_javascript(start_time_input,
                        time.strftime('%H', start_date))
        self._set_input_value_with_javascript(end_time_input,
                        time.strftime('%H', end_date))

    def _get_report_type(self):
        type = self.get_value("xpath=//input[@name='report_type']")
        return [k for k, v in self._report_types.iteritems() if v == type][0]


    def _show_all(self):
        if self._is_element_present('id=pageSize'):
            self.select_from_list('id=pageSize', 'All')
