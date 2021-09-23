#!/usr/bin/env python

"""
IAF Command Line Interface (CLI)

command:
    - help
"""


import clictorbase as ccb

class help(ccb.IafCliConfiguratorBase):


    class IafHelpNotAvailableError(ccb.IafCliError): pass

    def __init__(self, sess=None):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict(
                {'help is not available for' : self.IafHelpNotAvailableError})

    def __call__(self, option=None):
        self.clearbuf()
        if option == None:
            self._writeln(self.__class__.__name__)
        elif option == 1:
            self._writeln(self.__class__.__name__+' detail')
        else:
            self._writeln(self.__class__.__name__+' '+str(option))
        return self._wait_for_prompt()

if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    cli = help(cli_sess)

    # test case
    print cli()
    print cli('status')

    try:
        cli('help')
    except help.IafHelpNotAvailableError:
        print "'help help' failed with IafHelpNotAvailable Error as expected."
        cli._wait_for_prompt()
    else:
        raise RuntimeError, 'Expecting IafHelpNotAvailableError.'

    try:
        cli('yes')
    except ccb.IafUnknownCommandError:
        print "'help yes' failed with IafUnknownCommandError as expected."
    else:
        raise RuntimeError, 'Expecting IafUnknownCommandError error.'
