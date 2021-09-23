#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1362/gui/email/reporting/reports_parser_def/reporting_tables_helpers.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from data_load_monitor import wait_until_data_loaded

from dashboard_table import DashboardTable
from details_table import DetailsTable
from summary_table import SummaryTable


def get_table_class_by_name(table_name):
    all_names = []
    for table_class in (SummaryTable, DetailsTable, DashboardTable):
        available_names = table_class.get_available_table_names()
        available_name_prefixes = table_class.get_special_name_prefixes()
        if table_name in available_names or \
           any(map(lambda x: table_name.startswith(x), available_name_prefixes)):
            return table_class
        else:
            all_names.extend(available_names)
            all_names.extend(map('{0} ...'.format, available_name_prefixes))
    else:
        raise ValueError('Unknown table name "{0}". Available table names:\n{1}'.\
                         format(table_name, sorted(all_names)))


def reload_current_page_with_random_data(gui):
    url = gui.get_location()
    if 'random=1' in url:
        return
    elif '?' in url:
        gui.go_to('{0}&random=1'.format(url))
    else:
        gui.go_to('{0}?random=1'.format(url))
    wait_until_data_loaded(gui)


