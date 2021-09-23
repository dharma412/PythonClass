import os

from common.TestLibrary import TestLibrary


class NGGuiLibrary(TestLibrary):

    def __init__(self, dut=None, dut_version=None, dut_browser=None, dut_prefix='DUT'):
        self._parse_robot_vars(dut, dut_version, dut_prefix)
        gui_lib_names = self.get_test_libraries(['common/ngui', os.path.join(self.dut_version, 'ngui')])
        self.keywords = self.get_keywords(gui_lib_names, self.dut, self.dut_version, self.dut_browser)
        self.dut = dut
        self.dut_browser = dut_browser
