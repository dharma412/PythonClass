#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/rollbackconfig.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

"""
CLI command: rollbackconfig
"""
import clictorbase
from sal.containers.yesnodefault import is_yes

DEFAULT = clictorbase.DEFAULT

class rollbackconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1
    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def rollback(self, commit_item, confirm='yes', commit='yes'):
        self._query_response('ROLLBACK')
        self._query_select_list_item(commit_item)
        idx = self._query('roll back the configuration?','value is not valid')
        if idx == 0:
            self._sess.writeln(confirm)
            if self._query('commit this configuration now?') == 0:
                self._writeln(commit)
                if is_yes(commit):
                    self._to_the_top(self.newlines)
        elif idx == 1:
            raise clictorbase.IafCliValueError('That value is not valid')

    def setup(self, input_dict=None, **kwargs):
        param_map = \
        clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['enable']  = ['enable the Rollback Configuration', DEFAULT]
        param_map['disable']  = ['disable the Rollback Configuration', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')
        return self._process_input(param_map)

