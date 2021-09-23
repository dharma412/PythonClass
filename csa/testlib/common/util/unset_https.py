#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/unset_https.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.util.utilcommon import UtilCommon
from common.util.systools import SysTools


class UnsetHttps(UtilCommon):
    """
    Sets or unset https
    """

    def get_keyword_names(self):
        return [
            'unset_https',
            'set_https'
        ]

    def unset_https(self):
        """
        Example:
        | Unset Https |
        """
        self._info("Disabling HTTPS for " + self.dut_version)
        self._set_unset_https('no')

    def set_https(self):
        """
        Sets HTTPS

        Example:
        | Set Https |
        """
        self._info("Enabling HTTPS for " + self.dut_version)
        self._set_unset_https('yes')

    def _set_unset_https(self, https):
        """
        https specifies whether to set or unset https
        """

        cli = SysTools(self.dut, self.dut_version)._get_cli()
        cli.interfaceconfig().edit(if_name='Management', HTTPS=https)

        self._info("Committing changes")
        cli.commit()
