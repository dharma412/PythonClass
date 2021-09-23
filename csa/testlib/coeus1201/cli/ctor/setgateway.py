#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/setgateway.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""MGA CLI Configurator: setgateway"""

import clictorbase

class IafGatewayNotOnNetworkError(clictorbase.IafCliError):
    pass

class setgateway(clictorbase.IafCliConfiguratorBase):
    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('is not directly reachable',
                clictorbase.EXACT) : IafGatewayNotOnNetworkError,
        })

    def __call__(self, interface='', ip='', protocol=''):
        self._writeln('setgateway')
        self._query_select_list_item(protocol)
        self._query_select_list_item(interface)
        self._query_response(ip)
        self._wait_for_prompt()

def ctor_unit_test():
    # session host defaults to .iaf2rc.dut
    cli = setgateway(clictorbase.get_sess())

    # test1: positive test
    cli() # use default gateway

    # test2: negative  test
    try:
        cli(ip='set.an.invalid.address')
    except clictorbase.IafIpHostnameError, e:
            cli._restart()
    else:
        raise RuntimeError, 'Error: No exception. Expecting IafIpHostnameError'

    # test3: negative  test
    try:
        cli(ip='1.1.1.1')
    except IafGatewayNotOnNetworkError:
            cli._restart()
    else:
        raise RuntimeError,\
            'Error: No exception. Expecting IafGatewayNotOnNetworkError'

if __name__ == '__main__':
    ctor_unit_test()
