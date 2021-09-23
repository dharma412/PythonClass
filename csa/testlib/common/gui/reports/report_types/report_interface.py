#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/gui/reports/report_types/report_interface.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

class ReportInfoHolder(object):
    """ Interface which Report Info Holders should implement
    """

    def get_name(self):
        raise NotImplementedError

    def get_selector(self):
        raise NotImplementedError

    def get_chart_data(self):
        raise NotImplementedError

    def get_table_columns_data(self):
        raise NotImplementedError


class ChartInfoHolder(object):
    pass


class TableColumnsInfoHolder(object):
    pass
