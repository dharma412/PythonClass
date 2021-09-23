#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/ping6.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import re
import time

from clictorbase import IafCliConfiguratorBase, IafCliParamMap, IafCliError, \
                            REQUIRED, NO_DEFAULT, DEFAULT
from sal.deprecated.expect import EXACT

DEBUG = True

class CantResolveHostError(IafCliError): pass
class NoRouteError(IafCliError): pass

class ping6(IafCliConfiguratorBase):
    """ping6 - returns % of packets through
    """
    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
             ('hostname nor servname provided, or not known', EXACT) : CantResolveHostError,
             ('No route to host', EXACT) : NoRouteError,
        })

    def __call__(self, host=REQUIRED, interface=DEFAULT):
        self._writeln(self.__class__.__name__)
        self._expect([("Which interface do you want to send the pings from?", EXACT)], timeout=3)
        self._query_select_list_item(interface)
        self._expect([("Please enter the host you wish to ping.", EXACT)], timeout=3)
        self._query_response(host)
        time.sleep(10)
        self._sess.interrupt()
        lines = self._wait_for_prompt()
        self._debug(lines)
        pa = re.compile('(\d+)\.\d+% packet loss')
        res = pa.findall(lines)
        if not res:
            raise IafCliError, 'Cannot parse command output'
        percentage = int(res[0])
        return (100 - percentage)

if __name__ == '__main__':
    from clictorbase import get_sess
    sess = get_sess()
    pi = ping6(sess)
    print pi(host='qa70.qa')
