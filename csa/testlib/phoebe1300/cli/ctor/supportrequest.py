#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/supportrequest.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

"""
CLI command: supportrequest
"""

import socket
import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, \
    DEFAULT, REQUIRED
from sal.containers.yesnodefault import YES, NO


class supportrequest(IafCliConfiguratorBase):

    def __call__(self, input_dict=None, **kwargs):
        param_map = \
            IafCliParamMap(end_of_command='configuration information is generated...')
        self._restart()
        self._writeln(self.__class__.__name__)
        param_map['def_rcp'] = ['Do you want to send the support', DEFAULT]
        param_map['add_rcp'] = ['request to additional recipient(s)', DEFAULT]
        param_map['rcp_email'] = ['Please enter the email address', DEFAULT]
        param_map['exist_tick'] = ['Is this support request', DEFAULT]
        param_map['tech'] = ['select a technology', DEFAULT]
        param_map['sub_tech'] = ['select a subtechnology', DEFAULT]
        param_map['categ'] = ['select the problem category', DEFAULT]
        param_map['sub_categ'] = ['select a problem sub-category', DEFAULT, True]
        param_map['tick_num'] = ['enter the ticket number', REQUIRED]
        param_map['subj'] = ['enter a subject line', REQUIRED]
        param_map['descr'] = ['enter a description of your issue', DEFAULT]
        param_map['select_ccoid'] = ['Select the CCOID', DEFAULT, True]
        param_map['new_ccoid'] = ['enter the CCOID', REQUIRED]
        param_map['contact_name'] = ['name of the contact person', REQUIRED]
        param_map['contract_id'] = ['enter the contract ID', REQUIRED]
        param_map['corr_email'] = ['Please enter your email address', REQUIRED]
        param_map['add_info'] = ['enter any additional contact', DEFAULT]
        params = input_dict or kwargs
        print_req_ans = params.pop('print_req', DEFAULT)

        param_map.update(params)
        self._process_input(param_map, do_restart=False, timeout=1200)

        self._sess.clearbuf()
        self._query_response(print_req_ans, timeout=1200)

        return self._wait_for_prompt_line()
