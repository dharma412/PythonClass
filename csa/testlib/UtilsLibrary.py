#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/UtilsLibrary.py#2 $

# python import
import os

# sarf import
from common.TestLibrary import TestLibrary


class UtilsLibrary(TestLibrary):
    """ WSA Utilities Library

    Robot Framework Test Library that provides different utilities:
    log parsing, checking log for errors, netinstall, recover network
    connectivity through IPMI, etc.
    """

    def __init__(self, dut=None, dut_version=None):
        # parse Robot variables
        self._parse_robot_vars(dut, dut_version)

        # path to import libraries from
        lib_path = self.dut_version

        # get list of test libraries
        lib_names = self.get_test_libraries([
            'common/util',
            'common/rest',
            os.path.join(lib_path, 'util'),
        ])
        # get list of keywords
        self.keywords = self.get_keywords(lib_names, self.dut,
                                          self.dut_version)
