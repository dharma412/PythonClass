#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/zeus1350/gui/email/reporting/reports_parser_def/data_load_monitor.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

import re
import time

from common.util.sarftime import CountDownTimer

PERCENTAGE_LABEL = "//div[@id='container_reporting_system_heartbeat']"
TIME_RANGE_COMBO = "//select[@id='date_range']"

LOADING_FLAG = 'Loading'


class NoDataFound(Exception):
    pass


def wait_until_data_loaded(gui, timeout=10):
    loading_tmr = CountDownTimer(timeout).start()
    while loading_tmr.is_active():
        if gui._is_text_present(LOADING_FLAG):
            time.sleep(1)
        else:
            return
    print('!!! The "Loading" label is visible more than 5 seconds.' \
          'Table(s) data may not be populated.')


def change_time_range(gui, new_range):
    gui.select_from_list(TIME_RANGE_COMBO, new_range)
    gui.wait_until_page_loaded()
    wait_until_data_loaded(gui)


def verify_data_load_percentage_value(gui, expected_percentage,
                                      time_range=None, timeout=60):
    if not gui._is_element_present(PERCENTAGE_LABEL):
        return
    current_speed = gui.set_selenium_speed(0)
    try:
        current_location = gui.get_location()
        tmr = CountDownTimer(timeout).start()
        while tmr.is_active():
            if time_range is not None:
                change_time_range(gui, time_range)
            else:
                gui.go_to(current_location)
                wait_until_data_loaded(gui)
            load_prercentage_str = gui.get_text(PERCENTAGE_LABEL)
            match = re.search(r'([0-9]+\.[0-9]+)\s%', load_prercentage_str)
            if match and float(match.group(1)) >= expected_percentage:
                break
            else:
                time.sleep(5)
        else:
            raise NoDataFound('No data was found within {0} seconds timeout'. \
                              format(timeout))
    finally:
        gui.set_selenium_speed(current_speed)
