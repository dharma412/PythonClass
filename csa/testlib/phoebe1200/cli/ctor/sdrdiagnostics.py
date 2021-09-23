# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/sdrdiagnostics.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from clictorbase import DEFAULT, IafCliConfiguratorBase


class sdrdiagnostics(IafCliConfiguratorBase):
    def __call__(self, option=DEFAULT):
        self._writeln('sdrdiagnostics')
        self._query_select_list_item(option)
        return self._wait_for_prompt()

    def batch(self):
        self._info('BATCH COMMAND: sdrdiagnostics status')
        self._to_the_top(1)
        self.clearbuf()
        self._writeln('sdrdiagnostics status')
        self._wait_for_prompt()
        self._info(self.getbuf())
        return self.getbuf()
