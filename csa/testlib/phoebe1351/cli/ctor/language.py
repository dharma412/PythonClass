#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/language.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $


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
