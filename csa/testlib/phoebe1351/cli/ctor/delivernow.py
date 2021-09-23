#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/delivernow.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

"""
    IAF 2 CLI ctor - delivernow
"""


import clictorbase

class delivernow(clictorbase.IafCliConfiguratorBase):
    def __call__(self, how='all', host=None):
        if how == 'host': assert host
        self._sess.writeln('delivernow')
        if how == 'host':
            option = 'domain'
        else:
            option ='all'
        self._query_select_list_item(option, timeout=30)
        if how == 'host': self._query_response(host)
        # Not sure if this is needed
        self._wait_for_prompt()

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    dn = delivernow(cli_sess)
    dn(how='host', host='qa04.qa')
    dn()
