#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/outbreakflush.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import clictorbase
from sal.containers.yesnodefault import YES, NO

class outbreakflush(clictorbase.IafCliConfiguratorBase):
    class NoOutbreakFeatureKeyError(clictorbase.IafCliError): pass
    class OutbreakIsNotEnabledError(clictorbase.IafCliError): pass
    class FlushingRulesFailedError(clictorbase.IafCliError): pass

    def __call__(self,confirm=YES):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        flushed = self._query('want to clear the current rules',
                         'This feature requires activation with a software key.',
                         'This feature requires Outbreak Filters to be enabled (see "outbreakconfig").',
                         'Failed to clear the current rules.',timeout=10)

        if flushed == 0:
            self._query_response(confirm)
            res = self._query(self._get_prompt(),
                             'Cleared the current rules.',
                             'Failed to clear the current rules.',
                             timeout=30)
            if res == 0 or res == 1:
                return True
            else:
                raise self.FlushingRulesFailedError()
        elif flushed == 1:
            raise self.NoOutbreakFeatureKeyError()
        elif flushed == 2:
            raise self.OutbreakIsNotEnabledError()

if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    cli = outbreakflush(cli_sess)
    print cli()

