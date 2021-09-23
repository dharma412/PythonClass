#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/scheduled_report_info.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

class ScheduledReportInfo(object):
    """Container class holding information about scheduled report.

    Attributes:
        - `report_type`: type of the report.
        - `title`: title of the report.
        - `time_range`: time range for the report data.
        - `delivery`: delivery option of the report.
        - `reportformat`: format of the report.
        - `schedule`: scheduling options of the report.
        - `next_run`: next run date of the report.
        - `tier`: appliances or appliance groups for which the report is
                  run. Always 'None' for scheduled reports for Web.
    """
    _email_columns_order = ('report_type', 'title', 'time_range', 'delivery',
                            'reportformat', 'tier', 'schedule', 'next_run')

    _web_columns_order = ('report_type', 'title', 'time_range', 'delivery',
                          'reportformat', 'schedule', 'next_run')

    def __init__(self, report_type, title, time_range, delivery, reportformat,
                 schedule, next_run, tier=None):
        self.report_type = report_type
        self.title = title
        self.time_range = time_range
        self.delivery = delivery
        self.reportformat = reportformat
        self.schedule = schedule
        self.next_run = next_run
        self.tier = tier

    def __str__(self):
        info_str = 'Report Type: %s; Report Title: %s; Time Range: %s; ' \
                   'Delivery: %s; Format: %s; Schedule: %s; ' \
                   'Next Run Date: %s;' % (self.report_type, self.title,
                                           self.time_range, self.delivery, self.reportformat, self.schedule,
                                           self.next_run)

        if self.tier is not None:
            info_str += ' Tier: %s;' % (self.tier,)

        return info_str
