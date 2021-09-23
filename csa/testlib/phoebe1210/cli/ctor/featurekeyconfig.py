#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/featurekeyconfig.py#1 $
"""
IAF2 CLI command featurekeyconfig
"""

from sal.containers.yesnodefault import YES, NO
import clictorbase

DEFAULT = clictorbase.DEFAULT


class featurekeyconfig(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def setup(self):
        self._query_response('SETUP')
        return featurekeyconfigSetup(self._get_sess())


class featurekeyconfigSetup(clictorbase.IafCliConfiguratorBase):
    newlines = 2

    def autoactivate(self, toggle=DEFAULT):
        self._query_response('AUTOACTIVATE')
        self._query_response(toggle)
        self._to_the_top(self.newlines)

    def autocheck(self, toggle=DEFAULT):
        self._query_response('AUTOCHECK')
        self._query_response(toggle)
        self._to_the_top(self.newlines)


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    fc = featurekeyconfig(cli_sess)

    fc().setup().autoactivate(YES)
    fc().setup().autoactivate(NO)
    fc().setup().autocheck(YES)
    fc().setup().autocheck(NO)
