#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/EsaUtilsLibrary.py#1 $

# Import Python modules
import os

# Import SARF modules
from common.TestLibrary import TestLibrary


class EsaUtilsLibrary(TestLibrary):
    """ ESA Utilities Library

    """

    def __init__(self, dut=None, dut_version=None):
        # parse Robot variables
        self._parse_robot_vars(dut, dut_version)

        # path to import libraries from
        lib_path = self.dut_version

        # get list of test libraries
        lib_names = self.get_test_libraries([
            os.path.join(lib_path, 'utils')
        ])

        # get list of keywords
        self.keywords = self.get_keywords(lib_names, self.dut,
                                          self.dut_version)
