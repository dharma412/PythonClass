#!/usr/bin/env python

# sarf import
from ApiLibrary import ApiLibrary


class EsaApiLibrary(ApiLibrary):
    """ ESA API Library

    Robot Framework Test Library that aggregate all API keywords.
    """

    def __init__(self, dut=None, dut_version=None, dut_prefix='ESA'):
        ApiLibrary.__init__(self, dut, dut_version, dut_prefix)
