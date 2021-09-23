#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/suspendlistener.py#1 $
"""IAF Command Line Interface (CLI) configurator: suspendlistener
"""

import clictorbase


class suspendlistener(clictorbase.IafCliConfiguratorBase):
    def __call__(self, listener_name='All', delay=''):
        self._writeln('suspendlistener')
        self._expect(['Enter the number of seconds', 'Choose the listener', 'no listeners configured'])
        if self._expectindex == 0:
            self._query_response(delay)
            self._wait_for_prompt()
        elif self._expectindex == 1:
            self._query_select_list_item(listener_name)
            self._query_response(delay)
            self._wait_for_prompt()


if __name__ == '__main__':
    import resumelistener

    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = suspendlistener(cli_sess)
    # test case
    cli()
    print "Test passed, resuming listeners..."
    resumelistener.resumelistener(cli_sess)()
