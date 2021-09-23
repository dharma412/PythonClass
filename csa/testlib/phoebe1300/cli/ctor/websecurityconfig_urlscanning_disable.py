#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/websecurityconfig_urlscanning_disable.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

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
