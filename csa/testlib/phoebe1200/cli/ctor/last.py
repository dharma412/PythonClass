#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/last.py#1 $

"""
IAF Command Line Interface (CLI)

command:
    - last
"""
import clictorbase


class last(clictorbase.IafCliConfiguratorBase):

    def __call__(self, option=None):
        self.clearbuf()
        if option == None:
            self._writeln(self.__class__.__name__)
        else:
            self._writeln(self.__class__.__name__ + ' ' + str(option))
        return self._wait_for_prompt()


if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = last(cli_sess)
    # test case
    print cli()
    print cli('admin')
