#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/iseconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import string
from sal.exceptions import ConfigError
import clictorbase
from clictorbase import REQUIRED, DEFAULT, IafCliError, \
                        IafCliParamMap, IafCliConfiguratorBase
from sal.deprecated.expect import EXACT

class iseconfig(clictorbase.IafCliConfiguratorBase):
    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def setup(self, input_dict=None, **kwargs):
        self.clearbuf()
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['enable'] = ['Do you want to enable ISE', DEFAULT]
        param_map['servers'] = ['primary ISE server and optional secondary ISE server', DEFAULT]
        param_map['ise_data_timeout'] = ['timeout for ISE data', DEFAULT]
        param_map['backing_up'] = ['interval for backing up', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        if str(param_map['enable']).lower() == 'n':
            IafCliConfiguratorBase.ignore_unanswered_questions = True
        self._process_input(param_map)
        IafCliConfiguratorBase.ignore_unanswered_questions = False
        return self.getbuf()
