#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/archived_report_info.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

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
