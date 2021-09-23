#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/showlicense.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

"""
cli -> showlicense

"""
from clictorbase import IafCliConfiguratorBase
import re


class showlicense(IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._restart()
        self._writeln('showlicense')
        license_status = self._wait_for_prompt()
        if re.search('No License Installed', license_status):
            return 'No License Installed'
        return license_status
