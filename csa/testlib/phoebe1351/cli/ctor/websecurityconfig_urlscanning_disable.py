#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/websecurityconfig_urlscanning_disable.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import clictorbase
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap
from sal.deprecated.expect import REGEX

class websecurityconfig_urlscanning_disable(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('websecurityconfig urlscanning disable')
        websecurityconfig_urlscanning_disable = self._wait_for_prompt()
        return self