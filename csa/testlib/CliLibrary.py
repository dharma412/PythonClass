#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/CliLibrary.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

# python import
import os

# sarf import
from common.TestLibrary import TestLibrary


class CliLibrary(TestLibrary):
    """ Common CLI Keywords Library for ESA, SMA, WSA products

    Robot Framework Test Library that aggregate all CLI keywords.
    """

    def __init__(self, dut=None, dut_version=None, dut_prefix='DUT'):
        # library variables
        self._parse_robot_vars(dut, dut_version, dut_prefix)

        # get list of test libraries
        lib_path = self.dut_version
        lib_names = self.get_test_libraries([
            'common/cli',
            os.path.join(lib_path, 'cli'),
        ])

        # get list of keywords
        self.keywords = self.get_keywords(lib_names, self.dut, self.dut_version)
