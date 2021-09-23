#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/GuiLibrary.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

# python import
import os

# sarf import
from common.TestLibrary import TestLibrary

# robot import
# from robot.variables import GLOBAL_VARIABLES, init_global_variables

import common.Variables


class GuiLibrary(TestLibrary):
    """ Common GUI Keywords Library for ESA, SMA, WSA products
    Robot Framework Test Library that aggregate all GUI keywords.
    """

    def __init__(self, dut=None, dut_version=None, dut_prefix='DUT',
                 dut_browser=None, server_host=None, server_port=None):

        # library variables
        self._parse_robot_vars(dut, dut_version, dut_prefix)
        # selenium variables
        selenium_kwargs = self._get_selenium_vars(dut_prefix, dut_browser, \
                                                  server_host, server_port)
        # path to import libraries from
        lib_path = self.dut_version
        gui_lib_names = self.get_test_libraries(['common/gui', os.path.join(lib_path, 'gui'), ])
        # prepare keywords dictionary
        self.keywords = self.get_keywords(gui_lib_names, self.dut, self.dut_version, **selenium_kwargs)


    def _get_selenium_vars(self, dut_prefix='DUT', dut_browser=None,
                           selenium_host=None, selenium_port=None):

        # browser and selenium server arguments
        selenium_kwargs = {}
        if dut_browser:
            selenium_kwargs['dut_browser'] = dut_browser
        if selenium_host:
            selenium_kwargs['server_host'] = selenium_host
            # if server host is not set server_port will be ignored
            if selenium_port:
                selenium_kwargs['server_port'] = selenium_port

        # library variables
        try:
            self.robot_vars = common.Variables.get_variables()
        except:
            # no robot variables can be retrieved
            # default values for selenium paramters will be used
            print "No Robot variables can be retrieved. Default or explicitly" \
                  " set values for browser and selenium server parameters " \
                  " will be used!"
            return selenium_kwargs

        # if dut is in robot vars then find corresponding DUT_BROWSER parameter
        for key in self.robot_vars.keys():
            if self.robot_vars[key] == self.dut:
                # key is RF variable in format ${DUT}
                dut_prefix = key[2:-1]
        dut_browser = dut_browser or \
                      str(self.robot_vars['${%s_BROWSER}' % (dut_prefix,)])

        # default value for DUT_BROWSER variable is "local/firefox"
        # if other then "local/firefox" value is specified then Selenium Grid
        # will be used
        if dut_browser == 'local/firefox':
            # firefox is used by default, not needed to be passed in
            # selenium_kwargs
            if 'dut_browser' in selenium_kwargs:
                del selenium_kwargs['dut_browser']
        else:
            # init browser setting that will be passed to grid
            selenium_kwargs['dut_browser'] = dut_browser

        return selenium_kwargs
