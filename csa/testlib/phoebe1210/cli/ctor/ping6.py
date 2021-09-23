#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/ping6.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

import re
import time
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, IafCliError, \
    REQUIRED, NO_DEFAULT, DEFAULT, REGEX, EXACT

DEBUG = True


class CantResolveHostError(IafCliError): pass


class ping6(IafCliConfiguratorBase):
    """
    ping6 - returns % of packets through
    """

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('hostname nor servname provided', EXACT): CantResolveHostError,
        })

    def __call__(self, host=REQUIRED, interface=DEFAULT):
        self._writeln(self.__class__.__name__)
        self._query_select_list_item(interface)
        self._query_response(host)
        time.sleep(10)
        self._sess.interrupt()
        lines = self._wait_for_prompt()

        pa = re.compile('(\d+\.\d+)%')
        result = pa.findall(lines)
        if result:
            percentage = float(result[0])
        else:
            percentage = 100
        return (100 - percentage)


if __name__ == '__main__':
    from clictorbase import get_sess

    sess = get_sess()
    pi = ping6(sess)
    #    print pi(host='qa19.qa')
    print pi(host='qa70.qa')
#    print pi(host='qa.qa')
