#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/ping.py#1 $

import re
import time

from clictorbase import IafCliConfiguratorBase, IafCliParamMap, IafCliError, \
                            REQUIRED, NO_DEFAULT, DEFAULT
from sal.deprecated.expect import EXACT

DEBUG = True

class CantResolveHostError(IafCliError): pass

class ping(IafCliConfiguratorBase):
    """ping - returns % of packets through
    """
    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
             ('cannot resolve', EXACT) : CantResolveHostError,
             })

    def __call__(self, host=REQUIRED, interface=DEFAULT):
        self._writeln('ping')
        self._query_select_list_item(interface)
        self._query_response(host)
        time.sleep(10)
        self._sess.interrupt()
        lines = self._wait_for_prompt()

        pa = re.compile('(\d+)\.\d+% packet loss')
        percentage = int(pa.findall(lines)[0])
        return (100 - percentage)

if __name__ == '__main__':
    from clictorbase import get_sess
    sess = get_sess()
    pi = ping(sess)
#    print pi(host='qa19.qa')
    print pi(host='qa70.qa')
#    print pi(host='qa.qa')
