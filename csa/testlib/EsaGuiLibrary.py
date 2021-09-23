#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/EsaGuiLibrary.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

# sarf import
from GuiLibrary import GuiLibrary


class EsaGuiLibrary(GuiLibrary):
    """ ESA GUI Library
    Robot Framework Test Library that aggregate all GUI keywords.
    """

    def __init__(self, dut=None, dut_version=None, dut_prefix='ESA',
                 dut_browser=None, server_host=None, server_port=None):
        # just call parent init with dut_prefix=ESA by default
        GuiLibrary.__init__(self, dut, dut_version, dut_prefix, dut_browser,
                            server_host, server_port)
