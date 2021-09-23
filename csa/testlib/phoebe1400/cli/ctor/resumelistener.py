#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/resumelistener.py#1 $
"""IAF Command Line Interface (CLI) configurator: resumelistener
"""


import clictorbase

class resumelistener(clictorbase.IafCliConfiguratorBase):
    def __call__(self, listener_name='All'):
        self._writeln('resumelistener')
        self._expect([self._get_prompt(),'Choose the listener'])
        if self._expectindex == 1:
            self._query_select_list_item(listener_name)
            self._wait_for_prompt()


if __name__ == '__main__':
    import suspendlistener

    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = resumelistener(cli_sess)
    # suspend listeners first
    suspendlistener.suspendlistener(cli_sess)()
    # test case
    cli()

