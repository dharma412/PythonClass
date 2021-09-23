#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/findevent.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $
"""
SARF CLI command: findevent
"""
import re
from sal.containers.yesnodefault import YES, NO, is_yes

import clictorbase

REQUIRED = clictorbase.REQUIRED
DEFAULT = clictorbase.DEFAULT
EXACT = clictorbase.EXACT


class NotFoundError(clictorbase.IafCliError): pass


class findevent(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('No matching message IDs', EXACT): NotFoundError,
        })

    def __call__(self, input_dict=None, **kwargs):
        self._writeln(self.__class__.__name__)
        param_map = \
            clictorbase.IafCliParamMap(end_of_command=self._get_prompt())
        param_map['search_type'] = \
            ['which type of search you want to perform', DEFAULT, True]
        param_map['regex'] = ['regular expression to search for', DEFAULT]
        param_map['mid'] = ['Enter the Message ID', DEFAULT]
        param_map['log'] = ['number of the log you wish to use', DEFAULT, True]
        param_map['log_set'] = ['which set of logs to search', DEFAULT, True]
        param_map['log_files'] = ['Available mail log files', DEFAULT, True]
        param_map['result_item'] = \
            ['following matching message IDs were found. Please choose one to show additional log', DEFAULT, True]
        _params = input_dict or kwargs
        _as_list = _params.pop('as_list', YES)
        param_map.update(_params)
        self._process_input(param_map)
        return self._parse_lines(self.getbuf(), as_list=_as_list)

    def _parse_lines(self, raw, as_list=YES):
        res = []
        lines = raw.splitlines()
        # Match lines which starts with dates, i.e: Tue Dec 18 02:33:45 2007
        pat = re.compile(r'^\w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4}')
        for line in lines:
            if re.search(pat, line):
                res.append(line)
        if is_yes(as_list):
            return res
        return '\n'.join(res)


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    fe = findevent(cli_sess)

    print fe(search_type='ID', mid='1', log='mail_logs')
    print fe(search_type='FROM', regex='qa', log='mail_logs', log_set='Current')
    print fe(search_type='TO', regex='qa', log='mail_logs', log_set='select',
             log_files='1')
