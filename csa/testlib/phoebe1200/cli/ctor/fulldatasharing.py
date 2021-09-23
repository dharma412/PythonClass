#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/fulldatasharing.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
SARF CLI command: fulldatasharing
"""

import clictorbase

from sal.containers.yesnodefault import YES, NO


class fulldatasharing(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln('fulldatasharing')
        idx = self._query('Do you wish to proceed', 'Choose the operation')
        if idx == 0:
            self._query_response(YES)  # yes, please proceed
            idx = self._query('license agreement', 'Choose the operation')
            if idx == 0:
                self._query_response(YES)  # accept the license agreement
        return self

    def setup(self, enable=YES):
        self.level = 2
        self._query_response('setup')
        self._query_response(enable)
        self._to_the_top(self.level)


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    fdsh = fulldatasharing(cli_sess)
    fdsh().setup(enable=YES)
    fdsh().setup(enable=NO)
