#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/tuiconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
cli -> tuiconfig

"""
from clictorbase import IafCliConfiguratorBase, IafCliError

class tuiconfig(IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._restart()
        return self

    def _tui_config(self, options=' '):
        self._writeln(options)
        return self