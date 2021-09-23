#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/gui/monitor/reports/reports_base_esa.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.gui.reports_base import ReportsBase
from esa.constants import email_reports

class ReportsBaseEsa(ReportsBase):
    """
    This class just overrides attributes of parent class
    that do not work with ESA reports manipulation.
    """
    _report_types = \
        {email_reports.AMP:'mga_advanced_malware_protection',
         email_reports.AMP_VERDICT_UPDATES:'mga_advanced_malware_protection_verdict_updates',
         email_reports.FILTERS:'mga_content_filters',
         email_reports.DLP_INCIDENT:'mga_dlp_incident_summary',
         email_reports.DELIVERY:'mga_outgoing_delivery_status',
         email_reports.DOMAIN_BASED:'mga_domain_overview',
         email_reports.EXECUTIVE:'mga_overview_scheduled',
         email_reports.IN_MAIL:'mga_incoming_mail_scheduled',
         email_reports.INT_USERS:'mga_internal_user_scheduled',
         email_reports.VOF :'mga_virus_outbreaks_scheduled',
         email_reports.OUT_DESTINATIONS:'mga_destination_domains',
         email_reports.OUT_MAIL:'mga_outgoing_mail_scheduled',
         email_reports.OUT_DOMAIN_SENDERS:'mga_internal_senders',
         email_reports.SENDER_GROUPS:'mga_sender_groups',
         email_reports.SYSTEM_CAP:'mga_system_capacity_scheduled',
         email_reports.TLS_CONN:'mga_tls_connections',
         email_reports.VIRUS_TYPES:'mga_virus_types',
         email_reports.RATE_LIMIT:'mga_rate_limit_sender',
         email_reports.SENDER_DOMAIN_REPUTATION:'mga_sender_domain_reputation',}

class ArchivedReportInfo(object):
    """Container class holding information about archived report.

    :Attributes:
        - `report_type`: type of the report.
        - `title`: title of the report.
        - `time_range`: time range for the report data.
        - `format`: format of the report.
        - `generate_date`: date which report was generated on.
    """
    _email_columns_order = ('title', 'report_type', 'format',
                            'time_range', 'generate_date')

    def __init__(self,
                 report_type,
                 title,
                 time_range,
                 format,
                 generate_date):
        self.report_type = report_type
        self.title = title
        self.time_range = time_range
        self.format = format
        self.generate_date = generate_date

    def __str__(self):
        info_str = 'Report Type: %s; Report Title: %s; Time Range: %s; '\
                   'Format: %s; Generated On: %s;' % (self.report_type,
                   self.title, self.time_range, self.format,
                   self.generate_date)
        return info_str

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
    """
    _email_columns_order = ('report_type', 'title', 'time_range', 'delivery',
                            'format', 'schedule', 'next_run')

    def __init__(self, report_type, title, time_range, delivery, format,
                 schedule, next_run):
        self.report_type = report_type
        self.title = title
        self.time_range = time_range
        self.delivery = delivery
        self.format = format
        self.schedule = schedule
        self.next_run = next_run


    def __str__(self):
        info_str = 'Report Type: %s; Report Title: %s; Time Range: %s; '\
                   'Delivery: %s; Format: %s; Schedule: %s; '\
                   'Next Run Date: %s;' % (self.report_type, self.title,
                   self.time_range, self.delivery, self.format, self.schedule,
                   self.next_run)
        return info_str

