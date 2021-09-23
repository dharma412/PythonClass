#!/usr/bin/env python

# python import
import os

# SARF import
from common.TestLibrary import TestLibrary


class ApiLibrary(TestLibrary):
    """ Common API Keywords Library for ESA, SMA, WSA products

    Robot Framework Test Library that aggregate all API keywords.
    """

    def __init__(self, dut=None, dut_version=None, dut_prefix='DUT'):
        # library variables
        self._parse_robot_vars(dut, dut_version, dut_prefix)

        # get list of test libraries
        lib_names = self.get_test_libraries([
            'common/api',
            os.path.join(self.dut_version, 'api'),
        ])

        # get list of keywords
        self.keywords = self.get_keywords(lib_names, self.dut, self.dut_version)
