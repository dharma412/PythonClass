#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/ctor/resumelistener.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

import clictorbase

DEFAULT = clictorbase.DEFAULT


class resumelistener(clictorbase.IafCliConfiguratorBase):

    def __call__(self, input_dict=None, **kwargs):
        self._writeln(self.__class__.__name__)
        param_map = clictorbase.IafCliParamMap(
                        end_of_command=self._get_prompt())
        param_map['listener_name'] = ['Choose the listener', DEFAULT, True]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)


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

