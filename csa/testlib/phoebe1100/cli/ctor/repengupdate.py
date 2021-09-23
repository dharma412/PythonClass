#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/repengupdate.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import clictorbase
from sal.exceptions import ConfigError


class repengupdate(clictorbase.IafCliConfiguratorBase):
    def __call__(self, force=False):
        """Update repeng modules
        """
        self.clearbuf()
        if force:
            self._writeln('{0} force'.format(self.__class__.__name__))
        else:
            self._writeln(self.__class__.__name__)
        self._to_the_top(1)
        return self.getbuf()
