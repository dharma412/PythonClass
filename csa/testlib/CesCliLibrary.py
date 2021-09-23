# python import
import os

# sarf import
from common.TestLibrary import TestLibrary


class CesCliLibrary(TestLibrary):
    """ Common CLI Keywords Library for CES CLI validation.

    Robot Framework Test Library that aggregate all CLI keywords.
    """

    def __init__(self, dut=None, dut_version=None, dut_prefix='ESA'):
        # library variables
        self._parse_robot_vars(dut, dut_version, dut_prefix)

        # get list of test libraries
        lib_path = self.dut_version
        lib_names = self.get_test_libraries([
            'common/cli',
            # os.path.join(lib_path, 'cli', 'ces_cli'),
            os.path.join(lib_path, 'ces_cli'),
        ])

        # get list of keywords
        self.keywords = self.get_keywords(lib_names, self.dut, self.dut_version)
