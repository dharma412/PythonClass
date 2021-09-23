#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/setgateway.py#1 $
"""IAF Command Line Interface (CLI) Configurator: setgateway.
"""
import clictorbase as cb


class setgateway(cb.IafCliConfiguratorBase):
    def __call__(self, ip_version=cb.DEFAULT, ip=''):
        """_query_response() call can raise clictorbase.IafIpHostnameError.
        The IP address must be 4 numbers separated by a period.
        Each number must be a value from 0 to 255. (Ex: 192.168.1.1) """
        self._writeln(self.__class__.__name__)
        self._query_select_list_item(ip_version)
        self._query_response(ip)
        self._wait_for_prompt()


if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    # if cli_sess object is present in namespace, we're using
    # the dev unit test harness, don't get a new one
    # also set valid gateway address to eng env if present, qa if not
    try:
        cli_sess
    except NameError:
        cli_sess = cb.get_sess()
        gw_addr = '172.17.0.6'
    else:
        gw_addr = '172.16.0.6'

    cli = setgateway(cli_sess)
    # test case
    cli()
    cli(gw_addr)
    try:
        cli('set.an.invalid.address')
    except cb.IafIpHostnameError, e:
        pass
    else:
        raise RuntimeError, 'No exception. Expecting IafIpHostnameError'
