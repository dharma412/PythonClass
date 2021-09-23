#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/suspendlistener.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

import clictorbase

from sal.deprecated.expect import EXACT

DEFAULT = clictorbase.DEFAULT

class suspendlistener(clictorbase.IafCliConfiguratorBase):

    class SLNoListenersError(clictorbase.IafCliError):
        """
        If there is an error when attempting to bouncerecipients,
        this exception class should be raised.
        """
        pass

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
                ('There are no listeners configured', EXACT) :
                self.SLNoListenersError
    })

    def __call__(self, input_dict=None, **kwargs):
        self._writeln('suspendlistener')
        param_map = clictorbase.IafCliParamMap(
                        end_of_command=self._get_prompt())
        param_map['listener_name'] = ['Choose the listener', DEFAULT, True]
        param_map['delay'] = ['number of seconds to wait', DEFAULT]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

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
