#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/language.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $


import clictorbase


class language(clictorbase.IafCliConfiguratorBase):
    def __call__(self, lang=''):
        self.clearbuf()
        if lang:
            self._writeln('%s "%s"' % (self.__class__.__name__,
                                       lang))
        else:
            self._writeln(self.__class__.__name__)
        return self._wait_for_prompt()
