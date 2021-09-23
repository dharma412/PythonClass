#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/EsaCliLibrary.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

# sarf import
from CliLibrary import CliLibrary


class EsaCliLibrary(CliLibrary):
    """ ESA CLI Library

    Robot Framework Test Library that aggregate all CLI keywords.
    """

    def __init__(self, dut=None, dut_version=None, dut_prefix='ESA'):
        # just call parent init with dut_prefix=ESA by default
        CliLibrary.__init__(self, dut, dut_version, dut_prefix)
