#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/shutdown.py#1 $

import time
import clictorbase
from sal.containers.yesnodefault import YES, NO, is_yes, is_no


class shutdown(clictorbase.IafCliConfiguratorBase):

    def __call__(self, seconds=0):
        self._writeln('shutdown')
        self._query_response(seconds)
        # wait for connections to close, then wait 30 more seconds
        # for complete shutdown and poweroff to occur
        time.sleep(seconds + 30)
        self.close()


if __name__ == '__main__':
    sd = shutdown(clictorbase.get_sess())
    sd()
