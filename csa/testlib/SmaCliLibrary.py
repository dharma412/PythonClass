#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/SmaCliLibrary.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

# sarf import
from CliLibrary import CliLibrary


class SmaCliLibrary(CliLibrary):
    """ SMA CLI Library

    Robot Framework Test Library that aggregate all CLI keywords.
    """

    def __init__(self, dut=None, dut_version=None, dut_prefix='SMA'):
        # just call parent init with dut_prefix=SMA by default
        CliLibrary.__init__(self, dut, dut_version, dut_prefix)
