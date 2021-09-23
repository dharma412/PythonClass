# !/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/show_license.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase
from common.util.systools import SysTools


class ShowLicense(CliKeywordBase):
    """
        cli -> showlicense
    """

    def get_keyword_names(self):
        return ['show_license',
                ]

    def show_license(self):
        """
        cli -> showlicense

        Returns license status

        Examples:

        |  {$license_status}= Show License |
        |  Log  {$license_status}  |
        """
        if not (SysTools(self.dut, self.dut_version)._is_dut_a_virtual_model()):
            self._info('Its not a valid Virtual Model, returning ...')
            return
        return self._cli.showlicense()
